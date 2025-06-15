from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    # GET: List reviews, optionally filtered
    # POST: Create a new review (only for customers)
    path('reviews/', ReviewListView.as_view(), name='review-list'),

    # POST: Create a review
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),

    # PATCH: Update a review by ID
    path('reviews/<int:id>/', ReviewUpdateView.as_view(), name='review-update'),

    # DELETE: Delete a review by ID
    path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
