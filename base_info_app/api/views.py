from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import CustomUser
from django.db.models import Avg

class BaseInfoView(APIView):
    """
    View to retrieve basic statistics about the platform.

    Accessible by anyone (no authentication required).
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Returns general platform information:
        - Total number of reviews
        - Average rating across all reviews (rounded to 1 decimal)
        - Total number of business profiles
        - Total number of offers
        """

        # Total number of reviews
        review_count = Review.objects.count()

        # Calculate average rating, default to 0 if none exist
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        average_rating = round(average_rating, 1)

        # Count business user profiles
        business_profile_count = CustomUser.objects.filter(user_type='business').count()

        # Total number of offers
        offer_count = Offer.objects.count()

        # Return data as JSON response
        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })
