from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer


# Custom pagination class
class OfferPagination(PageNumberPagination):
    page_size = 1  # Default page size
    page_size_query_param = 'page_size'  # Allow override via ?page_size=


# Custom filter to support filtering by min_price and max_delivery_time on related OfferDetail
class OfferFilter(FilterSet):
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['user', 'min_price', 'max_delivery_time']


# Custom permission: everyone can read, only creator can modify
class IsOfferOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to all users,
    but restrict write access (PATCH, DELETE) to the offer's creator.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True  # Allow GET, HEAD, OPTIONS
        return obj.user == request.user  # Allow write only for the creator


# View for listing or creating offers
class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all().distinct()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'details__price']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.type != "business":  
            raise PermissionDenied("Only users with type 'business' can create offers.")
        serializer.save(user=user)


# View for retrieving, updating or deleting a specific offer
class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOfferOwnerOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_update(self, serializer):
        serializer.save()


# View to retrieve a specific OfferDetail (tier)
class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
