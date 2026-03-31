from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'product', 'start_date', 'end_date', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'rental_period', 'created_at']
    search_fields = ['customer__username', 'product__title']
    readonly_fields = ['created_at', 'updated_at']
