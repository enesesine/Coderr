from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProfileOwnerOrReadOnly(BasePermission):
    """
    • SAFE_METHODS (GET/HEAD/OPTIONS): allow for any authenticated user  
    • Other methods (PATCH/DELETE): only if the profile belongs to request.user
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.id == request.user.id
