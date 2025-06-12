# offers_app/api/urls.py
from django.urls import path
from .views import OfferListCreateView, OfferDetailView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list-create'),
    path('offers/<int:id>/', OfferDetailView.as_view(), name='offer-detail'),  
]
