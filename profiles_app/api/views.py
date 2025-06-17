# profiles_app/api/views.py
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from auth_app.models import CustomUser
from .serializers import ProfileSerializer
from .permissions import IsOwnerProfile


class UserProfileView(RetrieveUpdateAPIView):
    """
    GET   /api/profile/<id>/        – view any profile (auth required)  
    PATCH /api/profile/<id>/        – **only the owner** may update

    The IsOwnerProfile permission checks object-level access, but we add an
    extra guard inside update() as a fallback.
    """
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]
    lookup_field = "pk"

    # extra safety-net – abort before DRF updates a non-owned object
    def update(self, request, *args, **kwargs):
        if int(kwargs["pk"]) != request.user.id:
            raise PermissionDenied("You can only modify your own profile.")
        return super().update(request, *args, **kwargs)


class BusinessUserListView(ListAPIView):
    """
    GET /api/profiles/business/ – list all business accounts (auth required)
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type="business")


class CustomerUserListView(ListAPIView):
    """
    GET /api/profiles/customer/ – list all customer accounts (auth required)
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(type="customer")
