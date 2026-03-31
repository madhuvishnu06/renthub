from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, PaymentQRCode
from bookings.models import Booking
from .forms import PaymentForm, PaymentScreenshotForm, QRCodeForm, CreditCardPaymentForm
import uuid

@login_required
def payment_process(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    
    if booking.customer != request.user:
        messages.error(request, 'You can only pay for your own bookings.')
        return redirect('bookings:detail', pk=booking_id)
    
    if booking.status not in ['awaiting_payment', 'payment_submitted']:
        messages.error(request, 'This booking is not ready for payment. Please wait for shop owner approval.')
        return redirect('bookings:detail', pk=booking_id)
    
    try:
        payment = booking.payment
        if payment.status in ['verified', 'success']:
            messages.info(request, 'This booking has already been paid and verified.')
            return redirect('payments:success', pk=payment.pk)
    except Payment.DoesNotExist:
        payment = None
    
    shop_owner_qr = None
    try:
        shop_owner_qr = booking.product.owner.payment_qr
        if not shop_owner_qr.is_active:
            shop_owner_qr = None
    except PaymentQRCode.DoesNotExist:
        shop_owner_qr = None
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if payment_method == 'credit_card':
            form = CreditCardPaymentForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.cleaned_data.get('payment_screenshot'):
                    messages.error(request, 'Payment screenshot is required!')
                    return render(request, 'payments/process.html', {
                        'booking': booking,
                        'payment': payment,
                        'shop_owner_qr': shop_owner_qr,
                        'credit_card_form': form,
                        'screenshot_form': PaymentScreenshotForm(),
                    })
                
                if not payment:
                    payment = Payment.objects.create(
                        booking=booking,
                        amount=booking.total_price,
                        payment_method='credit_card',
                        status='submitted',
                        transaction_id=f'CC_{uuid.uuid4().hex[:12].upper()}',
                        payment_screenshot=form.cleaned_data['payment_screenshot'],
                        card_last_four=form.cleaned_data['card_number'][-4:],
                        card_type=form.cleaned_data.get('card_type', 'Unknown'),
                        payment_details=f"Cardholder: {form.cleaned_data['cardholder_name']}"
                    )
                else:
                    payment.payment_method = 'credit_card'
                    payment.status = 'submitted'
                    payment.transaction_id = f'CC_{uuid.uuid4().hex[:12].upper()}'
                    payment.payment_screenshot = form.cleaned_data['payment_screenshot']
                    payment.card_last_four = form.cleaned_data['card_number'][-4:]
                    payment.save()
                
                booking.status = 'payment_submitted'
                booking.save()
                
                messages.success(request, 'Payment submitted successfully! Waiting for shop owner verification.')
                return redirect('bookings:detail', pk=booking_id)
        
        elif payment_method in ['razorpay', 'stripe', 'qr_code', 'screenshot']:
            form = PaymentScreenshotForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.cleaned_data.get('payment_screenshot'):
                    messages.error(request, 'Payment screenshot is mandatory!')
                    return render(request, 'payments/process.html', {
                        'booking': booking,
                        'payment': payment,
                        'shop_owner_qr': shop_owner_qr,
                        'credit_card_form': CreditCardPaymentForm(),
                        'screenshot_form': form,
                    })
                
                if not payment:
                    payment = Payment.objects.create(
                        booking=booking,
                        amount=booking.total_price,
                        payment_method=payment_method,
                        status='submitted',
                        transaction_id=f'TXN_{uuid.uuid4().hex[:12].upper()}',
                        payment_screenshot=form.cleaned_data['payment_screenshot'],
                        payment_details=form.cleaned_data.get('payment_details', '')
                    )
                else:
                    payment.payment_method = payment_method
                    payment.status = 'submitted'
                    payment.payment_screenshot = form.cleaned_data['payment_screenshot']
                    payment.payment_details = form.cleaned_data.get('payment_details', '')
                    payment.save()
                
                booking.status = 'payment_submitted'
                booking.save()
                
                messages.success(request, 'Payment submitted successfully! Waiting for shop owner verification.')
                return redirect('bookings:detail', pk=booking_id)
            else:
                messages.error(request, 'Please correct the errors in the form.')
    
    credit_card_form = CreditCardPaymentForm()
    screenshot_form = PaymentScreenshotForm()
    
    context = {
        'booking': booking,
        'payment': payment,
        'shop_owner_qr': shop_owner_qr,
        'credit_card_form': credit_card_form,
        'screenshot_form': screenshot_form,
    }
    return render(request, 'payments/process.html', context)

@login_required
def payment_success(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    
    if payment.booking.customer != request.user and payment.booking.product.owner != request.user:
        messages.error(request, 'You do not have permission to view this payment.')
        return redirect('users:dashboard')
    
    return render(request, 'payments/success.html', {'payment': payment})

@login_required
def payment_failed(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    
    if payment.booking.customer != request.user:
        messages.error(request, 'You do not have permission to view this payment.')
        return redirect('users:dashboard')
    
    return render(request, 'payments/failed.html', {'payment': payment})

@login_required
def qr_code_manage(request):
    if request.user.role != 'shop_owner':
        messages.error(request, 'Only shop owners can manage QR codes.')
        return redirect('users:dashboard')
    
    try:
        qr_code = request.user.payment_qr
    except PaymentQRCode.DoesNotExist:
        qr_code = None
    
    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES, instance=qr_code)
        if form.is_valid():
            qr = form.save(commit=False)
            qr.shop_owner = request.user
            qr.save()
            messages.success(request, 'QR Code updated successfully!')
            return redirect('users:dashboard')
    else:
        form = QRCodeForm(instance=qr_code)
    
    return render(request, 'payments/qr_code_manage.html', {'form': form, 'qr_code': qr_code})

@login_required
def payment_list(request):
    if request.user.role == 'customer':
        payments = Payment.objects.filter(booking__customer=request.user).select_related('booking', 'booking__product')
    elif request.user.role == 'shop_owner':
        payments = Payment.objects.filter(booking__product__owner=request.user).select_related('booking', 'booking__product', 'booking__customer')
    else:
        payments = Payment.objects.all().select_related('booking', 'booking__product', 'booking__customer')
    
    return render(request, 'payments/list.html', {'payments': payments})
