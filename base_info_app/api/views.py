from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from reviews_app.models import Review
from offers_app.models import Offer
from auth_app.models import CustomUser
from django.db.models import Avg


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        average_rating = round(average_rating, 1)

        business_profile_count = CustomUser.objects.filter(user_type='business').count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        })
