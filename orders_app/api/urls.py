from django.urls import path
from .views import OrderListCreateView, OrderStatusUpdateView, OrderDeleteView, CompletedOrderCountView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:id>/', OrderStatusUpdateView.as_view(), name='order-update'),
    path('orders/<int:id>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]
