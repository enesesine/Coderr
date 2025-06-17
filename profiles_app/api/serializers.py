# profiles_app/api/serializers.py
from rest_framework import serializers
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    """
    Converts CustomUser instances to JSON for profile endpoints.

    API contract:
    • first_name, last_name, location, tel, description, working_hours
      → never null – return "" when empty.
    • created_at must always be present (ISO-format).
    """

    # Force CharFields to fallback to "" instead of None
    first_name = serializers.CharField(allow_blank=True, default="")
    last_name = serializers.CharField(allow_blank=True, default="")
    location = serializers.CharField(allow_blank=True, default="")
    tel = serializers.CharField(allow_blank=True, default="")
    description = serializers.CharField(allow_blank=True, default="")
    working_hours = serializers.CharField(allow_blank=True, default="")

    class Meta:
        model = CustomUser
        # Fields required by the two profile endpoints
        fields = [
            "user",          # PK in related endpoints, kept for compatibility
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
        read_only_fields = ["user", "username", "type", "email", "created_at"]

    def to_representation(self, instance):
        """
        Post-process default DRF representation so that *no* field is null.

        Any None -> "" (only for the string fields we expose).
        """
        rep = super().to_representation(instance)

        string_fields = (
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        )
        for f in string_fields:
            if rep[f] is None:
                rep[f] = ""

        # created_at could theoretisch None sein, wenn Record manuell angelegt wurde
        if rep["created_at"] is None:
            rep["created_at"] = ""

        return rep
