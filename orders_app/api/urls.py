from django.urls import path
from .views import (
    OrderListCreateView,
    OrderStatusUpdateView,
    OrderDeleteView,
    CompletedOrderCountView,
    OrderCountView  
)

urlpatterns = [
    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:id>/", OrderStatusUpdateView.as_view()),        
    path("orders/<int:id>/status/", OrderStatusUpdateView.as_view()), 
    path("orders/<int:id>/delete/", OrderDeleteView.as_view()),
    path("completed-order-count/<int:business_user_id>/", CompletedOrderCountView.as_view()),
    path("order-count/<int:business_user_id>/", OrderCountView.as_view()),   
]

