from django.db import models
from django.conf import settings

class Order(models.Model):
    """
    Represents a service order between a customer and a business user based on an offer.

    Tracks details like title, delivery time, features, price, and current status of the order.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),    # Order is currently being worked on
        ('completed', 'Completed'),        # Order has been completed
        ('cancelled', 'Cancelled'),        # Order was cancelled
    ]

    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    # The customer who placed the order

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_orders'
    )
    # The business user who is responsible for fulfilling the order

    title = models.CharField(max_length=255)
    # Title or name of the order

    revisions = models.IntegerField()
    # Number of allowed revisions for the order

    delivery_time_in_days = models.IntegerField()
    # Number of days estimated for delivery

    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Total price for the order

    features = models.JSONField(default=list)
    # A list of features included in the order, stored as JSON (e.g., ["Logo Design", "Flyer"])

    offer_type = models.CharField(max_length=20)
    # Type of offer (e.g., 'basic', 'premium')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    # Current status of the order (progress tracking)

    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the order was created

    updated_at = models.DateTimeField(auto_now=True)
    # Timestamp when the order was last updated

    def __str__(self):
        return self.title
        # Human-readable representation of the order (mainly used in Django admin)
