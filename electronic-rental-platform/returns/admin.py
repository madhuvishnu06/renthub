from django.contrib import admin
from .models import ReturnRequest, Notification


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'customer', 'shop_owner', 'reason', 'status', 'created_at')
    list_filter = ('status', 'reason', 'created_at')
    search_fields = ('customer__username', 'shop_owner__username', 'booking__product__title')
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')
    fieldsets = (
        ('Return Information', {
            'fields': ('booking', 'customer', 'shop_owner')
        }),
        ('Details', {
            'fields': ('reason', 'description', 'proof_image', 'status')
        }),
        ('Review', {
            'fields': ('shop_owner_response', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User & Type', {
            'fields': ('user', 'notification_type')
        }),
        ('Content', {
            'fields': ('title', 'message', 'return_request')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
