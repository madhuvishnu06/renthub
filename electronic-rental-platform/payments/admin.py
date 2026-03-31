from django.contrib import admin
from .models import Payment, PaymentQRCode

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'booking', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['booking__customer__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(PaymentQRCode)
class PaymentQRCodeAdmin(admin.ModelAdmin):
    list_display = ['shop_owner', 'is_active', 'created_at']
    list_filter = ['is_active']
