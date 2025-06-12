from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerProfile(BasePermission):

    """
    Erlaubt Zugriff nur, wenn der Benutzer sein eigenes Profil bearbeitet.
    """

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
