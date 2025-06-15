from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from orders_app.models import Order
from offers_app.models import OfferDetail
from .serializers import OrderSerializer
from orders_app import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OrderListCreateView(ListCreateAPIView):
    """
    Handles listing and creation of orders.

    GET: Returns a list of orders that belong to the current user as either customer or business user.
    POST: Allows a customer to create an order based on a specific OfferDetail.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Return orders where the user is either customer or business
        return Order.objects.filter(
            models.Q(customer_user=user) | models.Q(business_user=user)
        )

    def create(self, request, *args, **kwargs):
        user = request.user

        # Only users with type 'customer' can create orders
        if user.type != "customer":
            raise PermissionDenied("Only users of type 'customer' are allowed to create orders.")

        offer_detail_id = request.data.get("offer_detail_id")
        if not offer_detail_id:
            return self._bad_request("Field 'offer_detail_id' is required.")

        try:
            offer_detail = OfferDetail.objects.select_related('offer__user').get(pk=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise NotFound("Offer detail not found.")

        # Create new order from offer detail
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
        return Response(serializer.data, status=201)

    def _bad_request(self, message):
        # Helper method to return a 400 error with a custom message
        return Response({"error": message}, status=400)


class OrderStatusUpdateView(RetrieveUpdateAPIView):
    """
    Allows business users to update the status of an order.
    
    PATCH: Only the business user assigned to the order may update its status.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        order = super().get_object()
        # Only the business user associated with the order may update it
        if self.request.user != order.business_user:
            raise PermissionDenied("Only the business partner can update the order status.")
        return order

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Ensure only 'status' is being updated
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
    
    Only admin users (staff) are allowed to perform this action.
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

    Accessible without authentication.
    """
    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id)
        except User.DoesNotExist:
            raise NotFound("Business user not found.")

        count = Order.objects.filter(business_user=user, status='completed').count()
        return Response({"completed_order_count": count}, status=200)
