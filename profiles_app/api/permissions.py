from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerProfile(BasePermission):
    """
    Custom permission to allow access only if the user is modifying their own profile.

    This permission ensures that users cannot edit or view other users' profiles
    unless additional permissions are granted elsewhere (e.g. admin access).
    """

    def has_object_permission(self, request, view, obj):
        # Prevent access for unauthenticated users
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.id == request.user.id
