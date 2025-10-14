from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Student
from .forms import StudentForm


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
    
    context = {
        'student': student,
    }
    return render(request, 'students/student_detail.html', context)
