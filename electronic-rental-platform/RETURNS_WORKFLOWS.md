# Returns Feature - Visual Workflows & Examples

## 🔄 System Workflow Diagrams

### Complete Return Request Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RETURN REQUEST WORKFLOW                           │
└─────────────────────────────────────────────────────────────────────┘

CUSTOMER                              SHOP OWNER                  SYSTEM
   │                                      │                          │
   │  1. View Completed Booking           │                          │
   │─────────────────────────────────►    │                          │
   │                                      │                          │
   │  2. Click "Request Return"           │                          │
   │─────────────────────────────────►    │                          │
   │                                      │                          │
   │  3. Fill Return Form                 │                          │
   │     - Reason                         │                          │
   │     - Description                    │                          │
   │     - Proof Image (optional)         │                          │
   │─────────────────────────────────►    │                          │
   │                                      │  4. Receives             │
   │                                      │     Notification◄────────│
   │                                      │                          │
   │                                      │  5. Review Return        │
   │                                      │     Request              │
   │                                      │─────────────────────────►
   │                                      │                          │
   │                                      │  6. Make Decision        │
   │                                      │     (Approve/Reject)     │
   │                                      │─────────────────────────►
   │                                      │                          │
   │  7. Receives Decision                │  8. Add Response        │
   │     Notification◄───────────────────│     (optional)          │
   │                                      │                          │
   │  8. Check Notification in            │  9. Submit              │
   │     Dashboard                        │     Decision             │
   │─────────────────────────────────►    │                          │
   │                                      │                          │
   │  9. View Return Status               │                          │
   │     in Details                       │                          │
   │─────────────────────────────────►    │                          │
   │                                      │                          │

FINAL STATUS: 
- PENDING (awaiting shop owner review)
- APPROVED (accepted by shop owner)
- REJECTED (declined by shop owner)
- COMPLETED (return process finished)
```

### Notification System

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NOTIFICATION TRIGGERS                            │
└─────────────────────────────────────────────────────────────────────┘

EVENT                          RECIPIENT           NOTIFICATION TYPE
─────────────────────────────────────────────────────────────────────
Customer creates return    →   Shop Owner      →   "New Return Request"
Shop owner approves        →   Customer        →   "Return Approved"
Shop owner rejects         →   Customer        →   "Return Rejected"  
Shop owner marks completed →   Customer        →   "Return Completed"

NOTIFICATION FEATURES:
├─ Is marked unread by default (shows blue badge)
├─ Links to related return request
├─ Includes timestamp
├─ Can be marked as read
├─ Can be deleted
└─ Shows in dashboard widget
```

### Dashboard Display

```
┌──────────────────────────────────────────────┐
│   CUSTOMER DASHBOARD                         │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │
│  │ 2    │ │ 8    │ │ 1    │ │ 3    │       │
│  │Active│ │Total │ │Return│ │Notif.│       │
│  │Books │ │Books │ │Req.  │ │      │       │
│  └──────┘ └──────┘ └──────┘ └──────┘       │
│                                              │
│  ─────────────────────────────────────────  │
│  RECENT RETURNS                              │
│  ├─ Product 1: PENDING ⏳                   │
│  ├─ Product 2: APPROVED ✓                   │
│  └─ Product 3: REJECTED ✗                   │
│                                              │
│  ─────────────────────────────────────────  │
│  RECENT NOTIFICATIONS                        │
│  ├─ New: Return Request Submitted            │
│  ├─ Read: Return Approved                    │
│  └─ Read: Approve shipping label...          │
│                                              │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│   SHOP OWNER DASHBOARD                       │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │
│  │ 3    │ │ 2    │ │ 5    │ │ 2    │       │
│  │Product│ │Pending│ │Active│ │Notif.│      │
│  │s     │ │Return │ │Rental│ │      │      │
│  └──────┘ └──────┘ └──────┘ └──────┘       │
│                                              │
│  ─────────────────────────────────────────  │
│  RETURNS TO REVIEW [2 pending]               │
│  ├─ Customer: John Doe                       │
│  │   Reason: Damaged (screen cracked)        │
│  │   [REVIEW] ─────────────────────►         │
│  │                                           │
│  └─ Customer: Jane Smith                     │
│     Reason: Defective                        │
│     [REVIEW] ─────────────────────►          │
│                                              │
│  ─────────────────────────────────────────  │
│  RECENT NOTIFICATIONS                        │
│  ├─ New: Return Request from John Doe        │
│  ├─ New: Return Request from Jane Smith      │
│  └─ Read: Refund issued (approved 3 days ago)│
│                                              │
└──────────────────────────────────────────────┘
```

## 🎬 Step-by-Step User Journeys

### Journey 1: Customer Requests a Damaged Product Return

```
STEP 1: Login & Navigate
├─ Log in as customer
├─ Go to "My Dashboard" or "My Bookings"
└─ Find the completed rental (status = "Completed")

STEP 2: Start Return Request
├─ Click on the booking
├─ Scroll to "Return Request Status" section
├─ Click [Request Return] button
└─ Redirected to /returns/request/create/123/

STEP 3: Fill Return Form
├─ Reason: Select "Product Damaged" ⬇
├─ Description: "Screen has cracks on bottom left corner
│             and device doesn't turn on after drop"
├─ Proof Image: Upload photo of damage
└─ Click [Submit Return Request]

STEP 4: Confirmation
├─ Redirected to return request detail page
├─ Status shows: "Pending Review" (yellow badge)
├─ See message: "Return request submitted successfully!"
└─ Check dashboard: now shows "1 Pending Return"

STEP 5: Wait for Shop Owner Review
├─ Shop owner receives notification
├─ Waits for response
├─ Checks dashboard periodically
├─ Sees timeline view of return

STEP 6: Receive Decision Notification
├─ Notification appears in dashboard
├─ Gets notification badge (blue if unread)
├─ Click on notification to view decision
├─ If approved: Instructions for return
├─ If rejected: Shop owner's explanation
```

### Journey 2: Shop Owner Reviews Return Request

```
STEP 1: See Notification
├─ Shop owner logged in
├─ Dashboard shows notification badge
├─ Sees "2 Unread Notifications"
├─ Recently created return request appears
└─ Click "Return Requests" in navigation

STEP 2: View Return Requests
├─ Navigated to /returns/requests/
├─ Sees all return requests for their products
├─ Can filter by status (Pending, Approved, Rejected)
├─ Finds "John Doe - Product: iPhone Charger"
└─ Status: "Pending Review" (yellow badge)

STEP 3: Review Request Details
├─ Click on return request
├─ See customer information:
│  ├─ Name: John Doe
│  ├─ Email: john@example.com
│  └─ Phone: (555) 123-4567
├─ Product details:
│  ├─ Name: iPhone Charger
│  ├─ Rental dates: Jan 1 - Jan 5
│  └─ Total price: $50
├─ Return reason: "Product Damaged"
├─ Description: "Screen has cracks..."
├─ Proof image: Displays photo of damage
└─ Status: "Pending Review"

STEP 4: Make Decision
├─ Click [Review Request] button
├─ Taken to /returns/request/123/review/
├─ See decision form with:
│  ├─ Status dropdown: "Pending" → Select "Approved"
│  └─ Response textarea: "Approved. Please ship back to..."
├─ Fill in response
├─ Click [Submit Review]

STEP 5: Submit Decision
├─ Decision recorded in database
├─ reviewed_at timestamp set
├─ Return status changed to "Approved"
├─ Notification automatically created for customer
├─ Redirected to return request detail page
├─ Sees: "Return request approved successfully!"
└─ Status now shows: "Approved" (green badge)

STEP 6: Customer Gets Notification
├─ Customer sees notification in dashboard
├─ Click to view full decision
├─ Sees shop owner's response
├─ Can now proceed with return (send product back)
```

### Journey 3: Customer Checks Notifications

```
STEP 1: Navigate to Notifications
├─ Click "Notifications" link in dashboard
├─ Taken to /returns/notifications/
├─ Sees list of all notifications

STEP 2: View Notifications
├─ Notification 1: "Return Request Submitted" (Unread - blue)
├─ Notification 2: "Return Approved" (Unread - blue)
├─ Notification 3: "Return Request Acknowledged" (Read - gray)
└─ Each shows timestamp (e.g., "2 hours ago")

STEP 3: Read a Notification
├─ Click on notification
├─ See full notification details
├─ May show linked return request
├─ Can click "View Return Request" to see details

STEP 4: Manage Notifications
├─ Check box or button to "Mark as Read"
├─ Blue badge disappears after marking as read
├─ Click "Delete" to remove notification
├─ Notification removed from list
└─ Dashboard notification count decreases

STEP 5: Return to Dashboard
├─ Unread count now updated
├─ Only unread notifications show badge
└─ Can always view all in notification page
```

## 💡 Real-World Examples

### Example 1: Damaged Product

```
SCENARIO:
Customer Jane Smith rented a laptop. During rental, it fell
and the screen developed cracks. She wants to return it.

ACTIONS:

Jane (Customer):
├─ Logs in to dashboard
├─ Goes to "My Bookings"  
├─ Clicks on completed booking (Laptop rental)
├─ Clicks "Request Return"
├─ Fills form:
│  ├─ Reason: "Product Damaged"
│  ├─ Description: "Screen cracked after accidental drop.
│  │              Device still powers on but display is broken."
│  └─ Image: Uploads photo of cracked screen
└─ Clicks "Submit Return Request"

TechStore (Shop Owner):
├─ Receives notification: "New Return Request - Laptop"
├─ Logs in and views the return request
├─ Sees customer info and proof photo
├─ Reviews the damage claim
├─ Makes decision: "Approved"
├─ Adds response: "Approved. Please ship back to our address
│               using tracking. Refund will be issued upon receipt."
└─ Clicks "Submit Review"

Jane (Customer):
├─ Receives notification: "Return Approved"
├─ Views notification details
├─ Reads shop owner's instructions
├─ Sees in dashboard: Status changed to "Approved" (green)
└─ Proceeds to ship laptop back with tracking number

TechStore (Shop Owner):
├─ Receives return shipment
├─ Verifies condition matches description
├─ Issues refund to customer
└─ Marks return as "Completed"

Jane (Customer):
└─ Receives final notification: "Return Completed"
   Sees refund confirmation in her payment history
```

### Example 2: Not As Described

```
SCENARIO:
Customer Mike bought a "like new" camera lens but it has
dust inside and focusing issues. He requests a return.

ACTIONS:

Mike (Customer):
├─ Views completed camera rental
├─ Clicks "Request Return"
├─ Selects: Reason = "Not As Described"
├─ Describes issue: "Lens has dust inside the lens elements
│  and autofocus doesn't work properly. Listed as 'like new'
│  but appears to have been used without proper care."
├─ Uploads close-up photos of dust in lens
└─ Submits request

CameraGear Shop (Owner):
├─ Sees notification about lens return
├─ Reviews the photos and description
├─ Agrees the condition doesn't match listing
├─ Makes decision: "Approved"
├─ Response: "Approved. Agreed condition is not as listed.
│            Please return ASAP for full refund.
│            We'll provide prepaid return shipping label."
└─ Sends notification

Mike (Customer):
├─ Checks dashboard
├─ Sees "Approved" status
├─ Reads shop owner's message
├─ Receives return shipping label via email
└─ Ships lens back

CameraGear Shop:
├─ Inspects returned lens
├─ Confirms damage and takes photos for records
├─ Issues full refund
├─ Updates return status to "Completed"

Mike:
├─ Sees "Return Completed" notification
├─ Checks refund in bank account within 3-5 days
└─ Transaction complete
```

### Example 3: Shop Owner Rejects Return

```
SCENARIO:
Customer Sarah rented a tablet, used it normally during
rental period, but now wants to return it claiming a defect.
The shop owner inspects it and finds no actual defect.

ACTIONS:

Sarah (Customer):
├─ Completes rental of iPad
├─ Requests return with reason: "Product Defective"
├─ Description: "Occasionally lags when opening apps"
└─ No image uploaded (no visible damage)

TechWorks Shop (Owner):
├─ Receives notification about return
├─ Reviews the description
├─ Checks the device in their inventory
├─ Device works perfectly normally
├─ Tests apps - no lagging observed
├─ Decides: "Rejected"
├─ Response: "Rejected. Device works normally. All apps
│            open and respond quickly. May be due to
│            device usage. No defect found."
└─ Submits decision

Sarah (Customer):
├─ Receives notification: "Return Rejected"
├─ Reads shop owner's explanation
├─ Sees in dashboard: Status = "Rejected" (red badge)
├─ Can view shop owner's detailed response
└─ Can contact shop via chat if they want to discuss further

TechWorks:
├─ Keeps the device (not returned)
├─ Refund is not issued
└─ Return process complete
```

## 📱 UI Elements Reference

### Status Badge Colors
```
PENDING:   🟡 Yellow   (#fef3c7 background, #92400e text)
APPROVED:  🟢 Green    (#d1fae5 background, #065f46 text)
REJECTED:  🔴 Red      (#fee2e2 background, #991b1b text)
COMPLETED: 🔵 Blue     (#dbeafe background, #1e40af text)
```

### Button States
```
Primary (Blue):    Approve Return / Submit Request
Secondary (Gray):  Cancel / View Details
Outline (Border):  Secondary actions
Danger (Red):      Reject / Cancel booking
```

### Notification Badge
```
Unread:   Blue dot / badge with count
Read:     Gray / no badge
New:      Blue banner label
```

## 🎯 Quick Navigation Map

```
Home Page
├── Login / Register
└── Dashboard (after login)
    │
    ├── CUSTOMER DASHBOARD
    │   ├── My Bookings
    │   │   └── [Request Return] (for completed)
    │   ├── Return Requests (/returns/requests/)
    │   │   ├── Filter by status
    │   │   └── View request details
    │   └── Notifications (/returns/notifications/)
    │       ├── Mark as read
    │       └── Delete
    │
    └── SHOP OWNER DASHBOARD
        ├── Return Requests (/returns/requests/)
        │   ├── View pending returns
        │   └── [Review] button
        ├── Review Page (/returns/request/<id>/review/)
        │   ├── View customer details
        │   ├── View proof image
        │   └── Decide + respond
        └── Notifications (/returns/notifications/)
            ├── See all notifications
            └── View linked returns
```

---

This comprehensive guide shows exactly how customers and shop owners interact with the returns system, with real-world examples and visual representations of the data flow.
