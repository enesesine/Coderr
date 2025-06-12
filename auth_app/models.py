from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('business', 'Business'),
    ]
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Diese Felder jetzt ergänzen:
    file = models.CharField(max_length=255, blank=True, default="")
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username
