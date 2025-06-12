from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from reviews_app.models import Review
from .serializers import ReviewSerializer

class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
