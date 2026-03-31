"""
Script to verify payment system is working correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from payments.models import Payment, PaymentQRCode
from bookings.models import Booking
from products.models import Product
from users.models import User

print("=" * 50)
print("Payment System Check")
print("=" * 50)

# Check if payment models are working
print("\n1. Checking Payment model...")
try:
    payment_count = Payment.objects.count()
    print(f"   ✓ Payment model working. Total payments: {payment_count}")
except Exception as e:
    print(f"   ✗ Error with Payment model: {e}")

print("\n2. Checking PaymentQRCode model...")
try:
    qr_count = PaymentQRCode.objects.count()
    print(f"   ✓ PaymentQRCode model working. Total QR codes: {qr_count}")
except Exception as e:
    print(f"   ✗ Error with PaymentQRCode model: {e}")

print("\n3. Checking Booking-Payment relationship...")
try:
    bookings = Booking.objects.all()
    bookings_with_payment = sum(1 for b in bookings if hasattr(b, 'payment'))
    print(f"   ✓ Relationship working. Bookings with payment: {bookings_with_payment}/{bookings.count()}")
except Exception as e:
    print(f"   ✗ Error checking relationship: {e}")

print("\n4. Checking Shop Owner QR Code access...")
try:
    shop_owners = User.objects.filter(role='shop_owner')
    shop_owners_with_qr = sum(1 for owner in shop_owners if hasattr(owner, 'payment_qr'))
    print(f"   ✓ QR Code access working. Shop owners with QR: {shop_owners_with_qr}/{shop_owners.count()}")
except Exception as e:
    print(f"   ✗ Error checking QR access: {e}")

print("\n5. Testing payment flow URLs...")
try:
    from django.urls import reverse
    
    # Check if URLs are configured
    reverse('payments:list')
    reverse('payments:qr_code')
    print("   ✓ Payment URLs configured correctly")
except Exception as e:
    print(f"   ✗ Error with payment URLs: {e}")

print("\n" + "=" * 50)
print("Payment System Check Complete!")
print("=" * 50)

# Create a test booking if none exist
if Booking.objects.count() == 0:
    print("\nNo bookings found. To test payments:")
    print("1. Login as a customer")
    print("2. Browse products at /products/")
    print("3. Click 'Book Now' on any product")
    print("4. Select dates and create booking")
    print("5. You'll be redirected to payment page")
else:
    print(f"\nYou have {Booking.objects.count()} booking(s).")
    pending_bookings = Booking.objects.filter(status='pending').count()
    if pending_bookings > 0:
        print(f"   {pending_bookings} booking(s) waiting for payment")
