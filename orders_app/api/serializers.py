from rest_framework import serializers
from orders_app.models import Order

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Handles conversion between Order model instances and JSON representations
    for API interactions.
    """

    class Meta:
        model = Order
        # List of fields to be included in the serialized output
        fields = [
            'id',                   # Unique identifier for the order
            'customer_user',        # The customer who placed the order
            'business_user',        # The business user who will fulfill the order
            'title',                # Title or short description of the order
            'revisions',            # Number of revisions allowed
            'delivery_time_in_days',# Delivery time in days
            'price',                # Total price for the order
            'features',             # List of included features (stored as JSON)
            'offer_type',           # Type of offer (e.g. basic, premium)
            'status',               # Status of the order (e.g. in_progress, completed)
            'created_at',           # Timestamp when the order was created
            'updated_at'            # Timestamp when the order was last updated
        ]
