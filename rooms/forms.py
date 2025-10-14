from django import forms
from .models import Room, Hostel


class HostelForm(forms.ModelForm):
    """Form for creating/editing hostels - matches Supabase schema"""
    class Meta:
        model = Hostel
        fields = ['name', 'location', 'totalrooms']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'totalrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'totalrooms': 'Total Rooms',
        }


class RoomForm(forms.ModelForm):
    """Form for creating/editing rooms - matches Supabase schema"""
    class Meta:
        model = Room
        fields = ['hostelid', 'roomnumber', 'capacity', 'type']
        widgets = {
            'hostelid': forms.Select(attrs={'class': 'form-control'}),
            'roomnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'hostelid': 'Hostel',
            'roomnumber': 'Room Number',
        }
