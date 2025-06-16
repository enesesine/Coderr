from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from reviews_app.models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    """
    GET  /api/reviews/      → Liste aller Reviews (filter- & sortierbar)
    POST /api/reviews/      → Neues Review anlegen (nur Customer-User)
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["business_user", "reviewer"]
    ordering_fields = ["updated_at", "rating"]

    # einzig benötigte Überschreibung
    def perform_create(self, serializer):
        user = self.request.user

        # Nur Kunden dürfen bewerten
        if user.type != "customer":
            raise PermissionDenied(
                "Only users with the type 'customer' can create reviews."
            )

        business_user = self.request.data.get("business_user")
        if not business_user:
            raise ValidationError({"business_user": "This field is required."})

        if Review.objects.filter(reviewer=user, business_user_id=business_user).exists():
            raise ValidationError(
                {"detail": "You have already submitted a review for this business user."}
            )

        # Hier wird der reviewer verlässlich gesetzt
        serializer.save(reviewer=user)


class ReviewUpdateView(UpdateAPIView):
    """
    PATCH /api/reviews/<id>/   – Nur der Urheber darf aktualisieren
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        obj = super().get_object()
        if obj.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can update it.")
        return obj


class ReviewDeleteView(DestroyAPIView):
    """
    DELETE /api/reviews/<id>/delete/  – Nur der Urheber darf löschen
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_object(self):
        obj = super().get_object()
        if obj.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can delete it.")
        return obj
