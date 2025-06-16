from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Extend the default Django UserAdmin to include custom fields
class CustomUserAdmin(UserAdmin):
    # Add custom fields (including 'type') to the admin form display
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('type', 'file', 'location', 'tel', 'description', 'working_hours', 'uploaded_at')}),
    )

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
