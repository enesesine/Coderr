from django.db import models
from auth_app.models import CustomUser

class Review(models.Model):
    business_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='written_reviews')
    rating = models.PositiveSmallIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review von {self.reviewer} für {self.business_user} ({self.rating} Sterne)"
