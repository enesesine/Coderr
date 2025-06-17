from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import (
    PermissionDenied,
    NotFound,
    ValidationError,
    ParseError,
)
from rest_framework.response import Response
from rest_framework import status

from orders_app.models import Order
from offers_app.models import OfferDetail
from .serializers import OrderSerializer

User = get_user_model()

 
class OrderListCreateView(ListCreateAPIView):
    """
    GET  /api/orders/
        – Return every order where the current user is *either* customer_user
          *or* business_user (auth required).

    POST /api/orders/
        – A *customer* creates an order from an OfferDetail snapshot.
          ◦ Content-Type must be `application/json`.
          ◦ Body must contain valid JSON with field  `offer_detail_id`.

    Expected error codes:
        400  invalid JSON / missing fields
        401  unauthenticated
        403  non-customer tries to create
        404  offer detail not found
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

   
    def create(self, request, *args, **kwargs):
        
        if request.content_type != "application/json":
            return Response(
                {"detail": "Content-Type must be application/json"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            data = request.data  
        except ParseError:
            return Response(
                {"detail": "Request body is not valid JSON"},
                status=status.HTTP_400_BAD_REQUEST,
            )

       
        user = request.user
        if user.type != "customer":
            raise PermissionDenied(
                "Only users of type 'customer' are allowed to create orders."
            )

        
        offer_detail_id = data.get("offer_detail_id")
        if not offer_detail_id:
            raise ValidationError({"offer_detail_id": "This field is required."})

        try:
            offer_detail = OfferDetail.objects.select_related("offer__user").get(
                pk=offer_detail_id
            )
        except OfferDetail.DoesNotExist:
            raise NotFound("Offer detail not found.")

       
        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )

        return Response(
            OrderSerializer(order).data, status=status.HTTP_201_CREATED
        )



class OrderStatusUpdateView(RetrieveUpdateAPIView):
    """
    PATCH /api/orders/<id>/
        – Only the `business_user` of that order may patch **status**.

    Error codes:
        400  if 'status' missing
        401  unauthenticated
        403  user is not business partner
        404  order not found
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        order = super().get_object()
        if self.request.user != order.business_user:
            raise PermissionDenied("Only the business partner can update the status.")
        return order

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if "status" not in request.data:
            return Response(
                {"detail": "Only the 'status' field can be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            instance, data={"status": request.data["status"]}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class OrderDeleteView(DestroyAPIView):
    """
    DELETE /api/orders/<id>/delete/
        – Hard delete (staff / admin only).
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"

    def get_object(self):
        try:
            return Order.objects.get(pk=self.kwargs["id"])
        except Order.DoesNotExist:
            raise NotFound("The order was not found.")


class OrdersForBusinessView(ListAPIView):
    """
    GET /api/orders/business/
        – Auth’d business user sees every order where he/she is `business_user`.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(business_user=self.request.user)


class OrderCountView(APIView):
    """
    GET – Number of *in_progress* orders for the given business profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            biz = User.objects.get(pk=business_user_id, type="business")
        except User.DoesNotExist:
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cnt = Order.objects.filter(business_user=biz, status="in_progress").count()
        return Response({"order_count": cnt}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    """
    GET – Completed order count for a business profile (public).
    """
    permission_classes = []

    def get(self, request, business_user_id):
        try:
            biz = User.objects.get(pk=business_user_id, type="business")
        except User.DoesNotExist:
            return Response(
                {"detail": "Business user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cnt = Order.objects.filter(business_user=biz, status="completed").count()
        return Response({"completed_order_count": cnt}, status=status.HTTP_200_OK)
