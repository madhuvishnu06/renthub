from django.db import models
from bookings.models import Booking
from users.models import User

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('submitted', 'Submitted - Awaiting Verification'),
        ('verified', 'Verified by Shop Owner'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('qr_code', 'QR Code'),
        ('screenshot', 'Screenshot Upload'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', help_text="Payment proof screenshot (Required)")
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    card_type = models.CharField(max_length=20, blank=True, null=True)
    payment_details = models.TextField(blank=True, null=True, help_text="Additional payment information")
    notes = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    verified_at = models.DateTimeField(blank=True, null=True)
    verification_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment #{self.pk} - Booking #{self.booking.pk} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']

class PaymentQRCode(models.Model):
    shop_owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_qr')
    qr_code_image = models.ImageField(upload_to='qr_codes/')
    payment_details = models.TextField(help_text="Payment instructions (UPI ID, Account number, etc.)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"QR Code for {self.shop_owner.username}"
