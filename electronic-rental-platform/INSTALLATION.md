# Installation Guide - Electronic Rental Platform

This guide will help you set up and run the Electronic Rental Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** (optional) - For cloning the repository

### Verify Python Installation

Open your terminal/command prompt and run:
\`\`\`bash
python --version
# or
python3 --version
\`\`\`

You should see Python 3.8 or higher.

## Quick Setup (Automated)

### For Windows Users:
1. Double-click `setup.bat`
2. Follow the on-screen prompts
3. Wait for installation to complete

### For macOS/Linux Users:
1. Open terminal in project directory
2. Make the script executable: `chmod +x setup.sh`
3. Run the script: `./setup.sh`
4. Follow the on-screen prompts

## Manual Setup (Step-by-Step)

### Step 1: Extract Project Files

Extract the downloaded ZIP file to your desired location.

### Step 2: Open Terminal/Command Prompt

Navigate to the project directory:
\`\`\`bash
cd path/to/rental_platform
\`\`\`

### Step 3: Create Virtual Environment

**Windows:**
\`\`\`bash
python -m venv venv
\`\`\`

**macOS/Linux:**
\`\`\`bash
python3 -m venv venv
\`\`\`

### Step 4: Activate Virtual Environment

**Windows:**
\`\`\`bash
venv\Scripts\activate
\`\`\`

**macOS/Linux:**
\`\`\`bash
source venv/bin/activate
\`\`\`

You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

This will install:
- Django 4.2+
- Pillow (for image handling)
- qrcode (for QR code generation)
- python-dateutil (for date handling)

### Step 6: Create Media Directories

**Windows:**
\`\`\`bash
mkdir media\products
mkdir media\payments
mkdir media\qrcodes
\`\`\`

**macOS/Linux:**
\`\`\`bash
mkdir -p media/products
mkdir -p media/payments
mkdir -p media/qrcodes
\`\`\`

### Step 7: Run Database Migrations

\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

This creates all necessary database tables.

### Step 8: Create Superuser (Admin Account)

\`\`\`bash
python manage.py createsuperuser
\`\`\`

You'll be prompted to enter:
- Username
- Email address
- Password (enter twice)

**Note:** Save these credentials - you'll need them to access the admin panel.

### Step 9: Start Development Server

\`\`\`bash
python manage.py runserver
\`\`\`

You should see output like:
\`\`\`
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
\`\`\`

### Step 10: Access the Application

Open your web browser and navigate to:

- **Main Website:** `http://127.0.0.1:8000/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`
- **Screenshots/Docs:** `http://127.0.0.1:8000/screenshots/`

## Post-Installation Setup

### 1. Login to Admin Panel

1. Go to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. You can manage users, products, and categories from here

### 2. Create Initial Categories

1. In admin panel, go to "Products" → "Categories"
2. Add categories like:
   - Laptops
   - Cameras
   - Mobile Phones
   - Gaming Consoles
   - TVs & Monitors
   - Audio Equipment

### 3. Create Test Users

**Option A: Through Admin Panel**
1. Go to "Users" section
2. Click "Add User"
3. Choose role (Customer or Shop Owner)
4. Fill in required details

**Option B: Through Website**
1. Go to `http://127.0.0.1:8000/users/signup/`
2. Fill in the registration form
3. Select role (Customer or Shop Owner)

### 4. Add Sample Products (as Shop Owner)

1. Login as a shop owner
2. Go to "Add Product"
3. Fill in product details
4. Upload product images
5. Set pricing and availability

## Using the Platform

### As a Customer:
1. **Browse Products:** Visit homepage to see all available electronics
2. **Search/Filter:** Use search bar and filters to find specific items
3. **Book Rental:** Click product → Select dates → Book Now
4. **Make Payment:** Complete mock payment or upload screenshot
5. **Leave Review:** After rental completion, rate and review
6. **Chat:** Message shop owners for inquiries

### As a Shop Owner:
1. **Add Products:** Dashboard → Add Electronics
2. **Manage Inventory:** Edit/delete products, update stock
3. **Handle Bookings:** View and manage rental requests
4. **Upload QR Code:** Add payment QR code for customers
5. **Track Earnings:** View analytics in dashboard
6. **Respond to Messages:** Chat with customers

### As an Admin:
1. **Access Admin Panel:** `http://127.0.0.1:8000/admin/`
2. **Manage Users:** Activate/deactivate accounts, change roles
3. **Manage Products:** Oversee all listings
4. **Manage Categories:** Add/edit/delete categories
5. **View Analytics:** Monitor platform activity

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
\`\`\`bash
# Make sure virtual environment is activated
pip install -r requirements.txt
\`\`\`

### Issue: Port 8000 already in use

**Solution:**
\`\`\`bash
# Use a different port
python manage.py runserver 8080
\`\`\`

Then access at `http://127.0.0.1:8080/`

### Issue: Static files not loading

**Solution:**
\`\`\`bash
python manage.py collectstatic
\`\`\`

### Issue: Database errors

**Solution:**
\`\`\`bash
# Delete db.sqlite3 file
# Delete all migration files in */migrations/ (except __init__.py)
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
\`\`\`

### Issue: Images not uploading

**Solution:**
- Check that media directories exist
- Verify file permissions (macOS/Linux)
- Ensure Pillow is installed: `pip install Pillow`

### Issue: Cannot create superuser

**Solution:**
- Make sure migrations are complete
- Try: `python manage.py migrate --run-syncdb`
- Then retry: `python manage.py createsuperuser`

## Configuration Options

### Change Database (Production)

Edit `rental_platform/settings.py`:

\`\`\`python
# For PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
\`\`\`

### Enable Real Email (Optional)

Edit `rental_platform/settings.py`:

\`\`\`python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
\`\`\`

### Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Set up static file serving (WhiteNoise or CDN)
5. Configure media file storage (AWS S3, etc.)
6. Enable HTTPS
7. Set strong `SECRET_KEY`
8. Use environment variables for sensitive data

## Development Tips

### Activate Virtual Environment (Every Session)

**Windows:**
\`\`\`bash
venv\Scripts\activate
\`\`\`

**macOS/Linux:**
\`\`\`bash
source venv/bin/activate
\`\`\`

### Deactivate Virtual Environment

\`\`\`bash
deactivate
\`\`\`

### View Server Logs

Server logs appear in the terminal where you ran `runserver`.

### Create Database Backup

\`\`\`bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
\`\`\`

## Next Steps

1. **Explore Features:** Test all functionality
2. **Customize Design:** Edit CSS in `static/css/style.css`
3. **Add More Categories:** Expand product categories
4. **Configure Payments:** Integrate real payment gateway
5. **Deploy Online:** Host on Heroku, PythonAnywhere, or AWS

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review Django documentation
3. Check application logs in terminal
4. Verify all dependencies are installed

## Summary of Commands

\`\`\`bash
# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Access
http://127.0.0.1:8000/
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/screenshots/
\`\`\`

---

**Congratulations!** Your Electronic Rental Platform is now ready to use. Happy coding!
