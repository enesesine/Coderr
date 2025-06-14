from django.urls import path
from .views import UserProfileView, BusinessUserListView, CustomerUserListView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/business/', BusinessUserListView.as_view(), name='business-users'),
    path('profiles/customer/', CustomerUserListView.as_view(), name='customer-users'),
]
