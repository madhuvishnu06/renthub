"""
Force create all database tables for the Electronic Rental Platform
Run this script if makemigrations is not detecting changes
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 60)
print("ELECTRONIC RENTAL PLATFORM - DATABASE SETUP")
print("=" * 60)

# Step 1: Delete existing database
db_path = 'db.sqlite3'
if os.path.exists(db_path):
    print(f"\n[1/5] Deleting existing database: {db_path}")
    os.remove(db_path)
    print("✓ Database deleted")
else:
    print(f"\n[1/5] No existing database found")

# Step 2: Delete all migration files
print("\n[2/5] Cleaning migration files...")
apps = ['users', 'products', 'bookings', 'payments', 'chat', 'adminpanel']
for app in apps:
    migrations_dir = os.path.join(app, 'migrations')
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(migrations_dir, file)
                os.remove(file_path)
    else:
        # Create migrations directory if it doesn't exist
        os.makedirs(migrations_dir, exist_ok=True)
        with open(os.path.join(migrations_dir, '__init__.py'), 'w') as f:
            f.write('')
        print(f"  ✓ Created {migrations_dir}")

print("✓ Migration files cleaned")

# Step 3: Create new migrations
print("\n[3/5] Creating new migrations...")
call_command('makemigrations')
print("✓ Migrations created")

# Step 4: Apply migrations
print("\n[4/5] Applying migrations...")
call_command('migrate')
print("✓ Migrations applied")

# Step 5: Create sample categories
print("\n[5/5] Creating sample product categories...")
from products.models import Category

categories = [
    {'name': 'Laptops', 'description': 'High-performance laptops for work and gaming'},
    {'name': 'Cameras', 'description': 'Professional cameras and photography equipment'},
    {'name': 'Phones', 'description': 'Latest smartphones and mobile devices'},
    {'name': 'Audio Equipment', 'description': 'Speakers, headphones, and audio gear'},
    {'name': 'Gaming Consoles', 'description': 'PlayStation, Xbox, and gaming systems'},
    {'name': 'Drones', 'description': 'Aerial photography and recreational drones'},
]

for cat_data in categories:
    try:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"  ✓ Created category: {category.name}")
        else:
            print(f"  - Category already exists: {category.name}")
    except Exception as e:
        print(f"  ! Skipped category {cat_data['name']}: {str(e)}")

print("\n" + "=" * 60)
print("DATABASE SETUP COMPLETE!")
print("=" * 60)
print("\nNext steps:")
print("1. Create superuser: python manage.py shell")
print("   Then run: from users.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='admin')")
print("2. Run server: python manage.py runserver")
print("3. Visit: http://127.0.0.1:8000/")
print("\n")
