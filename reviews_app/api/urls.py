from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:id>/', ReviewUpdateView.as_view(), name='review-update'),
    path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
