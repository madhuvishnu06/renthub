from django import forms
from .models import Payment, PaymentQRCode

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Any payment notes...'
            }),
        }

class PaymentScreenshotForm(forms.ModelForm):
    payment_screenshot = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-file',
            'accept': 'image/*'
        }),
        help_text='Payment screenshot is mandatory'
    )
    
    class Meta:
        model = Payment
        fields = ['payment_screenshot', 'transaction_id', 'payment_details']
        widgets = {
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Transaction/Reference ID (Optional)'
            }),
            'payment_details': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Additional payment details...'
            }),
        }

class CreditCardPaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9]{16}',
            'maxlength': '16'
        }),
        help_text='16-digit card number'
    )
    cardholder_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'John Doe'
        })
    )
    expiry_date = forms.CharField(
        max_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'MM/YY',
            'pattern': '(0[1-9]|1[0-2])\/[0-9]{2}'
        })
    )
    cvv = forms.CharField(
        max_length=3,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'CVV',
            'pattern': '[0-9]{3}',
            'maxlength': '3'
        })
    )
    card_type = forms.ChoiceField(
        choices=[
            ('visa', 'Visa'),
            ('mastercard', 'Mastercard'),
            ('amex', 'American Express'),
            ('discover', 'Discover')
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    payment_screenshot = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-file',
            'accept': 'image/*'
        }),
        help_text='Upload payment confirmation screenshot (Required)'
    )

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = PaymentQRCode
        fields = ['qr_code_image', 'payment_details', 'is_active']
        widgets = {
            'qr_code_image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*'
            }),
            'payment_details': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'UPI ID, Account details, or payment instructions...'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }
