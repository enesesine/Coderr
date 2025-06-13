from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Extend the default Django UserAdmin to include custom fields
class CustomUserAdmin(UserAdmin):
    # Add 'user_type' to the admin form display (in the fieldsets)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type',)}),
    )

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
