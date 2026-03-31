import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product, ProductImage, Review
from bookings.models import Booking
from payments.models import Payment, PaymentQRCode
from chat.models import Conversation, Message

User = get_user_model()

def diagnose_database():
    print("\n" + "="*60)
    print("DATABASE DIAGNOSTIC REPORT")
    print("="*60 + "\n")
    
    # Check Users
    print("1. USERS:")
    user_count = User.objects.count()
    print(f"   Total Users: {user_count}")
    if user_count > 0:
        print(f"   - Customers: {User.objects.filter(role='customer').count()}")
        print(f"   - Shop Owners: {User.objects.filter(role='shop_owner').count()}")
        print(f"   - Admins: {User.objects.filter(role='admin').count()}")
        print(f"   Sample users: {list(User.objects.all().values_list('username', 'role')[:3])}")
    else:
        print("   ⚠ No users found!")
    
    # Check Categories
    print("\n2. CATEGORIES:")
    category_count = Category.objects.count()
    print(f"   Total Categories: {category_count}")
    if category_count > 0:
        print(f"   Categories: {list(Category.objects.values_list('name', flat=True))}")
    else:
        print("   ⚠ No categories found!")
    
    # Check Products
    print("\n3. PRODUCTS:")
    product_count = Product.objects.count()
    print(f"   Total Products: {product_count}")
    if product_count > 0:
        print(f"   Sample products: {list(Product.objects.all().values_list('title', 'owner__username')[:5])}")
    else:
        print("   ⚠ No products found!")
    
    # Check Bookings
    print("\n4. BOOKINGS:")
    booking_count = Booking.objects.count()
    print(f"   Total Bookings: {booking_count}")
    if booking_count > 0:
        print(f"   - Pending: {Booking.objects.filter(status='pending').count()}")
        print(f"   - Approved: {Booking.objects.filter(status='approved').count()}")
        print(f"   - Confirmed: {Booking.objects.filter(status='confirmed').count()}")
        print(f"   - Completed: {Booking.objects.filter(status='completed').count()}")
    else:
        print("   ⚠ No bookings found!")
    
    # Check Payments
    print("\n5. PAYMENTS:")
    payment_count = Payment.objects.count()
    print(f"   Total Payments: {payment_count}")
    if payment_count > 0:
        print(f"   - Completed: {Payment.objects.filter(status='completed').count()}")
        print(f"   - Pending: {Payment.objects.filter(status='pending').count()}")
        print(f"   - Failed: {Payment.objects.filter(status='failed').count()}")
    else:
        print("   ⚠ No payments found!")
    
    # Check Conversations
    print("\n6. CHAT:")
    conversation_count = Conversation.objects.count()
    message_count = Message.objects.count()
    print(f"   Total Conversations: {conversation_count}")
    print(f"   Total Messages: {message_count}")
    
    # Database file check
    print("\n7. DATABASE FILE:")
    db_path = "db.sqlite3"
    if os.path.exists(db_path):
        size = os.path.getsize(db_path) / 1024  # KB
        print(f"   ✓ Database file exists: {db_path}")
        print(f"   Size: {size:.2f} KB")
    else:
        print(f"   ✗ Database file not found!")
    
    print("\n" + "="*60)
    print("DIAGNOSIS COMPLETE")
    print("="*60 + "\n")
    
    # Recommendations
    if user_count == 0:
        print("⚠ ISSUE: No users in database")
        print("   FIX: Run 'python manage.py createsuperuser' to create admin user\n")
    
    if category_count == 0:
        print("⚠ ISSUE: No categories in database")
        print("   FIX: Run 'python create_test_data.py' to populate categories\n")
    
    if product_count == 0:
        print("⚠ ISSUE: No products in database")
        print("   FIX: Login as shop owner and add products, or run test data script\n")

if __name__ == "__main__":
    try:
        diagnose_database()
    except Exception as e:
        print(f"ERROR during diagnosis: {e}")
        import traceback
        traceback.print_exc()
