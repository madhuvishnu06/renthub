from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from bookings.models import Booking
from .models import ReturnRequest, Notification
from .forms import ReturnRequestForm, ReturnReviewForm


def create_notification(user, notification_type, return_request, title, message):
    """Helper function to create notifications"""
    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        return_request=return_request,
        title=title,
        message=message
    )


@login_required
def return_request_create(request, booking_id):
    """Customer creates a return request"""
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Verify the user is the customer who booked
    if booking.customer != request.user:
        messages.error(request, 'You can only create return requests for your own bookings.')
        return redirect('bookings:detail', pk=booking_id)
    
    # Check if booking is completed
    if booking.status != 'completed':
        messages.error(request, 'You can only request returns for completed bookings.')
        return redirect('bookings:detail', pk=booking_id)
    
    # Check if return request already exists
    if hasattr(booking, 'return_request'):
        messages.warning(request, 'A return request already exists for this booking.')
        return redirect('returns:request_detail', pk=booking.return_request.pk)
    
    if request.method == 'POST':
        form = ReturnRequestForm(request.POST, request.FILES)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.booking = booking
            return_request.customer = request.user
            return_request.shop_owner = booking.product.owner
            return_request.save()
            
            # Create notification for shop owner
            create_notification(
                user=booking.product.owner,
                notification_type='return_request',
                return_request=return_request,
                title=f'New Return Request - {booking.product.title}',
                message=f'{request.user.username} has requested a return for {booking.product.title}. Reason: {return_request.get_reason_display()}'
            )
            
            messages.success(request, 'Return request submitted successfully! Shop owner will review it soon.')
            return redirect('returns:request_detail', pk=return_request.pk)
    else:
        form = ReturnRequestForm()
    
    return render(request, 'returns/request_create.html', {
        'form': form,
        'booking': booking,
    })


@login_required
def return_request_detail(request, pk):
    """View return request details"""
    return_request = get_object_or_404(ReturnRequest, pk=pk)
    
    # Check permission
    if return_request.customer != request.user and return_request.shop_owner != request.user:
        messages.error(request, 'You do not have permission to view this return request.')
        return redirect('users:dashboard')
    
    return render(request, 'returns/request_detail.html', {
        'return_request': return_request,
    })


@login_required
def return_request_list(request):
    """List all return requests for the user"""
    if request.user.role == 'customer':
        return_requests = ReturnRequest.objects.filter(customer=request.user)
    elif request.user.role == 'shop_owner':
        return_requests = ReturnRequest.objects.filter(shop_owner=request.user)
    else:
        return_requests = ReturnRequest.objects.all()
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        return_requests = return_requests.filter(status=status)
    
    # Pagination
    paginator = Paginator(return_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'returns/request_list.html', {
        'page_obj': page_obj,
        'return_requests': page_obj.object_list,
        'status_filter': status,
    })


@login_required
def return_request_review(request, pk):
    """Shop owner reviews and approves/rejects return request"""
    return_request = get_object_or_404(ReturnRequest, pk=pk)
    
    # Check if user is the shop owner
    if return_request.shop_owner != request.user:
        messages.error(request, 'You can only review returns for your own products.')
        return redirect('returns:request_list')
    
    if return_request.status != 'pending':
        messages.warning(request, 'This return request has already been reviewed.')
        return redirect('returns:request_detail', pk=pk)
    
    if request.method == 'POST':
        form = ReturnReviewForm(request.POST, instance=return_request)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.reviewed_at = timezone.now()
            return_request.save()
            
            # Create notification for customer
            status_display = return_request.get_status_display()
            notification_type = f'return_{return_request.status}'
            
            create_notification(
                user=return_request.customer,
                notification_type=notification_type,
                return_request=return_request,
                title=f'Return Request {status_display}',
                message=f'Your return request for {return_request.booking.product.title} has been {return_request.status}.'
            )
            
            messages.success(request, f'Return request {return_request.status} successfully!')
            return redirect('returns:request_detail', pk=pk)
    else:
        form = ReturnReviewForm(instance=return_request)
    
    return render(request, 'returns/request_review.html', {
        'return_request': return_request,
        'form': form,
    })


@login_required
def notification_list(request):
    """View all notifications for the user"""
    notifications = Notification.objects.filter(user=request.user)
    
    # Pagination
    paginator = Paginator(notifications, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'returns/notification_list.html', {
        'page_obj': page_obj,
        'notifications': page_obj.object_list,
    })


@login_required
def notification_mark_as_read(request, pk):
    """Mark notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()
    messages.success(request, 'Notification marked as read.')
    return redirect('returns:notification_list')


@login_required
def notification_delete(request, pk):
    """Delete a notification"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted.')
    return redirect('returns:notification_list')


@login_required
def get_unread_notifications(request):
    """API endpoint to get unread notification count"""
    from django.http import JsonResponse
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})
