from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student, Allocation, StudentProfile
from .forms import StudentForm, AllocationForm, StudentProfileForm
from datetime import date


def is_admin(user):
    """Check if user is admin"""
    if user.is_superuser:
        return True
    try:
        return user.profile.role == 'admin'
    except:
        return False


@login_required
@user_passes_test(is_admin)
def student_list(request):
    """List all students"""
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'students/student_list.html', context)


@login_required
@user_passes_test(is_admin)
def student_add(request):
    """Add new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.name} added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Add Student',
    }
    return render(request, 'students/student_form.html', context)


@login_required
@user_passes_test(is_admin)
def student_edit(request, pk):
    """Edit student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.name} updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'title': 'Edit Student',
        'student': student,
    }
    return render(request, 'students/student_form.html', context)


@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    """Delete student"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f'Student {name} deleted successfully!')
        return redirect('student_list')
    
    context = {
        'student': student,
    }
    return render(request, 'students/student_confirm_delete.html', context)


@login_required
def student_detail(request, pk):
    """View student details"""
    student = get_object_or_404(Student, pk=pk)
    
    # Check if user is admin or the student themselves
    if not is_admin(request.user) and (not hasattr(request.user, 'student') or request.user.student.pk != pk):
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    allocations = student.allocations.all()
    
    context = {
        'student': student,
        'allocations': allocations,
    }
    return render(request, 'students/student_detail.html', context)


# Allocation Views
@login_required
@user_passes_test(is_admin)
def allocation_list(request):
    """List all room allocations"""
    allocations = Allocation.objects.all().select_related('student', 'room')
    context = {
        'allocations': allocations,
    }
    return render(request, 'students/allocation_list.html', context)


@login_required
@user_passes_test(is_admin)
def allocation_add(request):
    """Allocate room to student"""
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.date_of_allocation = date.today()
            allocation.save()
            messages.success(request, f'Room allocated to {allocation.student.name} successfully!')
            return redirect('allocation_list')
    else:
        form = AllocationForm()
    
    context = {
        'form': form,
        'title': 'Allocate Room',
    }
    return render(request, 'students/allocation_form.html', context)


@login_required
@user_passes_test(is_admin)
def allocation_delete(request, pk):
    """Remove room allocation"""
    allocation = get_object_or_404(Allocation, pk=pk)
    
    if request.method == 'POST':
        student_name = allocation.student.name
        allocation.delete()
        messages.success(request, f'Room allocation for {student_name} removed successfully!')
        return redirect('allocation_list')
    
    context = {
        'allocation': allocation,
    }
    return render(request, 'students/allocation_confirm_delete.html', context)


@login_required
def student_profile_edit(request):
    """Edit student profile (students only)"""
    # Try to find student by username matching
    student = Student.objects.filter(name__icontains=request.user.username).first()
    if not student:
        # If no exact match, try to find by user profile or create a basic student record
        student = Student.objects.filter(studentid=request.user.id).first()
    
    if not student:
        messages.error(request, 'Student profile not found. Please contact admin.')
        return redirect('dashboard')
    
    # Get or create student profile
    try:
        student_profile = StudentProfile.objects.get(student=student)
    except StudentProfile.DoesNotExist:
        student_profile = StudentProfile.objects.create(student=student)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
    else:
        form = StudentProfileForm(instance=student_profile)
    
    context = {
        'form': form,
        'title': 'Edit Profile',
        'student': student,
    }
    return render(request, 'students/student_profile_edit.html', context)
