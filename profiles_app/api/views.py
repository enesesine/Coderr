# profiles_app/api/views.py
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from auth_app.models import CustomUser
from .serializers import ProfileSerializer
from .permissions import IsProfileOwnerOrReadOnly       


class UserProfileView(RetrieveUpdateAPIView):
    """
    • **GET   /api/profile/<id>/**  
      Any authenticated user can read every profile.

    • **PATCH /api/profile/<id>/**  
      Only the owner of the profile may update it.

    The object-level permission `IsProfileOwnerOrReadOnly` enforces the rule,
    but we add an explicit check in `update()` as an extra guard.
    """
    queryset           = CustomUser.objects.all()
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
    lookup_field       = "pk"

    def update(self, request, *args, **kwargs):
        """Refuse updates on foreign profiles before DRF hits the serializer."""
        if int(kwargs["pk"]) != request.user.id:
            raise PermissionDenied("You can only modify your own profile.")
        return super().update(request, *args, **kwargs)


class BusinessUserListView(ListAPIView):
    """
    GET /api/profiles/business/ – list all business accounts (auth required)
    """
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type="business")


class CustomerUserListView(ListAPIView):
    """
    GET /api/profiles/customer/ – list all customer accounts (auth required)
    """
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type="customer")
