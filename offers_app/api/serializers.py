# offers_app/api/serializers.py
from rest_framework import serializers
from django.db import models, transaction
from offers_app.models import Offer, OfferDetail



VALID_OFFER_TYPES = {"basic", "standard", "premium"}
REQUIRED_TIER_FIELDS = {
    "title",
    "revisions",
    "delivery_time_in_days",
    "price",
    "features",
    "offer_type",
}




class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Very lightweight representation of a tier inside the *public* OfferSerializer.
    Only exposes its primary key and a front-end friendly link.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        # This keeps your front-end paths in one place
        return f"/offerdetails/{obj.id}/"





class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for a single pricing tier (“basic”, “standard”, “premium”).
    All fields are required – DRF enforces this automatically because
    they are not marked read-only / allow_null=True.
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
        read_only_fields = ["id"]





class OfferSerializer(serializers.ModelSerializer):
    """
    Serializer used for GET /api/offers/ and GET /api/offers/<id>/.
    Adds convenience fields (min_price/min_delivery_time) and a small slice
    of the creator’s public profile.
    """

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
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



    def get_min_price(self, obj):
        """Cheapest tier among basic/standard/premium."""
        return obj.details.aggregate(models.Min("price"))["price__min"] or 0

    def get_min_delivery_time(self, obj):
        """Fastest delivery-time among all tiers (days)."""
        return obj.details.aggregate(models.Min("delivery_time_in_days"))[
            "delivery_time_in_days__min"
        ] or 0

    def get_user_details(self, obj):
        u = obj.user
        return {"first_name": u.first_name, "last_name": u.last_name, "username": u.username}





class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Used for:
      • POST   /api/offers/          – create *three* tiers at once
      • PATCH  /api/offers/<id>/     – update 1-3 tiers

    Validation rules
    ----------------
    * POST:
        - exactly three tier objects
        - each tier must have a unique `offer_type`
        - offer_type set must be {basic, standard, premium}
    * PATCH:
        - 1-3 tier objects
        - any tier transmitted **must** contain *all* mandatory fields
          (we treat them as full overwrites, not partials)
        - no duplicate `offer_type`
    """

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ["id"]



    def validate_details(self, value):
        req = self.context["request"]
        method = req.method.upper()

  
        seen = set()
        for tier in value:
            ot = tier.get("offer_type")
            if ot not in VALID_OFFER_TYPES:
                raise serializers.ValidationError(
                    {"details": f"Unknown offer_type '{ot}' – must be basic / standard / premium."}
                )
            if ot in seen:
                raise serializers.ValidationError(
                    {"details": f"Duplicate offer_type '{ot}' supplied."}
                )
            seen.add(ot)

  
        if method == "POST":
            if len(value) != 3:
                raise serializers.ValidationError(
                    "Exactly three detail packages (basic, standard, premium) are required."
                )
            if seen != VALID_OFFER_TYPES:
                raise serializers.ValidationError(
                    "POST payload must include basic, standard and premium tiers."
                )

 
        if method == "PATCH":
            for idx, tier in enumerate(value, start=1):
                missing = [
                    f for f in REQUIRED_TIER_FIELDS
                    if f not in tier or tier[f] in (None, "", [])
                ]
                if missing:
                    raise serializers.ValidationError(
                        {f"details[{idx}]": f"Missing required fields: {', '.join(missing)}"}
                    )
        return value


    @transaction.atomic
    def create(self, validated_data):
        details_data = validated_data.pop("details")
        offer = Offer.objects.create(user=self.context["request"].user, **validated_data)

        for tier in details_data:
            OfferDetail.objects.create(offer=offer, **tier)
        return offer

    @transaction.atomic
    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        # scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # tiers
        if details_data:
            for tier_data in details_data:
                ot = tier_data["offer_type"]
                tier_obj = instance.details.filter(offer_type=ot).first()
                if tier_obj:
                    for field, val in tier_data.items():
                        setattr(tier_obj, field, val)
                    tier_obj.save()
                else:
                    OfferDetail.objects.create(offer=instance, **tier_data)

        return instance
