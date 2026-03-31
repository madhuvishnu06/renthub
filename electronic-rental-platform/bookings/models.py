from django.db import models
from users.models import User
from products.models import Product
from datetime import datetime

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Shop Owner Approval'),
        ('awaiting_payment', 'Awaiting Payment'),
        ('payment_submitted', 'Payment Submitted - Awaiting Verification'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    RENTAL_PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    rental_period = models.CharField(max_length=20, choices=RENTAL_PERIOD_CHOICES, default='daily')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    shop_owner_notes = models.TextField(blank=True, null=True, help_text="Shop owner's response to the booking request")
    shop_owner_approved_at = models.DateTimeField(blank=True, null=True)
    payment_verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Booking #{self.pk} - {self.product.title} by {self.customer.username}"
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    @property
    def shop_owner(self):
        return self.product.owner
    
    class Meta:
        ordering = ['-created_at']
