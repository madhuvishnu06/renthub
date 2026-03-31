# Returns Feature - Quick Reference Guide

## 🎯 What Was Added

A complete returns and notifications system for the rental platform where:
- **Customers** can request returns for completed bookings
- **Shop owners** receive notifications and can approve/reject returns
- **Both parties** are kept updated via automatic notifications
- **Dashboard** integration for quick access and status tracking

## 🚀 Quick Start (30 seconds)

```bash
# 1. Migrate database
python manage.py migrate returns

# 2. Test admin interface
# Go to http://localhost:8000/admin/
# Look for "Returns" section

# 3. You're done! 
```

## 📍 Where to Access the Feature

| User Type | URL | What They See |
|-----------|-----|---------------|
| **Customer** | `/users/dashboard/` | Returns count, recent returns, notifications |
| **Customer** | `/returns/requests/` | All their return requests with status |
| **Customer** | `/returns/notifications/` | All notifications received |
| **Shop Owner** | `/users/dashboard/` | Pending returns, recent requests, notifications |
| **Shop Owner** | `/returns/requests/` | Returns for their products (can filter by status) |
| **Admin** | `/admin/returns/` | Full management interface |

## 💻 Main Features At a Glance

### For Customers
```
Booking Detail Page
        ↓
    [Request Return] button (for completed bookings)
        ↓
    Fill form: reason + description + (optional) image
        ↓
    Shop owner gets NOTIFICATION
        ↓
    Customer gets NOTIFICATION when shop owner responds
```

### For Shop Owners
```
Dashboard
        ↓
    See "Pending Return Requests"
        ↓
    Click [Review] button
        ↓
    See customer details & proof image
        ↓
    Choose: APPROVE / REJECT / COMPLETED
        ↓
    Add optional response notes
        ↓
    Customer gets NOTIFICATION
```

### Notifications
```
Trigger Events:
├── New return request → Sent to shop owner
├── Return approved → Sent to customer
├── Return rejected → Sent to customer
└── Return completed → Sent to customer

Actions:
├── View all in /returns/notifications/
├── Mark as read (remove blue badge)
└── Delete notification
```

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `returns/models.py` | ReturnRequest & Notification models |
| `returns/views.py` | All page logic (create, review, list, etc.) |
| `returns/forms.py` | Return request and review forms |
| `templates/returns/*.html` | 5 templates for different pages |
| `rental_platform/settings.py` | Added 'returns' to INSTALLED_APPS |
| `rental_platform/urls.py` | Added returns URL patterns |

## 🎨 Templates Added

| Template | Used By | Purpose |
|----------|---------|---------|
| `request_create.html` | Customer | Create new return request |
| `request_detail.html` | Both | View return request details + timeline |
| `request_list.html` | Both | List returns with status filter |
| `request_review.html` | Shop Owner | Review and decide on return |
| `notification_list.html` | Both | View all notifications |

## 📊 Database Models

```
ReturnRequest
├── booking: Booking (OneToOne)
├── customer: User
├── shop_owner: User
├── reason: (damaged, defective, not_as_described, lost, other)
├── description: Text
├── status: (pending, approved, rejected, completed)
├── shop_owner_response: Text (optional)
├── proof_image: File (optional)
├── created_at: DateTime
├── updated_at: DateTime
└── reviewed_at: DateTime (when reviewed)

Notification
├── user: User
├── notification_type: (return_request, return_approved, return_rejected, return_completed)
├── return_request: ReturnRequest (optional)
├── title: Text
├── message: Text
├── is_read: Boolean
└── created_at: DateTime
```

## ✅ Status Filters Available

When viewing return requests, filter by:
- **Pending** - Awaiting shop owner review
- **Approved** - Accepted by shop owner
- **Rejected** - Declined by shop owner  
- **Completed** - Return process finished

## 🔗 URLs Quick Reference

```
# Customers
GET  /returns/request/create/<booking_id>/     → Create return form
GET  /returns/request/<id>/                    → View return details
GET  /returns/requests/                        → List my returns
GET  /returns/requests/?status=pending         → Filter by status
GET  /returns/notifications/                   → View notifications
POST /returns/notifications/<id>/mark-as-read/ → Mark as read
POST /returns/notifications/<id>/delete/       → Delete notification

# Shop Owners (same as above, but sees different data)
GET  /returns/requests/                        → List returns for my products
GET  /returns/request/<id>/review/             → Review return request
POST /returns/request/<id>/review/             → Submit decision

# API
GET  /returns/api/notifications/unread/        → Get unread count (JSON)
```

## 🧪 Testing Steps

### Test as Customer
1. Login as customer
2. Go to "My Bookings" 
3. Find a **completed** booking
4. Click "Request Return" button
5. Fill form and submit
6. Check dashboard for "1 Pending Return"

### Test as Shop Owner
1. Login as shop owner account
2. Go to dashboard
3. See notification about new return
4. Click "View Return Requests"
5. Click "Review" on the pending request
6. Choose "Approved" or "Rejected"
7. Add response (optional) and submit

### Test Notifications
1. Check dashboard for notification badge count
2. Click "Notifications" link
3. See notification in list with timestamp
4. Click "Mark as Read" to remove blue badge
5. Click "Delete" to remove notification

## 🎯 Common Use Cases

### Use Case 1: Product Arrived Damaged
```
1. Customer: Click "Request Return"
2. Customer: Select "Damaged" as reason
3. Customer: Describe issue and upload photo
4. Shop Owner: Receives notification
5. Shop Owner: Reviews details and image
6. Shop Owner: Approves return
7. Customer: Receives approval notification
```

### Use Case 2: Not As Described
```
1. Customer: Create return request
2. Customer: Choose "Not As Described" reason
3. Customer: Explain what's different
4. Shop Owner: Reviews request
5. Shop Owner: Can approve or request more info (via response)
6. Shop Owner: Makes decision
7. Customer: Sees result in dashboard
```

### Use Case 3: Shopowner Rejects Return
```
1. Shop Owner: Reviews customer's return request
2. Shop Owner: Chooses "Rejected"
3. Shop Owner: Adds response: "Product appears to be undamaged"
4. Customer: Gets rejection notification
5. Customer: Sees shop owner's response in details
```

## 🚨 Important Notes

⚠️ **Customers can only request returns for COMPLETED bookings**

⚠️ **Only ONE return request per booking** (enforced by database)

⚠️ **Images are optional** but recommended for proof

⚠️ **Notifications are permanent** until user deletes them

⚠️ **Shop owner responses** are only visible after they review the request

## 🔒 Permissions

- ✅ Customer can see only their own returns
- ✅ Customer can see only their own notifications
- ✅ Shop owner can see returns only for their products
- ✅ Shop owner can see only their own notifications
- ✅ Admin can see everything
- ✅ Can't view other user's data

## 📈 Dashboard Widgets

### Customer Dashboard Shows
```
[Pending Returns Count] [Active Bookings] [Total Bookings] [Unread Notifications]

Recent Returns Section
- Shows last 5 return requests with status
- Color-coded status badges

Recent Notifications Section
- Shows last 3 notifications
- Mark as read/delete options
```

### Shop Owner Dashboard Shows
```
[Pending Returns Count] [Active Rentals] [Products] [Unread Notifications]

Return Requests to Review Section
- Shows pending returns with customer name
- Quick [Review] button
- Highlights pending requests in yellow

Recent Notifications Section
- Shows latest notifications
```

## 🐛 Troubleshooting Quick Fix

| Problem | Solution |
|---------|----------|
| "Return Request Not Found" | Booking must be "completed" status |
| "You don't have permission" | Must be customer who made booking or shop owner |
| Images not uploading | Check `media/return_proofs/` directory exists |
| Notifications not showing | Refresh page or check unread count |
| Button missing from booking | Booking status is not "completed" |
| Can't access returns admin | Added 'returns' to INSTALLED_APPS? |

## 📚 Full Documentation

For complete details, see:
- `RETURNS_FEATURE.md` - Full feature documentation
- `RETURNS_SETUP.md` - Installation & setup guide  
- `RETURNS_IMPLEMENTATION.md` - Implementation details

## 🎓 Example Code

### Get a user's return requests
```python
from returns.models import ReturnRequest
my_returns = ReturnRequest.objects.filter(customer=request.user)
```

### Get pending returns for a shop owner
```python
pending = ReturnRequest.objects.filter(
    shop_owner=request.user,
    status='pending'
)
```

### Get unread notification count
```python
from returns.models import Notification
count = Notification.objects.filter(
    user=request.user,
    is_read=False
).count()
```

### Create a return request
```python
from returns.models import ReturnRequest
from bookings.models import Booking

booking = Booking.objects.get(pk=1)
return_req = ReturnRequest.objects.create(
    booking=booking,
    customer=booking.customer,
    shop_owner=booking.product.owner,
    reason='damaged',
    description='Screen is cracked'
)
# Notification auto-created by view
```

## ✨ Summary

✅ Fully functional returns system
✅ Automatic notifications
✅ Dashboard integration
✅ Admin interface
✅ Production ready
✅ Mobile responsive
✅ Secure (permission checks)
✅ Well documented

**Start using it today!**
