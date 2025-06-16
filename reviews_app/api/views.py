from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from reviews_app.models import Review
from .serializers import ReviewSerializer


class ReviewListView(ListCreateAPIView):
    """
    View to list all reviews with optional filtering and ordering.

    - Requires authentication.
    - Supports filtering by 'business_user' and 'reviewer'.
    - Supports ordering by 'updated_at' and 'rating'.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']


class ReviewCreateView(CreateAPIView):
    """
    View to create a new review.

    - Only users with the 'customer' role can create reviews.
    - A customer can only leave one review per business user.
    - The reviewer is automatically set to the current authenticated user.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Only customers can review
        if user.type != 'customer':
            raise PermissionDenied("Only users with the type 'customer' can create reviews.")

        business_user = request.data.get("business_user")
        if not business_user:
            raise ValidationError({"business_user": "This field is required."})

        # Check for duplicate
        if Review.objects.filter(reviewer=user, business_user_id=business_user).exists():
            raise ValidationError({"error": "You have already submitted a review for this business user."})

        # Serialize with validated reviewer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewUpdateView(UpdateAPIView):
    """
    View to update an existing review.

    - Only the user who created the review (reviewer) can update it.
    - Supports partial updates using PATCH.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        review = super().get_object()

        # Only the reviewer is allowed to update the review
        if review.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can update it.")
        return review


class ReviewDeleteView(DestroyAPIView):
    """
    View to delete an existing review.

    - Only the user who created the review (reviewer) can delete it.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        review = super().get_object()

        # Only the reviewer is allowed to delete the review
        if review.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can delete it.")
        return review
