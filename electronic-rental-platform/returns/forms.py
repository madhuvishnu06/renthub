from django import forms
from .models import ReturnRequest

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['reason', 'description', 'proof_image']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please describe the issue with the product...'
            }),
            'proof_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'reason': 'Reason for Return',
            'description': 'Detailed Description',
            'proof_image': 'Upload Proof Image (Optional)',
        }


class ReturnReviewForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['status', 'shop_owner_response']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'shop_owner_response': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Your response to the return request...'
            }),
        }
        labels = {
            'status': 'Decision',
            'shop_owner_response': 'Your Response',
        }
