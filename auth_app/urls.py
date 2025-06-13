from django.urls import path, include

# This file defines the base URL configuration for the 'auth_app' application.
# It includes all routes defined in 'auth_app.api.urls' under the '/api/' prefix.

urlpatterns = [
    # Include authentication-related API routes under the 'api/' path
    path('api/', include('auth_app.api.urls')),
]
