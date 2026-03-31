# Quick Fix Guide - Database Setup Issues

If you're seeing "No changes detected" or "no such table" errors, follow these steps:

## Option 1: Automated Fix (Recommended)

1. Open Command Prompt in the project directory
2. Activate virtual environment:
   \`\`\`
   venv\Scripts\activate
   \`\`\`
3. Run the fix script:
   \`\`\`
   python force_migrations.py
   \`\`\`
4. Create superuser:
   \`\`\`
   python manage.py createsuperuser
   \`\`\`
5. Start server:
   \`\`\`
   python manage.py runserver
   \`\`\`

## Option 2: Using Batch File

1. Open Command Prompt
2. Run:
   \`\`\`
   quick_fix.bat
   \`\`\`
3. Follow the prompts

## What This Does

The `force_migrations.py` script:
- Deletes the existing database (db.sqlite3)
- Cleans all old migration files
- Creates migration folders if missing
- Generates fresh migrations for all apps
- Applies all migrations to create tables
- Creates sample product categories

## After Running

You should be able to:
- Sign up as Customer or Shop Owner
- Login to the platform
- Browse products by category
- Create bookings
- Use chat messaging
- Access admin panel at `/admin/`

## Still Having Issues?

Make sure:
1. You're in the project root directory
2. Virtual environment is activated (you see `(venv)` in terminal)
3. All required packages are installed: `pip install -r requirements.txt`
4. You have write permissions in the project folder
