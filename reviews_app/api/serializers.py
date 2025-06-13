from rest_framework import serializers
from reviews_app.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Converts Review instances to and from JSON representations.
    Ensures that certain fields are read-only (e.g., the reviewer and timestamps).
    """

    class Meta:
        model = Review 
        fields = '__all__'  
        read_only_fields = [
            'reviewer',      
            'created_at',    
            'updated_at'      
        ]
