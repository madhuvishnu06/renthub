# Electronic Rental Platform

A comprehensive Django-based platform for renting electronic devices like laptops, cameras, phones, and other electronics. The platform connects customers with shop owners and provides a complete rental management system.

## Features

### Multi-Role System
- **Customers**: Browse products, make bookings, chat with shop owners, write reviews
- **Shop Owners**: Manage products, handle rental requests, track earnings, communicate with customers
- **Admin**: Oversee entire platform, manage users, products, bookings, and categories

### Core Functionality
- **Product Management**: Full CRUD operations with multiple images, categories, and specifications
- **Booking System**: Interactive date selection with automatic price calculation (daily/weekly/monthly rates)
- **Payment Integration**: Mock payment gateway with QR code support and screenshot upload
- **Chat System**: Real-time messaging between customers and shop owners
- **Reviews & Ratings**: 5-star rating system with detailed reviews
- **Invoice Generation**: Automatic invoice creation for bookings
- **Advanced Search**: Filter by category, condition, price range, and search by keywords

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or extract the project**
   \`\`\`bash
   cd electronic-rental-platform
   \`\`\`

2. **Create a virtual environment**
   \`\`\`bash
   python -m venv venv
   \`\`\`

3. **Activate the virtual environment**
   - On Windows:
     \`\`\`bash
     venv\Scripts\activate
     \`\`\`
   - On macOS/Linux:
     \`\`\`bash
     source venv/bin/activate
     \`\`\`

4. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

5. **Run migrations**
   \`\`\`bash
   python manage.py makemigrations
   python manage.py migrate
   \`\`\`

6. **Create a superuser (admin account)**
   \`\`\`bash
   python manage.py createsuperuser
   \`\`\`
   Follow the prompts to set username, email, and password.

7. **Create media directories**
   \`\`\`bash
   mkdir -p media/products media/qrcodes media/payment_screenshots
   \`\`\`

8. **Run the development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Custom Admin Dashboard: http://127.0.0.1:8000/adminpanel/

## User Roles Setup

### Creating User Accounts

1. **Customer Account**
   - Go to http://127.0.0.1:8000/signup/
   - Select "Customer" as user type
   - Fill in required details and register

2. **Shop Owner Account**
   - Go to http://127.0.0.1:8000/signup/
   - Select "Shop Owner" as user type
   - Fill in required details and register

3. **Admin Account**
   - Created via `createsuperuser` command (see step 6 above)
   - Can also be created through Django admin

## Usage Guide

### For Customers

1. **Browse Products**
   - View all available electronics on the homepage
   - Use filters to narrow down by category, condition, or price
   - Search for specific products

2. **Make a Booking**
   - Click on a product to view details
   - Select rental dates using the date picker
   - Review calculated price and confirm booking
   - Proceed to payment

3. **Payment**
   - Choose payment method (Card/UPI/QR Code)
   - Upload payment screenshot if using QR code
   - Receive booking confirmation

4. **Manage Bookings**
   - View all bookings in your dashboard
   - Check booking status (Pending/Confirmed/Completed/Cancelled)
   - Download invoices

5. **Communication**
   - Chat with shop owners about products
   - View message history in inbox

6. **Reviews**
   - Rate and review products after rental completion
   - Edit or delete your reviews

### For Shop Owners

1. **Add Products**
   - Access "My Products" from dashboard
   - Click "Add New Product"
   - Fill in product details, pricing, and upload images
   - Set daily, weekly, and monthly rental rates

2. **Manage Products**
   - View all your products
   - Edit product details and availability
   - Delete products
   - Track product ratings

3. **Handle Bookings**
   - View rental requests in dashboard
   - Confirm or reject bookings
   - Track booking status and earnings

4. **Customer Communication**
   - Respond to customer inquiries via chat
   - Manage conversations in inbox

5. **QR Code Setup**
   - Upload payment QR code for easy customer payments
   - Manage payment methods

### For Admins

1. **User Management**
   - View all users (customers and shop owners)
   - Activate/deactivate user accounts
   - Monitor user activity

2. **Product Oversight**
   - View all products on the platform
   - Remove inappropriate listings
   - Monitor product quality

3. **Booking Management**
   - Track all bookings across the platform
   - View revenue statistics
   - Handle disputes

4. **Category Management**
   - Add new product categories
   - Edit existing categories
   - Organize product taxonomy

5. **Platform Analytics**
   - View total users, products, and bookings
   - Monitor platform growth
   - Track revenue

## Project Structure

\`\`\`
electronic-rental-platform/
├── rental_platform/          # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── users/                    # User management app
│   ├── models.py            # Custom User model
│   ├── views.py             # Authentication views
│   └── forms.py             # User forms
├── products/                 # Products/Electronics app
│   ├── models.py            # Product, ProductImage, Review models
│   ├── views.py             # Product CRUD views
│   └── forms.py             # Product forms
├── bookings/                 # Booking management app
│   ├── models.py            # Booking model
│   ├── views.py             # Booking views
│   └── forms.py             # Booking forms
├── payments/                 # Payment processing app
│   ├── models.py            # Payment, QRCode models
│   ├── views.py             # Payment views
│   └── forms.py             # Payment forms
├── chat/                     # Messaging system app
│   ├── models.py            # Conversation, Message models
│   └── views.py             # Chat views
├── adminpanel/              # Custom admin dashboard
│   └── views.py             # Admin views
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # User uploads
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
\`\`\`

## Default Credentials

After running `createsuperuser`, use those credentials to log in as admin.

For testing, create sample users:
- Customer: Use signup form with "Customer" role
- Shop Owner: Use signup form with "Shop Owner" role

## Features in Detail

### Product Categories
- Laptops
- Cameras
- Phones
- Gaming Consoles
- Audio Equipment
- Other Electronics

### Product Conditions
- New
- Like New
- Good
- Fair

### Booking Status Flow
1. Pending (Initial state after customer books)
2. Confirmed (Shop owner accepts)
3. Completed (Rental period finished)
4. Cancelled (Either party cancels)

### Payment Status
- Pending
- Completed
- Failed

## Technologies Used

- **Backend**: Django 4.2
- **Database**: SQLite (development) - easily upgradeable to PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: Pillow
- **QR Codes**: qrcode library
- **Date Handling**: python-dateutil

## Future Enhancements

- Real-time chat with WebSockets
- Email notifications
- SMS alerts
- Advanced analytics dashboard
- Mobile app integration
- Payment gateway integration (Stripe/Razorpay)
- Delivery tracking
- Insurance options
- Multi-language support

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **Database Errors**
   - Delete `db.sqlite3` and migrations
   - Run `python manage.py makemigrations` and `python manage.py migrate`

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_URL and STATIC_ROOT in settings.py

4. **Permission Errors**
   - Ensure media/ directory has write permissions
   - Check file upload size limits

## Support

For issues or questions:
1. Check the documentation above
2. Review Django documentation: https://docs.djangoproject.com/
3. Check project issues on GitHub (if applicable)

## License

This project is for educational purposes.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Happy Renting!** 🎉
\`\`\`

```python file="" isHidden
