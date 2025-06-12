from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import status
from reviews_app.models import Review
from .serializers import ReviewSerializer


class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.user_type != 'customer':
            raise PermissionDenied("Nur Benutzer mit dem Typ 'customer' dürfen Bewertungen erstellen.")

        business_user = self.request.data.get("business_user")
        if not business_user:
            raise ValidationError({"business_user": "Dieses Feld wird benötigt."})

        if Review.objects.filter(reviewer=user, business_user_id=business_user).exists():
            raise ValidationError({"error": "Du hast bereits eine Bewertung für diesen Geschäftsbenutzer abgegeben."})

        serializer.save(reviewer=user)


class ReviewUpdateView(RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        review = super().get_object()
        if self.request.user != review.reviewer:
            raise PermissionDenied("Du darfst nur deine eigene Bewertung bearbeiten.")
        return review

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        partial_data = {
            key: request.data[key]
            for key in ['rating', 'description']
            if key in request.data
        }

        serializer = self.get_serializer(instance, data=partial_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
