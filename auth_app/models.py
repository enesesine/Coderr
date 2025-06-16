from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extended user model inheriting from Django's AbstractUser.
    Adds support for two user types: 'customer' and 'business',
    and additional profile fields.
    """

    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]

    # Defines the role of the user (customer or business)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Optional: File path or image URL associated with the user's profile
    file = models.CharField(max_length=255, blank=True, default="")

    # User's location (can be city, country, etc.)
    location = models.CharField(max_length=255, blank=True, default="")

    # User's phone number
    tel = models.CharField(max_length=50, blank=True, default="")

    # A brief description or bio of the user
    description = models.TextField(blank=True, default="")

    # User's working hours (for business users)
    working_hours = models.CharField(max_length=255, blank=True, default="")

    # Timestamp for when the user account was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp for when a profile-related file was uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username
