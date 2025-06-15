from django.urls import path
from .views import (
    OrderListCreateView,
    OrderStatusUpdateView,
    OrderDeleteView,
    CompletedOrderCountView,
    OrdersForBusinessView  
)

urlpatterns = [
    # GET: List all orders for the authenticated user
    # POST: Create a new order (only allowed for customers)
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),

    # PATCH: Update the status of a specific order
    # Only the business user associated with the order is allowed
    path('orders/<int:id>/', OrderStatusUpdateView.as_view(), name='order-update'),

    # DELETE: Delete a specific order
    # Only admin users (staff) are allowed to delete
    path('orders/<int:id>/delete/', OrderDeleteView.as_view(), name='order-delete'),

    # GET: Retrieve the count of completed orders for a specific business user
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),

    # GET: List all orders for the currently authenticated business user
    path('orders/business/', OrdersForBusinessView.as_view(), name='orders-business'),
]
