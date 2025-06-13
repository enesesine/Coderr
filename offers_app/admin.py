from django.contrib import admin
from .models import Offer, OfferDetail

# Inline configuration to display related OfferDetail objects directly within the Offer admin page
class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0  # No extra empty rows by default

# Custom admin configuration for the Offer model
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')  # Columns to show in the Offer list view
    inlines = [OfferDetailInline]  # Include OfferDetails inline on the Offer edit page

# Registering the models with their respective admin configurations
admin.site.register(Offer, OfferAdmin)  # Use the customized admin view for Offer
admin.site.register(OfferDetail)        # Register OfferDetail separately for direct access
