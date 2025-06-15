from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.response import Response
from rest_framework import status
from orders_app.models import Order
from offers_app.models import OfferDetail
from .serializers import OrderSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q  # <- WICHTIG: Das löst deinen Q-Fehler

User = get_user_model()


class OrderListCreateView(ListCreateAPIView):
    """
    Handles listing and creation of orders.

    GET: Returns a list of orders where the user is either the customer or the business user.
    POST: Allows a customer to create an order from an existing OfferDetail.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)  # <- Fix hier
        )

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.user_type != "customer":
            raise PermissionDenied("Only users of type 'customer' are allowed to create orders.")

        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            raise ValidationError({"offer_detail_id": "This field is required."})

        try:
            offer_detail = OfferDetail.objects.select_related('offer__user').get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise NotFound("Offer detail not found.")

        # Create order using offer detail info
        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status='in_progress'
        )

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateView(RetrieveUpdateAPIView):
    """
    Allows business users to update the status of an order.
    PATCH: Only the business user can modify the order status.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        order = super().get_object()
        if self.request.user != order.business_user:
            raise PermissionDenied("Only the business partner can update the order status.")
        return order

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if "status" not in request.data:
            return Response(
                {"detail": "Only the 'status' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST
            )
        partial_data = {"status": request.data["status"]}
        serializer = self.get_serializer(instance, data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class OrderDeleteView(DestroyAPIView):
    """
    Deletes an order.
    Only admin users are authorized to perform this action.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def get_object(self):
        try:
            return Order.objects.get(pk=self.kwargs["id"])
        except Order.DoesNotExist:
            raise NotFound("The order was not found.")


class CompletedOrderCountView(APIView):
    """
    Returns the number of completed orders for a given business user.
    This endpoint does not require authentication.
    """
    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
        except User.DoesNotExist:
            raise NotFound("Business user not found.")

        count = Order.objects.filter(business_user=user, status='completed').count()
        return Response({"completed_order_count": count}, status=status.HTTP_200_OK)


class OrdersForBusinessView(ListAPIView):
    """
    Returns all orders assigned to the authenticated business user.
    GET: Only the business_user will see relevant orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(business_user=self.request.user)
