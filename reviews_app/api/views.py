from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from reviews_app.models import Review
from .serializers import ReviewSerializer
from auth_app.models import CustomUser


class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']

    def create(self, request, *args, **kwargs):
        user = request.user

        if user.user_type != "customer":
            raise PermissionDenied("Nur Kunden dürfen Bewertungen erstellen.")

        business_user_id = request.data.get("business_user")
        if not business_user_id:
            return Response({"error": "Feld 'business_user' ist erforderlich."}, status=400)

        try:
            business_user = CustomUser.objects.get(id=business_user_id, user_type="business")
        except CustomUser.DoesNotExist:
            return Response({"error": "Kein gültiger Geschäftsbenutzer gefunden."}, status=404)

        if Review.objects.filter(reviewer=user, business_user=business_user).exists():
            return Response({"error": "Du hast bereits eine Bewertung für diesen Geschäftsbenutzer abgegeben."}, status=403)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(reviewer=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
