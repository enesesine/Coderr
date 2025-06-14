from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer


# Custom pagination class
class OfferPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'


# Custom filter to support filtering by min_price and max_delivery_time on related OfferDetail
class OfferFilter(FilterSet):
    min_price = NumberFilter(field_name='details__price', lookup_expr='gte')
    max_delivery_time = NumberFilter(field_name='details__delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['user', 'min_price', 'max_delivery_time']


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
        serializer.save(user=self.request.user)


# View for retrieving, updating or deleting a specific offer
class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_object(self):
        offer = super().get_object()
        if offer.user != self.request.user:
            raise PermissionDenied("You are not the creator of this offer.")
        return offer

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
