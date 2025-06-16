from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerProfile(BasePermission):
    """
    Read for all auth-Users, write only for owners.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.id == request.user.id  
        return obj.id == request.user.id      