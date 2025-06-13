"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information, see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import include(): from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # JWT authentication endpoints
    # Used to obtain a new access and refresh token pair
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Used to refresh the access token using a valid refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Authentication app routes (e.g., login, registration)
    path('', include('auth_app.urls')),

    # Profile management routes (e.g., user profile view/update)
    path('api/', include('profiles_app.api.urls')),

    # Offer-related endpoints (e.g., offer creation, listing)
    path('api/', include('offers_app.api.urls')),

    # Order-related endpoints (e.g., create, update, delete orders)
    path('api/', include('orders_app.api.urls')),

    # Review system routes (e.g., create, list, edit reviews)
    path('api/', include('reviews_app.api.urls')),

    # General platform statistics (e.g., review count, average rating)
    path('api/', include('base_info_app.api.urls')),
]
