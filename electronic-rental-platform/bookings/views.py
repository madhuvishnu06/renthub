from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from products.models import Product
from .forms import BookingForm
from decimal import Decimal

@login_required
def booking_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if not product.is_available:
        messages.error(request, 'This product is currently unavailable.')
        return redirect('products:detail', pk=product_id)
    
    if product.owner == request.user:
        messages.error(request, 'You cannot book your own product.')
        return redirect('products:detail', pk=product_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.product = product
            booking.status = 'pending'
            
            duration = booking.duration_days
            rental_period = booking.rental_period
            if rental_period == 'daily':
                booking.total_price = product.daily_price * duration
            elif rental_period == 'weekly':
                weeks = Decimal(str(duration / 7))
                booking.total_price = product.weekly_price * weeks
            elif rental_period == 'monthly':
                months = Decimal(str(duration / 30))
                booking.total_price = product.monthly_price * months
            else:
                booking.total_price = product.daily_price * duration
            
            try:
                booking.save()
                messages.success(request, 'Booking request submitted successfully! Waiting for shop owner approval.')
                return redirect('bookings:detail', pk=booking.pk)
            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create.html', {'form': form, 'product': product})

@login_required
def booking_invoice(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.customer != request.user and booking.product.owner != request.user:
        messages.error(request, 'You do not have permission to view this invoice.')
        return redirect('users:dashboard')
    
    return render(request, 'bookings/invoice.html', {'booking': booking})

@login_required
def booking_list(request):
    if request.user.role == 'customer':
        bookings = Booking.objects.filter(customer=request.user).select_related('product', 'product__owner')
    elif request.user.role == 'shop_owner':
        bookings = Booking.objects.filter(product__owner=request.user).select_related('product', 'customer')
    else:
        bookings = Booking.objects.all().select_related('product', 'customer', 'product__owner')
    
    return render(request, 'bookings/list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.customer != request.user and booking.product.owner != request.user and request.user.role != 'admin':
        messages.error(request, 'You do not have permission to view this booking.')
        return redirect('users:dashboard')
    
    has_payment = hasattr(booking, 'payment')
    
    return render(request, 'bookings/detail.html', {
        'booking': booking,
        'has_payment': has_payment
    })

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.customer != request.user:
        messages.error(request, 'You can only cancel your own bookings.')
        return redirect('bookings:detail', pk=pk)
    
    if booking.status in ['completed', 'cancelled']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', pk=pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:list')
    
    return render(request, 'bookings/cancel.html', {'booking': booking})

@login_required
def booking_approve(request, pk):
    """Shop owner approves the booking request"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.product.owner != request.user:
        messages.error(request, 'Only the shop owner can approve bookings.')
        return redirect('bookings:detail', pk=pk)
    
    if booking.status != 'pending':
        messages.error(request, 'This booking has already been processed.')
        return redirect('bookings:detail', pk=pk)
    
    if request.method == 'POST':
        booking.status = 'awaiting_payment'
        booking.shop_owner_notes = request.POST.get('notes', '')
        booking.shop_owner_approved_at = timezone.now()
        booking.save()
        messages.success(request, 'Booking approved! Customer will be notified to proceed with payment.')
        return redirect('bookings:detail', pk=pk)
    
    return render(request, 'bookings/approve.html', {'booking': booking})

@login_required
def booking_reject(request, pk):
    """Shop owner rejects the booking request"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.product.owner != request.user:
        messages.error(request, 'Only the shop owner can reject bookings.')
        return redirect('bookings:detail', pk=pk)
    
    if booking.status != 'pending':
        messages.error(request, 'This booking has already been processed.')
        return redirect('bookings:detail', pk=pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.shop_owner_notes = request.POST.get('notes', '')
        booking.save()
        messages.success(request, 'Booking rejected.')
        return redirect('bookings:detail', pk=pk)
    
    return render(request, 'bookings/reject.html', {'booking': booking})

@login_required
def booking_confirm(request, pk):
    """Shop owner confirms payment and finalizes booking"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.product.owner != request.user:
        messages.error(request, 'Only the shop owner can confirm bookings.')
        return redirect('bookings:detail', pk=pk)
    
    if booking.status != 'payment_submitted':
        messages.error(request, 'Payment must be submitted before confirming.')
        return redirect('bookings:detail', pk=pk)
    
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.payment_verified_at = timezone.now()
        booking.save()
        
        # Update payment status
        if hasattr(booking, 'payment'):
            booking.payment.status = 'verified'
            booking.payment.verified_by = request.user
            booking.payment.verified_at = timezone.now()
            booking.payment.verification_notes = request.POST.get('notes', '')
            booking.payment.save()
        
        messages.success(request, 'Payment verified and booking confirmed successfully!')
        return redirect('bookings:detail', pk=pk)
    
    return render(request, 'bookings/confirm.html', {'booking': booking})

@login_required
def booking_complete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    if booking.product.owner != request.user:
        messages.error(request, 'Only the shop owner can mark bookings as complete.')
        return redirect('users:dashboard')
    
    if booking.status != 'confirmed':
        messages.error(request, 'Only confirmed bookings can be completed.')
        return redirect('bookings:detail', pk=pk)
    
    booking.status = 'completed'
    booking.save()
    messages.success(request, 'Booking marked as complete.')
    return redirect('bookings:detail', pk=pk)
