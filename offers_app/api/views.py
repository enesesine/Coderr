# offers_app/api/views.py 

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferCreateSerializer, OfferDetailSerializer




class OfferPagination(PageNumberPagination):
    """Default page-size 1 (Postman-Tests) – overridable via ?page_size=."""
    page_size = 1
    page_size_query_param = "page_size"




class OfferFilter(FilterSet):
    """?min_price= & ?max_delivery_time= für verknüpfte OfferDetails"""
    min_price = NumberFilter(field_name="details__price", lookup_expr="gte")
    max_delivery_time = NumberFilter(
        field_name="details__delivery_time_in_days", lookup_expr="lte"
    )

    class Meta:
        model = Offer
        fields = ["user", "min_price", "max_delivery_time"]




class IsOfferOwnerOrReadOnly(BasePermission):
    """Read für alle, Write nur für den Ersteller."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user




class OfferListCreateView(ListCreateAPIView):
    """
    GET  /api/offers/          – public list  
    POST /api/offers/          – only *business* users may create
    """
    queryset = Offer.objects.all().distinct()
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = OfferPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ["updated_at", "details__price"]
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        return OfferCreateSerializer if self.request.method == "POST" else OfferSerializer

    def perform_create(self, serializer):
        if self.request.user.type != "business":
            raise PermissionDenied("Only users with type 'business' can create offers.")
       
        serializer.save()


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET    /api/offers/<id>/  
    PATCH  /api/offers/<id>/  – creator only  
    DELETE /api/offers/<id>/  – creator only
    """
    queryset = Offer.objects.all()
    permission_classes = [IsAuthenticated, IsOfferOwnerOrReadOnly]
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        return OfferCreateSerializer if self.request.method == "PATCH" else OfferSerializer


class OfferDetailRetrieveView(RetrieveAPIView):
    """GET /api/offerdetails/<id>/ – single pricing tier"""
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
