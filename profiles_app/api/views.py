from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from auth_app.models import CustomUser
from .serializers import ProfileSerializer
from .permissions import IsOwnerProfile


class UserProfileView(RetrieveUpdateAPIView):
    """
    Retrieve and update the authenticated user's profile.
    
    Only the profile owner can update their profile (enforced by IsOwnerProfile permission).
    """
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]
    lookup_field = "pk"  # Profile is accessed by user ID (primary key)


class BusinessUserListView(ListAPIView):
    """
    List all users with the type 'business'.
    
    Requires the user to be authenticated.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returns only users of type 'business'
        return CustomUser.objects.filter(type='business')


class CustomerUserListView(ListAPIView):
    """
    List all users with the type 'customer'.
    
    Requires the user to be authenticated.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returns only users of type 'customer'
        return CustomUser.objects.filter(type='customer')
