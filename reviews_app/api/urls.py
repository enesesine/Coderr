from django.urls import path
from .views import ReviewListCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path("reviews/", ReviewListCreateView.as_view(), name="review-list-create"),
    path("reviews/<int:id>/", ReviewUpdateView.as_view(), name="review-update"),
    path("reviews/<int:id>/delete/", ReviewDeleteView.as_view(), name="review-delete"),
]
