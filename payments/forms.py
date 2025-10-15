from django import forms
from .models import Fee
from students.models import Student


class FeeForm(forms.ModelForm):
    """Form for creating/editing fees - matches Supabase schema"""
    
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='Not Paid'
    )
    
    class Meta:
        model = Fee
        fields = ['studentid', 'amount', 'status']
        widgets = {
            'studentid': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'studentid': 'Student ID',
            'amount': 'Amount (₹)',
            'status': 'Payment Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show student ID and name in dropdown
        self.fields['studentid'].label_from_instance = lambda obj: f"{obj.studentid} - {obj.name}"


class FeeUpdateForm(forms.ModelForm):
    """Form for updating fee status - matches Supabase schema"""
    
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    ]
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Fee
        fields = ['status']
        labels = {
            'status': 'Payment Status',
        }


# Backward compatibility aliases
PaymentForm = FeeForm
PaymentUpdateForm = FeeUpdateForm
