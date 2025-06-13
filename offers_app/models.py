from django.db import models
from auth_app.models import CustomUser

class Offer(models.Model):
    """
    Represents a general offer created by a business user.
    This is the high-level container for one or more offer details (variants).
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='offers'
    )  # The business user who created the offer
    title = models.CharField(max_length=255)  # Title of the offer
    image = models.ImageField(
        upload_to='offer_images/',
        null=True,
        blank=True
    )  # Optional image representing the offer
    description = models.TextField()  # Description of the offer
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Auto-updated on changes

    def __str__(self):
        return self.title  # String representation of the offer


class OfferDetail(models.Model):
    """
    Represents specific versions (tiers) of an offer, like Basic, Standard, Premium.
    Includes pricing, delivery time, and features for each variant.
    """
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name='details'
    )  # Parent offer this detail belongs to
    title = models.CharField(max_length=255, default="")  # Title of the detail/tier
    revisions = models.IntegerField(default=0)  # Number of revisions allowed
    delivery_time_in_days = models.IntegerField(default=1)  # Delivery time in days
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for this detail
    features = models.JSONField(default=list)  # List of features (stored as JSON)
    offer_type = models.CharField(
        max_length=10,
        choices=OFFER_TYPE_CHOICES
    )  # Type of offer: basic/standard/premium

    def __str__(self):
        return f"{self.offer.title} - {self.title}"  # String representation
