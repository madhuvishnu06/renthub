# Returns Feature - Quick Setup Guide

## Installation Steps

### 1. Apply Database Migrations

```bash
# Run the migration to create returns tables
python manage.py migrate returns

# Or if you need to create migrations first
python manage.py makemigrations returns
python manage.py migrate returns
```

### 2. Verify Installation

Check that the feature is working:

```bash
# Open Django shell
python manage.py shell

# Verify models exist
from returns.models import ReturnRequest, Notification
print("✓ Returns app models loaded successfully")
```

### 3. Access Admin Interface

1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. You should see:
   - **Returns** > Return Requests (manage returns)
   - **Returns** > Notifications (view notifications)

### 4. Test the Feature

#### For Customers:
1. Create a booking and complete it
2. Go to booking details
3. Click "Request Return" button
4. Fill out the form and submit
5. Check dashboard for notifications

#### For Shop Owners:
1. Login as a shop owner
2. Check dashboard for pending returns
3. Click "Review Request" to approve/reject
4. Add response and submit decision

## Key URLs

- Customer Dashboard: `/users/dashboard/`
- Shop Owner Dashboard: `/users/dashboard/`
- Return Requests List: `/returns/requests/`
- Create Return Request: `/returns/request/create/<booking_id>/`
- View Return Details: `/returns/request/<id>/`
- Review Return (Shop Owner): `/returns/request/<id>/review/`
- Notifications: `/returns/notifications/`
- Admin: `/admin/returns/`

## Files Added/Modified

**New Files:**
```
returns/
├── __init__.py
├── models.py          # ReturnRequest, Notification models
├── views.py           # All views for returns
├── forms.py           # Return request and review forms
├── urls.py            # URL routing
├── apps.py            # App config
├── admin.py           # Admin interface
└── migrations/
    ├── __init__.py
    └── 0001_initial.py

templates/returns/
├── request_create.html    # Create return request form
├── request_detail.html    # View return request
├── request_list.html      # List all return requests
├── request_review.html    # Shop owner review interface
└── notification_list.html # View notifications
```

**Modified Files:**
- `rental_platform/settings.py` - Added 'returns' to INSTALLED_APPS
- `rental_platform/urls.py` - Added returns URL patterns
- `templates/bookings/detail.html` - Added return button
- `templates/users/customer_dashboard.html` - Added returns section
- `templates/users/shop_owner_dashboard.html` - Added returns section
- `users/views.py` - Updated dashboard context

## Features Available

✅ **Customers Can:**
- View completed bookings
- Click "Request Return" on completed bookings
- Submit return with reason and description
- Upload proof image (optional)
- View all their return requests
- See return status (pending/approved/rejected/completed)
- Receive notifications of decisions
- View notifications dashboard

✅ **Shop Owners Can:**
- See pending returns in dashboard
- Review customer return requests
- View customer details and proof image
- Approve, reject, or mark as completed
- Add response/notes to decision
- See all return requests for their products
- Receive notifications of new returns

✅ **Admin Can:**
- View all return requests
- Manage all notifications
- Filter by status, reason, date
- Search by username or product
- View detailed request information

## Common Operations

### Migrate Database
```bash
python manage.py migrate returns
```

### Create a Return Request (as customer)
```python
from returns.models import ReturnRequest
from bookings.models import Booking

booking = Booking.objects.get(pk=1)
return_req = ReturnRequest.objects.create(
    booking=booking,
    customer=booking.customer,
    shop_owner=booking.product.owner,
    reason='damaged',
    description='Product arrived with cracked screen'
)
```

### Review a Return Request (as shop owner)
```python
from returns.models import ReturnRequest, Notification

return_req = ReturnRequest.objects.get(pk=1)
return_req.status = 'approved'
return_req.shop_owner_response = 'Approved. Please ship back for refund.'
return_req.save()

# Notification is automatically created by the view
```

### Get Unread Notifications
```python
from returns.models import Notification

unread = Notification.objects.filter(
    user_id=request.user.id,
    is_read=False
).count()
```

## Permissions & Access Control

- Customers can only view/create their own returns
- Shop owners can only view returns for their products
- Users can only see their own notifications
- Admin can view everything

## Important Notes

1. **Returns can only be requested for completed bookings**
2. **One return request per booking** (OneToOneField enforces this)
3. **Notifications are automatically created** when status changes
4. **Images are stored in** `media/return_proofs/`
5. **Timestamps track** when requests are made and reviewed

## Troubleshooting

### Migration Issues
```bash
# Reset migrations (CAREFUL - loses data)
python manage.py migrate returns zero
python manage.py migrate returns

# Or just run migrate
python manage.py migrate
```

### Templates Not Found
- Ensure `templates/returns/` directory exists
- Check TEMPLATES setting in settings.py
- Verify 'APP_DIRS': True in TEMPLATES

### Permissions Error
- Verify user is logged in
- Check user role (customer/shop_owner)
- Confirm user owns the booking (for customers)
- Confirm user owns the product (for shop owners)

### Notifications Not Appearing
- Check that Notification objects are created
- Verify user_id matches in notification
- Check is_read flag (False = unread badge shows)
- Use `Notification.objects.filter(user=request.user)`

## Next Steps

1. **Email Integration**: Send email notifications
2. **Refunds**: Automate refund processing
3. **Shipping**: Track return shipments
4. **Analytics**: View return statistics
5. **Chat**: Enable in-app messaging for returns

---

**Feature Status: ✅ Ready for Production**

For detailed documentation, see [RETURNS_FEATURE.md](RETURNS_FEATURE.md)
