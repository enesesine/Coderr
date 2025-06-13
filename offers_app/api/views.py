from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer

# Custom pagination class to allow dynamic page size via query parameter
class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


# View for listing all offers or creating a new one
class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Authenticated users can POST; everyone can GET
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['user']  # Filter by user ID (creator of the offer)
    ordering_fields = ['updated_at', 'details__price']  # Allow ordering by last update and price
    search_fields = ['title', 'description']  # Enable search by title or description

    def get_serializer_class(self):
        # Use a different serializer for creation
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        # Save the offer with the user already associated from the serializer
        serializer.save()


# View for retrieving, updating or deleting a specific offer (by its creator)
class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_object(self):
        # Ensure only the owner of the offer can modify it
        offer = super().get_object()
        if offer.user != self.request.user:
            raise PermissionDenied("You are not the creator of this offer.")
        return offer

    def get_serializer_class(self):
        # Use different serializer for partial update
        if self.request.method == 'PATCH':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_update(self, serializer):
        # Perform save operation during update
        serializer.save()


# View for retrieving an individual OfferDetail by ID
class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
