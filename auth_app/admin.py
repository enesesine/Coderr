# auth_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Extends the default Django UserAdmin to show our extra fields but keeps
    non-editable timestamps read-only, so the admin form can be rendered.
    """
    # show the role switcher
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("type", "file", "location", "tel",
                           "description", "working_hours")}),
    )

    # make sure auto_now/auto_now_add fields don't hit the form
    readonly_fields = ("created_at", "uploaded_at")  # <-- FIX

    # list view columns
    list_display = ("username", "email", "type", "is_staff", "created_at")
    list_filter = ("type", "is_staff", "is_superuser", "is_active")


admin.site.register(CustomUser, CustomUserAdmin)
