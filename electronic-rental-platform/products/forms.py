from django import forms
from .models import Product, ProductImage, Category, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'condition', 'daily_price', 
                  'weekly_price', 'monthly_price', 'stock', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Product name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Detailed description'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'daily_price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'weekly_price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-file', 'accept': 'image/*'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class ProductSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Search electronics...'
    }))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='All Categories'
    )
    condition = forms.ChoiceField(
        choices=[('', 'All Conditions')] + list(Product.CONDITION_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-input',
        'placeholder': 'Min price',
        'step': '0.01'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-input',
        'placeholder': 'Max price',
        'step': '0.01'
    }))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Share your experience with this product...'
            }),
        }
