from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
    """
    Endpoint for registering a new user.
    - Accepts: username, email, password, repeated_password, and user type.
    - Returns: an authentication token along with user information.
    """
    permission_classes = []  # Open access

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create or retrieve an auth token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        # Return any validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Endpoint for user login.
    - Accepts: username and password
    - Returns: an authentication token and user details if valid
    """
    permission_classes = []  # Open access

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Create or retrieve an auth token for the user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        # Return error if credentials are invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
