from rest_framework import serializers
from auth_app.models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user profile.
    
    This serializer exposes selected fields from the CustomUser model,
    allowing profile data to be read and updated, with some fields set as read-only.
    """

    # Expose the user's ID using the alias 'user' (read-only)
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "user",           # alias for 'id'
            "username",       # read-only: cannot be changed after creation
            "first_name",
            "last_name",
            "file",           # e.g., profile picture or related upload
            "location",       # optional location data
            "tel",            # phone number
            "description",    # profile bio/description
            "working_hours",  # availability or business hours
            "type",           # user type: customer or business (read-only)
            "email",          # email address (read-only)
            "created_at",     # registration date (read-only)
            "uploaded_at"     # file upload date
        ]
        read_only_fields = ["username", "email", "type", "created_at"]

    def to_representation(self, instance):
        """
        Convert null values for specific fields to empty strings in the serialized output.

        This helps maintain frontend consistency and avoids 'null' values
        where empty strings are expected.
        """
        data = super().to_representation(instance)
        for field in [
            "first_name", "last_name", "file", "location", 
            "tel", "description", "working_hours"
        ]:
            if data[field] is None:
                data[field] = ""
        return data
