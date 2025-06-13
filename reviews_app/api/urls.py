from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

# URL configuration for the review-related endpoints
urlpatterns = [
    # Lists all reviews, optionally filtered or ordered
    path('reviews/', ReviewListView.as_view(), name='review-list'),

    # Allows a customer to create a new review for a business user
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),

    # Allows the original reviewer to update their review (only 'rating' and 'description')
    path('reviews/<int:id>/', ReviewUpdateView.as_view(), name='review-update'),

    # Allows the original reviewer to delete their review
    path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
