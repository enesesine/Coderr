from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
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


class ReviewUpdateView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        review = super().get_object()
        if review.reviewer != self.request.user:
            raise PermissionDenied("Nur der Ersteller darf diese Bewertung aktualisieren.")
        return review


class ReviewDeleteView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        review = super().get_object()
        if review.reviewer != self.request.user:
            raise PermissionDenied("Nur der Ersteller darf diese Bewertung löschen.")
        return review
