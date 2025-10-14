from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):
    """Form for creating/editing fees - matches Supabase schema"""
    class Meta:
        model = Fee
        fields = ['studentid', 'amount', 'duedate', 'status']
        widgets = {
            'studentid': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'duedate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'studentid': 'Student',
            'duedate': 'Due Date',
        }


class FeeUpdateForm(forms.ModelForm):
    """Form for updating fee status - matches Supabase schema"""
    class Meta:
        model = Fee
        fields = ['status']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Backward compatibility aliases
PaymentForm = FeeForm
PaymentUpdateForm = FeeUpdateForm
