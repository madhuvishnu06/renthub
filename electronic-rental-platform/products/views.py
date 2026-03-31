from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductImage, Category, Review
from .forms import ProductForm, ProductImageForm, ProductSearchForm, ReviewForm
from django.forms import modelformset_factory

def product_list(request):
    products = Product.objects.filter(is_available=True)
    form = ProductSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        condition = form.cleaned_data.get('condition')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if query:
            products = products.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            products = products.filter(category=category)
        if condition:
            products = products.filter(condition=condition)
        if min_price:
            products = products.filter(daily_price__gte=min_price)
        if max_price:
            products = products.filter(daily_price__lte=max_price)
    
    context = {
        'products': products,
        'form': form,
        'categories': Category.objects.all()
    }
    return render(request, 'products/list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    user_has_completed_booking = False
    user_has_reviewed = False
    
    if request.user.is_authenticated:
        # Check if user has completed a booking for this product
        user_has_completed_booking = request.user.bookings.filter(
            product=product, 
            status='completed'
        ).exists()
        
        # Check if user has already reviewed this product
        user_has_reviewed = Review.objects.filter(
            product=product, 
            user=request.user
        ).exists()
    
    context = {
        'product': product,
        'images': product.images.all(),
        'reviews': product.reviews.all()[:5],
        'user_has_completed_booking': user_has_completed_booking,
        'user_has_reviewed': user_has_reviewed,
    }
    return render(request, 'products/detail.html', context)

@login_required
def product_create(request):
    if request.user.role != 'shop_owner':
        messages.error(request, 'Only shop owners can add products.')
        return redirect('home')
    
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=3, max_num=5)
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            
            for image_form in formset:
                if image_form.cleaned_data and image_form.cleaned_data.get('image'):
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()
            
            messages.success(request, 'Product added successfully!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())
    
    return render(request, 'products/create.html', {'form': form, 'formset': formset})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.owner != request.user:
        messages.error(request, 'You can only edit your own products.')
        return redirect('products:detail', pk=pk)
    
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=2, max_num=5, can_delete=True)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=product.images.all())
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:detail', pk=pk)
    else:
        form = ProductForm(instance=product)
        formset = ImageFormSet(queryset=product.images.all())
    
    return render(request, 'products/edit.html', {'form': form, 'formset': formset, 'product': product})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if product.owner != request.user:
        messages.error(request, 'You can only delete your own products.')
        return redirect('products:detail', pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:list')
    
    return render(request, 'products/delete.html', {'product': product})

@login_required
def my_products(request):
    if request.user.role != 'shop_owner':
        messages.error(request, 'Only shop owners can access this page.')
        return redirect('home')
    
    products = Product.objects.filter(owner=request.user)
    return render(request, 'products/my_products.html', {'products': products})

@login_required
def review_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Check if user has already reviewed this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review:
        messages.error(request, 'You have already reviewed this product.')
        return redirect('products:review_edit', pk=existing_review.pk)
    
    # Check if user has completed a booking for this product
    has_booking = request.user.bookings.filter(product=product, status='completed').exists()
    if not has_booking:
        messages.error(request, 'You can only review products you have rented.')
        return redirect('products:detail', pk=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('products:detail', pk=product_id)
    else:
        form = ReviewForm()
    
    return render(request, 'products/review_create.html', {'form': form, 'product': product})

@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if review.user != request.user:
        messages.error(request, 'You can only edit your own reviews.')
        return redirect('products:detail', pk=review.product.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('products:detail', pk=review.product.pk)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'products/review_edit.html', {'form': form, 'review': review})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if review.user != request.user:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('products:detail', pk=review.product.pk)
    
    product_id = review.product.pk
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('products:detail', pk=product_id)
    
    return render(request, 'products/review_delete.html', {'review': review})
