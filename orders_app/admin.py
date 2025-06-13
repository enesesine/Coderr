from django.contrib import admin
from orders_app.models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ['id', 'title', 'customer_user', 'business_user', 'price', 'status', 'created_at']
    
    # Fields that can be searched in the admin search bar
    search_fields = ['title', 'customer_user__username', 'business_user__username']
    
    # Filters available in the right sidebar of the admin panel
    list_filter = ['status', 'created_at']
