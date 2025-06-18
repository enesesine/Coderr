# reviews_app/api/views.py
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from reviews_app.models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(ListCreateAPIView):
    """
    GET  /api/reviews/
         • Optional filters  
           ?business_user=<id> **oder** ?business_user_id=<id>  
           ?reviewer=<id>       **oder** ?reviewer_id=<id>  
         • Optional ordering: ?ordering=updated_at | -rating

    POST /api/reviews/
         • Only 'customer' profiles may create exactly **one** review
           per business_user.
    """
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ["business_user", "reviewer"]
    ordering_fields    = ["updated_at", "rating"]

    def get_queryset(self):
        """
        Postman-Tests nutzen die Suffix-Parameter *business_user_id* /
        *reviewer_id*.  Wir fangen sie hier ab; zusätzlich funktionieren
        weiterhin die „normalen“ Query-Filter von DjangoFilter.
        """
        qs = Review.objects.all()

        biz_id = self.request.query_params.get("business_user_id")
        rev_id = self.request.query_params.get("reviewer_id")

        if biz_id is not None:
            qs = qs.filter(business_user_id=biz_id)
        if rev_id is not None:
            qs = qs.filter(reviewer_id=rev_id)

        return qs


    def perform_create(self, serializer):
        user = self.request.user

        if user.type != "customer":
            raise PermissionDenied("Only users with type 'customer' can create reviews.")

        business_user = self.request.data.get("business_user")
        if not business_user:
            raise ValidationError({"business_user": "This field is required."})

        if Review.objects.filter(reviewer=user, business_user_id=business_user).exists():
            raise ValidationError({"detail": "You have already reviewed this business user."})

        serializer.save(reviewer=user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET     /api/reviews/<id>/        – retrieve  
    PATCH   /api/reviews/<id>/        – update (author only)  
    DELETE  /api/reviews/<id>/delete/ – delete (author only → returns 204)
    """
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
    permission_classes  = [IsAuthenticated]
    lookup_field        = "id"

    def get_object(self):
        obj = super().get_object()
        if obj.reviewer != self.request.user:
            raise PermissionDenied("Only the author of this review can modify or delete it.")
        return obj

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)
