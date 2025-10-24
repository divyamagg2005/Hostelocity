from django import forms
from .models import Fee, PaymentRecord
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
    
    payment_type = forms.ChoiceField(
        choices=PaymentRecord.PAYMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        label='Payment Type',
        help_text='Optional: Select the type of payment'
    )
    
    class Meta:
        model = Fee
        fields = ['studentid', 'amount', 'duedate', 'status']
        widgets = {
            'studentid': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'duedate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'studentid': 'Student ID',
            'amount': 'Amount (₹)',
            'duedate': 'Due Date',
            'status': 'Payment Status',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show student ID and name in dropdown
        self.fields['studentid'].label_from_instance = lambda obj: f"{obj.studentid} - {obj.name}"
        
        # If editing an existing fee, populate payment_type from PaymentRecord
        if self.instance and self.instance.pk:
            try:
                payment_record = PaymentRecord.objects.get(fee=self.instance)
                self.fields['payment_type'].initial = payment_record.payment_type
            except PaymentRecord.DoesNotExist:
                pass


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
