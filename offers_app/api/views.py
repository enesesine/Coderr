from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer
from .serializers import OfferSerializer, OfferCreateSerializer


class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['user']
    ordering_fields = ['updated_at', 'details__price']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_create(self, serializer):
        serializer.save()


class OfferDetailView(RetrieveUpdateDestroyAPIView):  # <--- DELETE jetzt unterstützt
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  
    lookup_url_kwarg = 'id'

    def get_object(self):
        offer = super().get_object()
        if offer.user != self.request.user:
            raise PermissionDenied("Du bist nicht der Ersteller dieses Angebots.")
        return offer

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferCreateSerializer
        return OfferSerializer

    def perform_update(self, serializer):
        serializer.save()
