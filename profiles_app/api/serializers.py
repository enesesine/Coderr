# profiles_app/api/serializers.py
from rest_framework import serializers
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serialises a CustomUser for the profile endpoints.

    • first_name, last_name, location, tel, description, working_hours
      are never null – they fall back to an empty string.
    • email is writable (PATCH) but always returned.
    • created_at is always included (ISO 8601).
    """

    user = serializers.IntegerField(source="id", read_only=True)
    username = serializers.CharField(read_only=True)

    # make all optional text fields default to "" when missing
    first_name     = serializers.CharField(allow_blank=True, default="")
    last_name      = serializers.CharField(allow_blank=True, default="")
    location       = serializers.CharField(allow_blank=True, default="")
    tel            = serializers.CharField(allow_blank=True, default="")
    description    = serializers.CharField(allow_blank=True, default="")
    working_hours  = serializers.CharField(allow_blank=True, default="")
    email = serializers.EmailField(required=False)

    class Meta:
        model  = CustomUser
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = ["user", "username", "type", "created_at"]

    # never return null strings
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for f in (
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        ):
            if rep[f] is None:
                rep[f] = ""
        if rep["created_at"] is None:
            rep["created_at"] = ""
        return rep
