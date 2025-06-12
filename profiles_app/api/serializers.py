from rest_framework import serializers
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "user",  # alias für id
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
            "uploaded_at"
        ]
        read_only_fields = ["username", "email", "type", "created_at"]

    user = serializers.IntegerField(source='id', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # leere Strings statt null
        for field in ["first_name", "last_name", "file", "location", "tel", "description", "working_hours"]:
            if data[field] is None:
                data[field] = ""
        return data
