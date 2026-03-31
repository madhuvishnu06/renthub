from django.db import models
from users.models import User
from bookings.models import Booking

class ReturnRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    RETURN_REASON_CHOICES = (
        ('damaged', 'Product Damaged'),
        ('defective', 'Product Defective'),
        ('not_as_described', 'Not As Described'),
        ('lost', 'Product Lost'),
        ('other', 'Other Reason'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='return_request')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_requests')
    shop_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_returns')
    reason = models.CharField(max_length=50, choices=RETURN_REASON_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shop_owner_response = models.TextField(blank=True, null=True)
    proof_image = models.ImageField(upload_to='return_proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Return Request #{self.pk} - {self.booking.product.title}"
    
    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('return_request', 'New Return Request'),
        ('return_approved', 'Return Approved'),
        ('return_rejected', 'Return Rejected'),
        ('return_completed', 'Return Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    return_request = models.ForeignKey(ReturnRequest, on_delete=models.CASCADE, related_name='notifications', blank=True, null=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_notification_type_display()} for {self.user.username}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    class Meta:
        ordering = ['-created_at']
