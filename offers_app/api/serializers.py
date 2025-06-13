from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from auth_app.models import CustomUser
from django.db import models


# Serializer that returns only the ID and a link for each OfferDetail
class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        # Generate a frontend-like URL path for offer details
        return f"/offerdetails/{obj.id}/"


# Serializer to handle the full representation of a single OfferDetail
class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


# Main serializer for reading Offer data, includes nested details and summary fields
class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id', 'user', 'title', 'image', 'description',
            'created_at', 'updated_at', 'details',
            'min_price', 'min_delivery_time', 'user_details'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def get_min_price(self, obj):
        # Returns the minimum price from all related OfferDetails
        return obj.details.aggregate(models.Min("price"))['price__min'] or 0

    def get_min_delivery_time(self, obj):
        # Returns the minimum delivery time from all related OfferDetails
        return obj.details.aggregate(models.Min("delivery_time_in_days"))['delivery_time_in_days__min'] or 0

    def get_user_details(self, obj):
        # Returns a subset of user profile fields associated with the offer
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }


# Serializer for creating and updating Offer along with nested OfferDetails
class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def validate_details(self, value):
        # Ensure that an offer contains at least 3 detail packages
        request = self.context.get("request")
        if request and request.method == "POST" and len(value) < 3:
            raise serializers.ValidationError("An offer must include at least 3 detail packages.")
        return value

    def create(self, validated_data):
        # Handles nested creation of Offer and related OfferDetails
        details_data = validated_data.pop('details')
        user = self.context['request'].user
        offer = Offer.objects.create(user=user, **validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        # Handles updating Offer and its nested OfferDetails
        details_data = validated_data.pop('details', None)

        # Update basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            for detail_data in details_data:
                offer_type = detail_data.get("offer_type")
                # Check if the detail already exists by type
                detail_obj = instance.details.filter(offer_type=offer_type).first()
                if detail_obj:
                    # Update existing detail
                    for key, value in detail_data.items():
                        setattr(detail_obj, key, value)
                    detail_obj.save()
                else:
                    # Create new detail if not found
                    OfferDetail.objects.create(offer=instance, **detail_data)

        return instance
