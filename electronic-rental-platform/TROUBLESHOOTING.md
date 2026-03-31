# Troubleshooting Guide - Electronic Rental Platform

## Database Errors (OperationalError: no such table)

If you see errors like "no such table: products_category" or similar, it means the database tables haven't been created yet.

### Solution:

**Windows (Command Prompt):**
\`\`\`cmd
cd C:\Users\HP\Downloads\electronic-rental-platform
venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
\`\`\`

**Or use the automated script:**
\`\`\`cmd
fix_database.bat
\`\`\`

**Linux/Mac:**
\`\`\`bash
cd /path/to/electronic-rental-platform
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
\`\`\`

**Or use the automated script:**
\`\`\`bash
chmod +x fix_database.sh
./fix_database.sh
\`\`\`

## Common Issues

### 1. "no such table" errors on multiple pages
**Cause:** Migrations haven't been run
**Fix:** Run `python manage.py migrate`

### 2. Sign up/Login not working
**Cause:** users_customuser table doesn't exist
**Fix:** Run `python manage.py makemigrations users` then `python manage.py migrate`

### 3. Products page error
**Cause:** products_category and products_product tables don't exist
**Fix:** Run `python manage.py makemigrations products` then `python manage.py migrate`

### 4. Bookings not working
**Cause:** bookings_booking table doesn't exist
**Fix:** Run `python manage.py makemigrations bookings` then `python manage.py migrate`

### 5. Chat/Messaging errors
**Cause:** chat_conversation and chat_message tables don't exist
**Fix:** Run `python manage.py makemigrations chat` then `python manage.py migrate`

### 6. Admin panel errors
**Cause:** adminpanel tables don't exist
**Fix:** Run `python manage.py makemigrations adminpanel` then `python manage.py migrate`

## Complete Fresh Setup

If nothing works, start fresh:

\`\`\`cmd
# Delete the database
del db.sqlite3

# Delete all migration files (except __init__.py)
# In each app folder: users/migrations/, products/migrations/, etc.

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
\`\`\`

## Verification

After running migrations, verify tables exist:

\`\`\`cmd
python manage.py dbshell
.tables
.quit
\`\`\`

You should see tables like:
- auth_user
- users_customuser
- products_category
- products_product
- bookings_booking
- payments_payment
- chat_conversation
- chat_message

## Need Help?

If you still face issues:
1. Check Python version: `python --version` (should be 3.8+)
2. Check Django version: `python -m django --version` (should be 4.2+)
3. Make sure you're in the correct directory
4. Make sure virtual environment is activated (you should see `(venv)` in prompt)
