from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
    """
    API endpoint for user registration.
    Accepts user details, creates a new user, and returns an auth token.
    """
    permission_classes = []  # Public endpoint – no authentication required

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate a token for the newly created user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        # Return validation errors if the request is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    Accepts username and password, authenticates the user, and returns an auth token.
    """
    permission_classes = []  # Public endpoint – no authentication required

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Reuse or generate a token for the authenticated user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        # Return error if authentication fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
