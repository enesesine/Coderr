from rest_framework import serializers
from django.db import models

from offers_app.models import Offer, OfferDetail
from auth_app.models import CustomUser


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Lightweight representation – only ID plus a frontend-friendly URL.
    Shown when listing offers so the client can fetch each tier individually.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for a single pricing tier (basic / standard / premium …).
    Used inside Offer POST/PATCH bodies and when returning an OfferDetail directly.
    """
    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing / retrieving Offer objects.
    Adds aggregates (min price / delivery time) and basic creator info.
    """
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        read_only_fields = ["id", "created_at", "updated_at", "user"]
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min("price"))["price__min"] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min("delivery_time_in_days"))[
            "delivery_time_in_days__min"
        ] or 0

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username,
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used for POST (create) and PATCH (partial update) of an Offer
    together with its nested OfferDetails.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    # ---------- validation helpers ----------

    def _validate_unique_offer_types(self, details):
        """Prevent duplicate basic/standard/premium blocks."""
        seen = set()
        for d in details:
            t = d.get("offer_type")
            if t in seen:
                raise serializers.ValidationError(
                    f"Duplicate offer_type '{t}' detected. Each tier must be unique."
                )
            seen.add(t)

    def _validate_required_fields(self, details):
        """Ensure each tier contains all mandatory keys."""
        required = {
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        }
        for d in details:
            missing = required - d.keys()
            if missing:
                raise serializers.ValidationError(
                    f"Missing field(s) {', '.join(missing)} in detail block."
                )

    # ---------- field-level validation ----------

    def validate_details(self, value):
        request = self.context.get("request")
        if request and request.method == "POST" and len(value) < 3:
            raise serializers.ValidationError(
                "An offer must include at least 3 detail packages."
            )

        self._validate_unique_offer_types(value)
        self._validate_required_fields(value)
        return value

    # ---------- create / update ----------

    def create(self, validated_data):
        details_data = validated_data.pop("details")
        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        # update core offer fields
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # update or create nested tiers
        if details_data:
            for detail in details_data:
                tier_type = detail.get("offer_type")
                tier_obj = instance.details.filter(offer_type=tier_type).first()
                if tier_obj:
                    for k, v in detail.items():
                        setattr(tier_obj, k, v)
                    tier_obj.save()
                else:
                    OfferDetail.objects.create(offer=instance, **detail)

        return instance
