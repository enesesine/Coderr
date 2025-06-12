from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:id>/', ReviewUpdateView.as_view(), name='review-update'),
]
