from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, FormView, UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, ProfileForm
from .models import User

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}
    
    if user.role == 'customer':
        # Get customer bookings with related data
        from bookings.models import Booking
        from returns.models import ReturnRequest, Notification
        
        context['active_bookings'] = Booking.objects.filter(
            customer=user,
            status__in=['pending', 'confirmed']
        ).select_related('product').prefetch_related('product__images')[:3]
        
        context['total_bookings'] = Booking.objects.filter(customer=user).count()
        context['completed_bookings'] = Booking.objects.filter(customer=user, status='completed').count()
        
        # Get return requests
        context['return_requests'] = ReturnRequest.objects.filter(customer=user)[:5]
        context['pending_returns'] = ReturnRequest.objects.filter(customer=user, status='pending').count()
        
        # Get unread notifications
        context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
        context['recent_notifications'] = Notification.objects.filter(user=user)[:3]
        
        return render(request, 'users/customer_dashboard.html', context)
        
    elif user.role == 'shop_owner':
        # Get shop owner products and bookings
        from products.models import Product
        from bookings.models import Booking
        from returns.models import ReturnRequest, Notification
        
        products = Product.objects.filter(owner=user).prefetch_related('images', 'bookings')
        context['products'] = products
        context['products_count'] = products.count()
        
        # Get all bookings for shop owner's products
        all_bookings = Booking.objects.filter(product__owner=user).select_related('product', 'customer')
        context['pending_bookings'] = all_bookings.filter(status='pending').count()
        context['active_rentals'] = all_bookings.filter(status='confirmed').count()
        context['recent_bookings'] = all_bookings[:5]
        
        # Calculate total earnings from completed bookings
        from django.db.models import Sum
        total_earnings = all_bookings.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
        context['total_earnings'] = total_earnings
        
        # Get return requests
        context['return_requests'] = ReturnRequest.objects.filter(shop_owner=user)[:5]
        context['pending_returns'] = ReturnRequest.objects.filter(shop_owner=user, status='pending').count()
        
        # Get unread notifications
        context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
        context['recent_notifications'] = Notification.objects.filter(user=user)[:3]
        
        return render(request, 'users/shop_owner_dashboard.html', context)
        
    elif user.role == 'admin':
        return redirect('adminpanel:dashboard')
    
    return redirect('home')
