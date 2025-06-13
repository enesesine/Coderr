from django.db import models
from auth_app.models import CustomUser

class Review(models.Model):
    """
    Represents a review that a customer leaves for a business user.

    Each review contains a numeric rating, a written description, and references
    to both the business user being reviewed and the reviewer (customer).
    """

    # The business user receiving the review
    business_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='received_reviews'
    )

    # The user (typically a customer) who wrote the review
    reviewer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='written_reviews'
    )

    # A numeric rating (e.g., 1 to 10) given by the reviewer
    rating = models.PositiveSmallIntegerField()

    # A detailed text description of the review
    description = models.TextField()

    # Timestamp when the review was first created
    created_at = models.DateTimeField(auto_now_add=True)

    # Timestamp when the review was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the review object.
        Shows who wrote the review and for whom, along with the rating.
        """
        return f"Review by {self.reviewer} for {self.business_user} ({self.rating} stars)"
