# offers_app/api/serializers.py
from rest_framework import serializers
from django.db import models, transaction
from offers_app.models import Offer, OfferDetail


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer used inside OfferSerializer.
    Only exposes the id and a front-end friendly URL for the tier.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model  = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for a single tier (“basic”, “standard”, “premium”).
    Used for nested create / update operations.
    """
    class Meta:
        model  = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]
        read_only_fields = ["id"]


class OfferSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for listing / retrieving offers.
    Adds convenience fields for minimum price / delivery time
    and some public information about the creator.
    """
    details            = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price          = serializers.SerializerMethodField()
    min_delivery_time  = serializers.SerializerMethodField()
    user_details       = serializers.SerializerMethodField()

    class Meta:
        model  = Offer
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
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    # --------------------------------------------------------------------- #

    def get_min_price(self, obj):
        return obj.details.aggregate(models.Min("price"))["price__min"] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(models.Min("delivery_time_in_days"))[
            "delivery_time_in_days__min"
        ] or 0

    def get_user_details(self, obj):
        u = obj.user
        return {"first_name": u.first_name, "last_name": u.last_name, "username": u.username}


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used for POST /api/offers/ and PATCH /api/offers/<id>/.
    * On **create** exactly three detail objects are required (basic / standard / premium).
    * On **update** you may send 1–3 detail objects; only supplied fields get patched.
    * Duplicate offer_type values are rejected.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model  = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]

    # --------------------------------------------------------------------- #
    # validation helpers

    def validate_details(self, value):
        request_method = self.context["request"].method
        if request_method == "POST" and len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly 3 detail packages "
                "('basic', 'standard', 'premium')."
            )

        seen = set()
        for d in value:
            ot = d.get("offer_type")
            if ot in seen:
                raise serializers.ValidationError(
                    f"Duplicate offer_type '{ot}' detected."
                )
            seen.add(ot)
        return value

    # --------------------------------------------------------------------- #
    # transactional create / update

    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(user=self.context["request"].user, **validated_data)

        for d in details_data:
            OfferDetail.objects.create(offer=offer, **d)

        return offer

    @transaction.atomic
    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        # update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update / create tiers
        if details_data:
            for d in details_data:
                ot = d.get("offer_type")
                tier = instance.details.filter(offer_type=ot).first()
                if tier:
                    for k, v in d.items():
                        setattr(tier, k, v)
                    tier.save()
                else:
                    OfferDetail.objects.create(offer=instance, **d)

        return instance
