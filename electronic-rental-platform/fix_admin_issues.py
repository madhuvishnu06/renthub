import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product
from django.db import connection

User = get_user_model()

def fix_admin_issues():
    print("\n" + "="*60)
    print("FIXING ADMIN PANEL ISSUES")
    print("="*60 + "\n")
    
    # 1. Check if tables exist
    print("1. Checking database tables...")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"   Found {len(tables)} tables")
        
        required_tables = ['users_user', 'products_product', 'products_category', 'bookings_booking', 'payments_payment']
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"   ⚠ Missing tables: {missing_tables}")
            print("   Run: python manage.py migrate")
            return
        else:
            print("   ✓ All required tables exist")
    
    # 2. Ensure superuser exists
    print("\n2. Checking for superuser...")
    superusers = User.objects.filter(is_superuser=True)
    if superusers.exists():
        print(f"   ✓ Found {superusers.count()} superuser(s)")
        for su in superusers:
            print(f"     - {su.username} ({su.email})")
    else:
        print("   ⚠ No superuser found!")
        print("   Creating superuser 'admin'...")
        try:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            print("   ✓ Superuser created successfully")
            print("     Username: admin")
            print("     Password: admin123")
        except Exception as e:
            print(f"   ✗ Error creating superuser: {e}")
    
    # 3. Ensure categories exist
    print("\n3. Checking categories...")
    category_count = Category.objects.count()
    if category_count == 0:
        print("   ⚠ No categories found. Creating default categories...")
        categories = ['Laptop', 'Camera', 'Phone', 'Gaming Console', 'Drone', 'Tablet', 'Audio Equipment', 'Other']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        print(f"   ✓ Created {len(categories)} categories")
    else:
        print(f"   ✓ Found {category_count} categories")
    
    # 4. Check for test data
    print("\n4. Checking for test data...")
    product_count = Product.objects.count()
    user_count = User.objects.count()
    print(f"   Users: {user_count}")
    print(f"   Products: {product_count}")
    
    if product_count == 0:
        print("\n   ℹ To add test products:")
        print("   - Login to admin panel: http://127.0.0.1:8000/admin/")
        print("   - Or run: python create_test_data.py")
    
    print("\n" + "="*60)
    print("FIX COMPLETE")
    print("="*60)
    print("\nNext steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Visit admin panel: http://127.0.0.1:8000/admin/")
    print("3. Login with username: admin, password: admin123")
    print("4. Try adding a product to test if data saves correctly")
    print("\n")

if __name__ == "__main__":
    try:
        fix_admin_issues()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
