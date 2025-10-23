from django import forms
from .models import StudentProfile, Student, Allocation


class StudentForm(forms.ModelForm):
    """Form for admin to add/edit students"""
    
    class Meta:
        model = Student
        fields = ['name', 'gender', 'department', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student name'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True


class AllocationForm(forms.ModelForm):
    """Form for admin to allocate rooms to students"""
    
    class Meta:
        model = Allocation
        fields = ['student', 'room', 'date_of_allocation']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'room': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date_of_allocation': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show only available rooms
        from rooms.models import Room
        allocated_room_ids = Allocation.objects.values_list('room_id', flat=True)
        self.fields['room'].queryset = Room.objects.exclude(
            roomid__in=allocated_room_ids
        )


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