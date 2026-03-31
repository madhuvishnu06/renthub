from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.models import User
from products.models import Product, Category
from bookings.models import Booking
from payments.models import Payment
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_superuser)

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Statistics
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_bookings = Booking.objects.count()
    total_revenue = Payment.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent activity
    recent_users = User.objects.order_by('-created_at')[:5]
    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Category stats
    categories = Category.objects.annotate(product_count=Count('products')).order_by('-product_count')
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'recent_users': recent_users,
        'recent_bookings': recent_bookings,
        'pending_bookings': pending_bookings,
        'categories': categories,
    }
    return render(request, 'adminpanel/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('-created_at')
    
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'role_filter': role_filter,
    }
    return render(request, 'adminpanel/users.html', context)

@login_required
@user_passes_test(is_admin)
def manage_products(request):
    products = Product.objects.all().select_related('owner', 'category').order_by('-created_at')
    
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'category_filter': category_filter,
    }
    return render(request, 'adminpanel/products.html', context)

@login_required
@user_passes_test(is_admin)
def manage_bookings(request):
    bookings = Booking.objects.all().select_related('customer', 'product').order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
    }
    return render(request, 'adminpanel/bookings.html', context)

@login_required
@user_passes_test(is_admin)
def manage_categories(request):
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'adminpanel/categories.html', context)
