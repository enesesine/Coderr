from rest_framework import serializers
from auth_app.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Handles password validation and ensures both passwords match before user creation.
    """
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'repeated_password', 'type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validates that password and repeated_password match,
        and that the password meets Django's validation criteria.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['password'])  # Validate using Django's built-in password validators
        return data

    def create(self, validated_data):
        """
        Removes repeated_password from the data and creates the user.
        """
        validated_data.pop('repeated_password')  # No need to store this field
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Authenticates the user using Django's built-in authentication system.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates the user's credentials.
        If invalid, raises an authentication error.
        """
        user = authenticate(
            username=data.get("username"),
            password=data.get("password")
        )
        if not user:
            raise AuthenticationFailed("Invalid username or password.")

        data["user"] = user  # Include the authenticated user in the validated data
        return data
