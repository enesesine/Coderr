from django.urls import path
from .views import ReviewListView, ReviewUpdateView, ReviewDeleteView

# URL configuration for the review-related endpoints
urlpatterns = [
    # GET: List all reviews / POST: Create a new review
    path('reviews/', ReviewListView.as_view(), name='review-list-create'),

    # PATCH: Update a specific review (only the reviewer can do this)
    path('reviews/<int:id>/', ReviewUpdateView.as_view(), name='review-update'),

    # DELETE: Remove a specific review (only the reviewer can do this)
    path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
