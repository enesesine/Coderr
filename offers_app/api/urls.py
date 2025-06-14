from django.urls import path
from .views import (
    OfferListCreateView,
    OfferDetailView,
    OfferDetailRetrieveView
)

# URL configuration for the offers_app API endpoints
urlpatterns = [

    # Endpoint to list all offers or create a new offer (GET/POST)
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),

    # Endpoint to retrieve, update, or delete a specific offer by ID (GET/PATCH/DELETE)
    path('offers/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),

    # Endpoint to retrieve a single OfferDetail (tier/package) by ID (GET)
    path('offerdetails/<int:id>/', OfferDetailRetrieveView.as_view(), name='offerdetail-detail'),
]
