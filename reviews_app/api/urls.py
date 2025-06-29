# reviews_app/api/urls.py
from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path("reviews/",          ReviewListCreateView.as_view(), name="review-list-create"),
    path("reviews/<int:id>/", ReviewDetailView.as_view(),    name="review-detail"),
]
