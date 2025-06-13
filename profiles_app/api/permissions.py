from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerProfile(BasePermission):
    """
    Custom permission to allow access only if the user is modifying their own profile.

    This permission ensures that users cannot edit or view other users' profiles
    unless additional permissions are granted elsewhere (e.g. admin access).
    """

    def has_object_permission(self, request, view, obj):
        # Only allow access if the object's ID matches the authenticated user's ID
        return obj.id == request.user.id
