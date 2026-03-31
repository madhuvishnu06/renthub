#!/usr/bin/env python
"""
Database Setup Script for Electronic Rental Platform
This script will create all necessary migrations and set up the database
"""

import os
import sys
import django

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental_platform.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def setup_database():
    """Create all migrations and apply them"""
    
    print("=" * 60)
    print("ELECTRONIC RENTAL PLATFORM - DATABASE SETUP")
    print("=" * 60)
    print()
    
    # List of apps to migrate
    apps = ['users', 'products', 'bookings', 'payments', 'chat', 'adminpanel']
    
    print("Step 1: Creating migrations for all apps...")
    print("-" * 60)
    
    for app in apps:
        try:
            print(f"Creating migrations for {app}...")
            call_command('makemigrations', app, interactive=False)
        except Exception as e:
            print(f"Warning: {app} - {str(e)}")
    
    print()
    print("Step 2: Applying all migrations...")
    print("-" * 60)
    
    try:
        call_command('migrate', interactive=False)
        print("All migrations applied successfully!")
    except Exception as e:
        print(f"Error applying migrations: {str(e)}")
        return False
    
    print()
    print("Step 3: Verifying database tables...")
    print("-" * 60)
    
    # Get list of tables
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Total tables created: {len(tables)}")
        for table in tables:
            print(f"  ✓ {table[0]}")
    
    print()
    print("=" * 60)
    print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Create superuser: python manage.py createsuperuser")
    print("2. Run server: python manage.py runserver")
    print("3. Access at: http://127.0.0.1:8000/")
    print()
    
    return True

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
