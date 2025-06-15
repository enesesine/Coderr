from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from auth_app.models import CustomUser
from django.db import models


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for linking an OfferDetail.
    Used when listing Offer objects with references to their pricing tiers.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        # Returns a frontend-compatible URL for a specific offer detail
        return f"/offerdetails/{obj.id}/"


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for OfferDetail.
    Used when creating or updating offer tiers like 'basic', 'standard', or 'premium'.
    """
    class Meta:
        model = OfferDetail
        fields = [
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'id'
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for displaying Offers.
    Includes linked details, minimum price and time, and user profile summary.
    """
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_min_price(self, obj):
        # Calculates the lowest price from all related offer tiers
        return obj.details.aggregate(models.Min("price"))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        # Calculates the fastest delivery time from all related offer tiers
        return obj.details.aggregate(models.Min("delivery_time_in_days"))['delivery_time_in_days__min'] or 0

    def get_user_details(self, obj):
        # Returns basic public profile info of the offer creator
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating or updating an Offer including its nested OfferDetails.
    Validates minimum number of detail packages and supports nested creation/update logic.
    """
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'image', 'description', 'details']

    def validate_details(self, value):
        # Enforces that a new offer must have at least 3 pricing tiers (basic, standard, premium)
        request = self.context.get("request")
        if request and request.method == "POST" and len(value) < 3:
            raise serializers.ValidationError("An offer must include at least 3 detail packages.")
        return value

    def create(self, validated_data):
        # Creates an Offer instance along with all its nested OfferDetail entries
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        # Updates Offer and its nested OfferDetails based on offer_type matching
        details_data = validated_data.pop('details', None)

        # Update fields on the offer itself
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle nested detail updates
        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                detail_obj = instance.details.filter(offer_type=offer_type).first()
                if detail_obj:
                    # Update existing detail with same type
                    for key, value in detail_data.items():
                        setattr(detail_obj, key, value)
                    detail_obj.save()
                else:
                    # Create new detail if not found
                    OfferDetail.objects.create(offer=instance, **detail_data)

        return instance
