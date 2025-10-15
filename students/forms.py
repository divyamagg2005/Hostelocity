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
            'department': forms.Select(attrs={'class': 'form-control'}),
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get all students who already have allocations
        allocated_student_ids = Allocation.objects.values_list('student_id', flat=True)
        
        # Filter to show only unallocated students
        self.fields['student'].queryset = Student.objects.exclude(
            studentid__in=allocated_student_ids
        ).order_by('name')
        
        # Get available rooms (not full)
        available_rooms = []
        for room in Room.objects.all():
            current_occupancy = Allocation.objects.filter(room=room).count()
            if not room.capacity or current_occupancy < room.capacity:
                available_rooms.append(room.roomid)
        
        # Filter to show only available rooms
        self.fields['room'].queryset = Room.objects.filter(
            roomid__in=available_rooms
        ).select_related('hostelid').order_by('hostelid__name', 'roomnumber')
        
        # Update labels to show more info
        self.fields['student'].label_from_instance = lambda obj: f"{obj.name} (ID: {obj.studentid})"
        self.fields['room'].label_from_instance = lambda obj: (
            f"Room {obj.roomnumber} - {obj.hostelid.name} "
            f"(Available: {obj.capacity - Allocation.objects.filter(room=obj).count()}/{obj.capacity})"
        )
    
    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        room = cleaned_data.get('room')
        
        if student and room:
            # Check if student already has a room allocation
            existing_allocation = Allocation.objects.filter(student=student).first()
            if existing_allocation:
                raise forms.ValidationError(
                    f'{student.name} is already allocated to Room {existing_allocation.room.roomnumber}. '
                    f'Please remove the existing allocation first.'
                )
            
            # Check if room is full
            current_occupancy = Allocation.objects.filter(room=room).count()
            if room.capacity and current_occupancy >= room.capacity:
                raise forms.ValidationError(
                    f'Room {room.roomnumber} is full! '
                    f'Capacity: {room.capacity}, Current Occupancy: {current_occupancy}'
                )
        
        return cleaned_data
