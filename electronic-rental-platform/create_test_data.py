"""
Script to create test data for the Electronic Rental Platform
Run this after setting up the database to populate with sample data
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from users.models import User
from products.models import Product, Category
from decimal import Decimal

def create_test_data():
    print("Creating test data...")
    
    # Create categories
    categories_data = [
        'Laptop', 'Camera', 'Phone', 'Gaming Console', 
        'Drone', 'Tablet', 'Audio Equipment', 'Other'
    ]
    
    categories = {}
    for cat_name in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': cat_name.lower().replace(' ', '-')}
        )
        categories[cat_name] = cat
        if created:
            print(f"✓ Created category: {cat_name}")
    
    # Create shop owner if doesn't exist
    shop_owner, created = User.objects.get_or_create(
        username='shopowner',
        defaults={
            'email': 'shop@test.com',
            'role': 'shop_owner',
            'first_name': 'Shop',
            'last_name': 'Owner'
        }
    )
    if created:
        shop_owner.set_password('test123')
        shop_owner.save()
        print(f"✓ Created shop owner: shopowner (password: test123)")
    
    # Create customer if doesn't exist
    customer, created = User.objects.get_or_create(
        username='customer',
        defaults={
            'email': 'customer@test.com',
            'role': 'customer',
            'first_name': 'Test',
            'last_name': 'Customer'
        }
    )
    if created:
        customer.set_password('test123')
        customer.save()
        print(f"✓ Created customer: customer (password: test123)")
    
    # Create sample products
    products_data = [
        {
            'title': 'MacBook Pro 14-inch M2',
            'category': 'Laptop',
            'description': 'High-performance laptop perfect for professionals and creators. Features M2 chip, 16GB RAM, and 512GB SSD.',
            'condition': 'like_new',
            'daily_price': Decimal('50.00'),
            'weekly_price': Decimal('300.00'),
            'monthly_price': Decimal('1000.00'),
            'stock': 3
        },
        {
            'title': 'Canon EOS R5 Camera',
            'category': 'Camera',
            'description': 'Professional mirrorless camera with 45MP sensor and 8K video recording capabilities.',
            'condition': 'new',
            'daily_price': Decimal('80.00'),
            'weekly_price': Decimal('500.00'),
            'monthly_price': Decimal('1800.00'),
            'stock': 2
        },
        {
            'title': 'iPhone 15 Pro Max',
            'category': 'Phone',
            'description': 'Latest iPhone with A17 Pro chip, titanium design, and advanced camera system.',
            'condition': 'new',
            'daily_price': Decimal('30.00'),
            'weekly_price': Decimal('180.00'),
            'monthly_price': Decimal('600.00'),
            'stock': 5
        },
        {
            'title': 'Sony PlayStation 5',
            'category': 'Gaming Console',
            'description': 'Next-gen gaming console with 4K graphics and exclusive games library.',
            'condition': 'like_new',
            'daily_price': Decimal('20.00'),
            'weekly_price': Decimal('120.00'),
            'monthly_price': Decimal('400.00'),
            'stock': 4
        },
        {
            'title': 'DJI Mavic 3 Pro Drone',
            'category': 'Drone',
            'description': 'Professional drone with Hasselblad camera and 46 minutes flight time.',
            'condition': 'good',
            'daily_price': Decimal('60.00'),
            'weekly_price': Decimal('350.00'),
            'monthly_price': Decimal('1200.00'),
            'stock': 2
        },
    ]
    
    for product_data in products_data:
        category_name = product_data.pop('category')
        product, created = Product.objects.get_or_create(
            title=product_data['title'],
            defaults={
                **product_data,
                'category': categories[category_name],
                'owner': shop_owner,
                'is_available': True
            }
        )
        if created:
            print(f"✓ Created product: {product.title}")
    
    print("\n" + "="*50)
    print("Test data creation complete!")
    print("="*50)
    print("\nTest Accounts:")
    print("-" * 50)
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  URL: http://127.0.0.1:8000/admin/")
    print("\nShop Owner:")
    print("  Username: shopowner")
    print("  Password: test123")
    print("  URL: http://127.0.0.1:8000/login/")
    print("\nCustomer:")
    print("  Username: customer")
    print("  Password: test123")
    print("  URL: http://127.0.0.1:8000/login/")
    print("-" * 50)
    print(f"\nTotal Products: {Product.objects.count()}")
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Users: {User.objects.count()}")
    print("\nNext Steps:")
    print("1. Login as customer and browse products")
    print("2. Click 'Book Now' on any product")
    print("3. Select dates and proceed to payment")
    print("4. Check admin panel to see all data")

if __name__ == '__main__':
    create_test_data()
