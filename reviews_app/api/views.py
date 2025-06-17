# reviews_app/api/views.py
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from reviews_app.models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    """
    GET  /api/reviews/               – list all reviews (auth-required, with filters)  
    POST /api/reviews/               – create a review (customer only)

    * Filters:* `?business_user=<id>` or `?reviewer=<id>`  
    * Ordering:* `?ordering=updated_at` or `?ordering=-rating`
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["business_user", "reviewer"]
    ordering_fields = ["updated_at", "rating"]

    def perform_create(self, serializer):
        user = self.request.user

        # Only customers are allowed to post reviews
        if user.type != "customer":
            raise PermissionDenied("Only users with type 'customer' can create reviews.")

        business_user = self.request.data.get("business_user")
        if not business_user:
            raise ValidationError({"business_user": "This field is required."})

        # One review per customer → business pair
        if Review.objects.filter(reviewer=user, business_user_id=business_user).exists():
            raise ValidationError({"detail": "You have already reviewed this business user."})

        serializer.save(reviewer=user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET     /api/reviews/<id>/   – retrieve  
    PATCH   /api/reviews/<id>/   – update (only the author)  
    DELETE  /api/reviews/<id>/   – delete (only the author, returns **204**)

    All operations require authentication.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    # ensure that only the review author can change / delete
    def get_object(self):
        obj = super().get_object()
        if obj.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can modify or delete it.")
        return obj

    # explicit 204 on successful delete
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
