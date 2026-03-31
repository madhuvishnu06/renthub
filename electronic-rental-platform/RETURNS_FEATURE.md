# Returns & Notifications Feature Documentation

## Overview

The returns and notifications feature allows customers to request product returns after completing a rental, with shop owners able to review and approve/reject these requests. Automated notifications keep both parties informed throughout the process.

## Features

### 1. **Customer Return Request Page**
- Customers can request returns for **completed bookings only**
- They provide:
  - Reason for return (damaged, defective, not as described, lost, other)
  - Detailed description of the issue
  - Optional proof image upload
- Returns are stored and tracked with status updates
- Customers receive notifications when shop owners review their requests

### 2. **Shop Owner Review & Confirmation**
- Shop owners receive automatic notifications when new return requests are submitted
- They can view all return requests for their products
- They can:
  - **Approve** the return with optional notes
  - **Reject** the return with explanation
  - **Mark as completed** once the return process is finished
- Customers are automatically notified of the decision

### 3. **Notification System**
- Automatic notifications are created for:
  - New return requests (sent to shop owner)
  - Return approvals (sent to customer)
  - Return rejections (sent to customer)
  - Return completions (sent to customer)
- Notifications are visible in the dashboard
- Users can mark notifications as read or delete them
- Unread notification count displayed in dashboard

### 4. **Dashboard Integration**
- **Customer Dashboard:**
  - Shows pending return request count
  - Displays recent return requests with status
  - Shows unread notification count
  - Quick links to return requests and notifications
  - "Request Return" button on completed bookings

- **Shop Owner Dashboard:**
  - Shows pending return requests requiring review
  - Displays recent return requests
  - Quick review button for pending returns
  - Shows unread notification count
  - Integration with product management

## Database Models

### ReturnRequest Model
```python
- booking: OneToOneField (links to booking)
- customer: ForeignKey (who requested the return)
- shop_owner: ForeignKey (product owner receiving the request)
- reason: CharField (reason for return)
- description: TextField (detailed explanation)
- status: CharField (pending/approved/rejected/completed)
- shop_owner_response: TextField (shop owner's notes)
- proof_image: ImageField (optional evidence image)
- created_at: DateTimeField
- updated_at: DateTimeField
- reviewed_at: DateTimeField (when shop owner responded)
```

### Notification Model
```python
- user: ForeignKey (notification recipient)
- notification_type: CharField (type of notification)
- return_request: ForeignKey (related return request)
- title: CharField (notification title)
- message: TextField (notification message)
- is_read: BooleanField (read status)
- created_at: DateTimeField
```

## URL Endpoints

### Customer Routes
- `GET /returns/request/create/<booking_id>/` - Create return request form
- `GET /returns/request/<id>/` - View return request details
- `GET /returns/requests/` - List all return requests (with filters)
- `GET /returns/notifications/` - View all notifications
- `POST /returns/notifications/<id>/mark-as-read/` - Mark notification as read
- `POST /returns/notifications/<id>/delete/` - Delete notification

### Shop Owner Routes
- `GET /returns/requests/` - List return requests (pending and completed)
- `GET /returns/request/<id>/` - View return request details
- `GET/POST /returns/request/<id>/review/` - Review and decide on return request

### API Routes
- `GET /returns/api/notifications/unread/` - Get unread notification count (JSON)

## How It Works

### Customer Return Request Flow
1. Customer views a completed booking
2. Clicks "Request Return" button
3. Fills out return form (reason, description, optional image)
4. Submits the request
5. Notification automatically sent to shop owner
6. Waits for shop owner review

### Shop Owner Review Flow
1. Shop owner sees notification of new return request
2. Navigates to return requests or reviews from dashboard
3. Views request details (customer info, reason, proof image)
4. Clicks "Review Request"
5. Selects decision (Approved/Rejected/Completed)
6. Adds optional response/notes
7. Submits decision
8. Customer automatically receives notification

### Notification Flow
1. Event occurs (new request, approval, rejection, completion)
2. `create_notification()` helper function creates Notification record
3. Notification appears in recipient's notification list
4. Dashboard shows unread notification badge
5. User can mark as read or delete

## Admin Interface

Both `ReturnRequest` and `Notification` models are registered in Django admin with:
- List view with filters (status, reason, date)
- Search functionality (by username, product title)
- Read-only timestamp fields
- Detailed fieldsets for organization
- Inline editing capability

## Templates

### Customer Templates
- `returns/request_create.html` - Create return request form
- `returns/request_detail.html` - View return request with timeline
- `returns/request_list.html` - List all returns with status filters
- `returns/notification_list.html` - Notifications dashboard

### Shop Owner Template
- `returns/request_review.html` - Review and approve/reject returns

### Updated Templates
- `bookings/detail.html` - Added return request button for completed bookings
- `users/customer_dashboard.html` - Added returns and notifications sections
- `users/shop_owner_dashboard.html` - Added pending returns section

## Integration with Existing System

### Booking Status Dependency
- Return requests can only be created for bookings with status = "completed"
- This ensures products have been returned before initiating returns process

### User Roles
- **Customers**: Can view their own return requests and notifications
- **Shop Owners**: Can view return requests for their products and review them
- **Admin**: Can view and manage all returns and notifications

## Notification Permissions
- Users only see their own notifications
- Shop owners receive notifications for returns of their products
- Customers receive notifications for their own returns

## Future Enhancements

1. **Email Notifications** - Send real emails for return requests
2. **Refund Processing** - Automatic refund handling after approved returns
3. **Return Shipping** - Track return shipment status
4. **Admin Dashboard** - Analytics on return requests
5. **Return History** - Detailed tracking of return lifecycle
6. **Auto-Notification Cleanup** - Archive old notifications
7. **Bulk Actions** - Batch approve/reject returns

## Testing the Feature

### Create Test Data
```bash
python manage.py shell

# Create users
from users.models import User
customer = User.objects.create(username='testcustomer', role='customer')
shopowner = User.objects.create(username='testshopowner', role='shop_owner')

# Create product
from products.models import Product, Category
cat = Category.objects.create(name='Test', slug='test')
product = Product.objects.create(
    owner=shopowner,
    title='Test Product',
    category=cat,
    daily_price=50
)

# Create completed booking
from bookings.models import Booking
from datetime import date
booking = Booking.objects.create(
    customer=customer,
    product=product,
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 5),
    total_price=250,
    status='completed'
)
```

### Test Return Request
1. Log in as customer
2. Go to booking details
3. Click "Request Return"
4. Fill out return form
5. Submit

### Test Shop Owner Review
1. Log in as shop owner
2. See notification in dashboard
3. Go to "Return Requests"
4. Click "Review Request"
5. Select approve/reject
6. Add response and submit

### Verify Notifications
1. Check dashboard for notification badge
2. View notification details
3. Mark as read/delete

## Troubleshooting

### Migrations Not Applied
```bash
python manage.py migrate returns
```

### Notifications Not Appearing
- Check that returns app is in INSTALLED_APPS in settings.py
- Verify notification was created with `Notification.objects.all()`
- Check user_id matches current user

### Return Request Not Available
- Confirm booking status is "completed"
- Check that no previous return request exists for booking
- Verify customer is the booking customer

### Images Not Uploading
- Check MEDIA_ROOT and MEDIA_URL settings
- Ensure 'return_proofs/' directory exists or is creatable
- Check file permissions and disk space

## Files Modified/Created

### New Files
- `returns/__init__.py`
- `returns/models.py`
- `returns/views.py`
- `returns/forms.py`
- `returns/urls.py`
- `returns/apps.py`
- `returns/admin.py`
- `returns/migrations/0001_initial.py`
- `templates/returns/request_create.html`
- `templates/returns/request_detail.html`
- `templates/returns/request_list.html`
- `templates/returns/request_review.html`
- `templates/returns/notification_list.html`

### Modified Files
- `rental_platform/settings.py` - Added 'returns' to INSTALLED_APPS
- `rental_platform/urls.py` - Added returns URL includes
- `templates/bookings/detail.html` - Added return request button
- `templates/users/customer_dashboard.html` - Added returns/notifications sections
- `templates/users/shop_owner_dashboard.html` - Added returns/notifications sections
- `users/views.py` - Updated dashboard to include returns/notifications context

## Database Setup

After creating the returns app, run migrations:

```bash
python manage.py makemigrations returns
python manage.py migrate returns
```

Or run the pre-created migration:
```bash
python manage.py migrate returns
```

---

## Summary

This feature provides a complete returns management system with:
✅ Customer return request submission
✅ Shop owner review and decision making
✅ Automatic notification system
✅ Dashboard integration
✅ Admin interface
✅ Permission-based access control
✅ Image proof upload capability
✅ Status tracking and timeline view

The system is fully integrated with existing bookings and user system and is ready for production use.
