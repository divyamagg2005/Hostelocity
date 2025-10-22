from django import forms
from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    """Form for students to edit their profile details"""
    
    class Meta:
        model = StudentProfile
        fields = [
            'address', 'father_name', 'mother_name', 
            'father_phone', 'mother_phone', 'date_of_birth', 'hostel_mess'
        ]
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your permanent address'
            }),
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Father\'s full name'
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mother\'s full name'
            }),
            'father_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Father\'s phone number'
            }),
            'mother_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mother\'s phone number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hostel_mess': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required for first-time setup
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs.update({'required': True})