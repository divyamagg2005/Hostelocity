from django import forms
from .models import Student, Allocation
from rooms.models import Room


class StudentForm(forms.ModelForm):
    """Form for creating/editing students - matches Supabase schema"""
    class Meta:
        model = Student
        fields = ['name', 'gender', 'department', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AllocationForm(forms.ModelForm):
    """Form for allocating students to rooms"""
    class Meta:
        model = Allocation
        fields = ['student', 'room']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
        }
