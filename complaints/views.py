from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Complaint
from .forms import ComplaintForm, ComplaintUpdateForm
from students.models import Student


def is_admin(user):
    """Check if user is admin"""
    if user.is_superuser:
        return True
    try:
        return user.profile.role == 'admin'
    except:
        return False


@login_required
def complaint_list(request):
    """List complaints based on user role"""
    if is_admin(request.user):
        # Admin sees all complaints
        complaints = Complaint.objects.all()
        template = 'complaints/complaint_list.html'
    else:
        # Student sees only their complaints
        try:
            # Try to find student by username matching
            student = Student.objects.filter(name__icontains=request.user.username).first()
            if not student:
                # If no exact match, try to find by user profile or create a basic student record
                student = Student.objects.filter(studentid=request.user.id).first()
            
            if student:
                complaints = Complaint.objects.filter(student=student)
            else:
                complaints = []
                messages.warning(request, 'Student profile not found.')
        except Exception as e:
            complaints = []
            messages.warning(request, f'Error finding student profile: {str(e)}')
        template = 'complaints/student_complaint_list.html'
    
    context = {
        'complaints': complaints,
    }
    return render(request, template, context)


@login_required
def complaint_add(request):
    """Add new complaint (students only)"""
    try:
        # Try to find student by username matching
        student = Student.objects.filter(name__icontains=request.user.username).first()
        if not student:
            # If no exact match, try to find by user profile or create a basic student record
            student = Student.objects.filter(studentid=request.user.id).first()
        
        if not student:
            messages.error(request, 'Student profile not found. Please contact admin.')
            return redirect('dashboard')
        
        if request.method == 'POST':
            form = ComplaintForm(request.POST)
            if form.is_valid():
                try:
                    complaint = form.save(commit=False)
                    complaint.student = student
                    complaint.save()
                    
                    # Send email confirmation to student (only if email is configured)
                    email_sent = False
                    try:
                        from django.conf import settings
                        # Only attempt to send email if email is properly configured
                        if settings.EMAIL_HOST_USER and request.user.email:
                            from hostel_management.email_utils import send_complaint_confirmation_email
                            email_sent = send_complaint_confirmation_email(complaint, request.user.email)
                    except Exception as e:
                        print(f"Email sending failed: {str(e)}")
                        # Continue even if email fails
                    
                    if email_sent:
                        messages.success(request, 'Complaint submitted successfully! A confirmation email has been sent.')
                    else:
                        messages.success(request, 'Complaint submitted successfully!')
                    return redirect('complaint_list')
                except Exception as e:
                    messages.error(request, f'Error saving complaint: {str(e)}')
                    print(f"Error saving complaint: {str(e)}")
            else:
                # Form validation errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        else:
            form = ComplaintForm()
        
        # Determine template based on user role
        if is_admin(request.user):
            template = 'complaints/complaint_form.html'
        else:
            template = 'complaints/student_complaint_form.html'
        
        context = {
            'form': form,
            'title': 'Submit Complaint',
        }
        return render(request, template, context)
    except Exception as e:
        messages.error(request, f'Unexpected error: {str(e)}')
        print(f"Unexpected error in complaint_add: {str(e)}")
        import traceback
        traceback.print_exc()
        return redirect('dashboard')


@login_required
def complaint_detail(request, pk):
    """View complaint details"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permissions and determine template
    if is_admin(request.user):
        template = 'complaints/complaint_detail.html'
    else:
        # Try to find student by username matching
        student = Student.objects.filter(name__icontains=request.user.username).first()
        if not student:
            # If no exact match, try to find by user profile or create a basic student record
            student = Student.objects.filter(studentid=request.user.id).first()
        
        if not student:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard')
        
        if complaint.student != student:
            messages.error(request, 'You do not have permission to view this complaint.')
            return redirect('complaint_list')
        
        template = 'complaints/student_complaint_detail.html'
    
    context = {
        'complaint': complaint,
    }
    return render(request, template, context)


@login_required
@user_passes_test(is_admin)
def complaint_update(request, pk):
    """Update complaint status (admin only)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    old_status = complaint.status
    
    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            # Check if status changed to resolved
            status_changed_to_resolved = (old_status != 'resolved' and complaint.status == 'resolved')
            
            if complaint.status == 'resolved' and not complaint.resolved_at:
                complaint.resolved_at = timezone.now()
            complaint.save()
            
            # Send email notification if complaint was just resolved
            if status_changed_to_resolved:
                email_sent = False
                try:
                    from django.conf import settings
                    # Only attempt to send email if email is properly configured
                    if settings.EMAIL_HOST_USER:
                        from hostel_management.email_utils import send_complaint_resolution_email
                        from django.contrib.auth.models import User
                        
                        # Try to find user email by matching username with student name
                        user = User.objects.filter(username__iexact=complaint.student.name).first()
                        if not user:
                            # Try other methods to find user
                            user = User.objects.filter(id=complaint.student.studentid).first()
                        
                        if user and user.email:
                            email_sent = send_complaint_resolution_email(complaint, user.email)
                except Exception as e:
                    print(f"Email sending failed: {str(e)}")
                
                if email_sent:
                    messages.success(request, 'Complaint updated successfully! A resolution email has been sent to the student.')
                else:
                    messages.success(request, 'Complaint updated successfully!')
            else:
                messages.success(request, 'Complaint updated successfully!')
            
            return redirect('complaint_detail', pk=pk)
    else:
        form = ComplaintUpdateForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
        'title': 'Update Complaint',
    }
    return render(request, 'complaints/complaint_update.html', context)


@login_required
@user_passes_test(is_admin)
def complaint_resolve(request, pk):
    """Mark complaint as resolved and delete it (admin only)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        student_name = complaint.student.name
        complaint.delete()
        messages.success(request, f'Complaint from {student_name} marked as resolved and removed!')
        return redirect('complaint_list')
    
    context = {
        'complaint': complaint,
    }
    return render(request, 'complaints/complaint_confirm_resolve.html', context)


@login_required
def complaint_delete(request, pk):
    """Delete complaint (students can delete their own, admins can delete any)"""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    # Check permissions
    if not is_admin(request.user):
        # Students can only delete their own complaints
        student = Student.objects.filter(name__icontains=request.user.username).first()
        if not student:
            student = Student.objects.filter(studentid=request.user.id).first()
        
        if not student or complaint.student != student:
            messages.error(request, 'You do not have permission to delete this complaint.')
            return redirect('complaint_list')
    
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
        return redirect('complaint_list')
    
    context = {
        'complaint': complaint,
    }
    return render(request, 'complaints/complaint_confirm_delete.html', context)
