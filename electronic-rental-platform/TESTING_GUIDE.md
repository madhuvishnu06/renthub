# Testing Guide for Electronic Rental Platform

## Step 1: Start the Server

\`\`\`cmd
venv\Scripts\activate
python manage.py runserver
\`\`\`

## Step 2: Test Payment Flow

### Create Test Accounts

1. **Admin Account** (Already exists)
   - Username: `admin`
   - Password: `admin123`
   - URL: `http://127.0.0.1:8000/admin/`

2. **Create Shop Owner Account**
   - Go to: `http://127.0.0.1:8000/signup/`
   - Username: `shopowner`
   - Email: `shop@test.com`
   - Password: `test123`
   - Role: **Shop Owner**

3. **Create Customer Account**
   - Go to: `http://127.0.0.1:8000/signup/`
   - Username: `customer`
   - Email: `customer@test.com`
   - Password: `test123`
   - Role: **Customer**

### Add Products as Shop Owner

1. Login as shop owner
2. Go to: `http://127.0.0.1:8000/products/create/`
3. Fill in product details:
   - Title: "MacBook Pro"
   - Category: Laptop
   - Description: "High-performance laptop"
   - Condition: Like New
   - Daily Rate: 50
   - Weekly Rate: 300
   - Monthly Rate: 1000
   - Stock: 5
   - Check "Available"
4. Upload product images (optional)
5. Click "Add Product"

### Test Booking Flow as Customer

1. **Logout and login as customer**
2. **Browse products**: `http://127.0.0.1:8000/products/`
3. **Click on a product** to view details
4. **Click "Book Now"** button
5. **Fill booking form**:
   - Start Date: Today or future date
   - End Date: At least 1 day after start date
   - Rental Period: Select Daily/Weekly/Monthly
   - Notes: Optional
6. **Watch the browser console** (F12 → Console tab) for debug messages:
   - Should see: `[v0] Form submitting...`
7. **Watch VS Code terminal** for server debug messages:
   - Should see: `[v0] Form submitted for booking creation`
   - Should see: `[v0] Booking saved successfully with ID: X`
   - Should see: `[v0] Redirecting to payment`

### Test Payment

1. After booking creation, you should be redirected to: `http://127.0.0.1:8000/payments/process/<booking_id>/`
2. The payment page shows:
   - Booking details
   - Total amount
   - Payment method options
3. **To make a mock payment**:
   - Select payment method (Razorpay/Stripe/Card)
   - Click "Pay Now" button
   - Should redirect to success page
4. **Or upload payment screenshot**:
   - Upload an image file
   - Enter transaction ID
   - Click "Submit Payment Proof"

## Step 3: Check Admin Panel

1. **Login to admin**: `http://127.0.0.1:8000/admin/`
   - Username: `admin`
   - Password: `admin123`

2. **Check if data appears**:
   - Click "Users" - should see all registered users
   - Click "Products" → "Products" - should see added products
   - Click "Bookings" - should see created bookings
   - Click "Payments" - should see payment records
   - Click "Chat" → "Conversations" - should see chat messages (if any)

3. **If data doesn't appear**:
   - Check VS Code terminal for errors
   - Run: `python manage.py migrate` to ensure database is updated
   - Restart server

## Troubleshooting

### Payment Page Doesn't Open

**Check browser console (F12)**:
- Look for JavaScript errors
- Should see `[v0] Form submitting...` when clicking "Proceed to Payment"

**Check VS Code terminal**:
- Should see `[v0] Form submitted for booking creation`
- If you see `[v0] Form validation failed`, check the error messages
- If you see `[v0] Error saving booking`, there's a database issue

**Common issues**:
1. **Date validation error**: Start date must be today or future, end date must be after start date
2. **Missing rental period**: Make sure to select Daily/Weekly/Monthly
3. **Database error**: Run `python manage.py migrate` again

### Admin Panel Shows No Data

1. **Make sure you created data first**:
   - Add products as shop owner
   - Create bookings as customer
   - Make payments

2. **Check if models are registered**:
   - All models should appear in the admin sidebar
   - If not, run `python manage.py migrate` and restart server

3. **Check database file exists**:
   - Look for `db.sqlite3` in your project folder
   - If missing, run `python force_migrations.py` to recreate it

## Debug Commands

\`\`\`cmd
# Check for migration issues
python manage.py showmigrations

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create test data
python manage.py shell
>>> from products.models import Product, Category
>>> Category.objects.all()  # Should show categories
>>> Product.objects.all()   # Should show products
\`\`\`

## Expected Terminal Output

When booking works correctly, you should see:

\`\`\`
[v0] Form submitted for booking creation
[v0] POST data: <QueryDict: {'csrfmiddlewaretoken': [...], 'start_date': ['2025-11-28'], 'end_date': ['2025-11-30'], 'rental_period': ['daily'], 'notes': ['']}>
[v0] Form is valid, creating booking
[v0] Duration: 3 days
[v0] Daily price: 50.00, Weekly: 300.00, Monthly: 1000.00
[v0] Calculated total price: 150.00
[v0] Booking saved successfully with ID: 1
[v0] Payment process accessed for booking ID: 1
[v0] Booking found: MacBook Pro, Total: $150.00
[v0] Rendering payment page
