from django.contrib import admin
from .models import Offer, OfferDetail

class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0

class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    inlines = [OfferDetailInline]

admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail)
