from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Fee
from .forms import FeeForm, FeeUpdateForm
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
def payment_list(request):
    """List payments based on user role"""
    if is_admin(request.user):
        # Admin sees all payments
        payments = Fee.objects.all()
    else:
        # Student sees only their payments
        try:
            student = Student.objects.get(user=request.user)
            payments = Fee.objects.filter(student=student)
        except Student.DoesNotExist:
            payments = []
            messages.warning(request, 'Student profile not found.')
    
    context = {
        'payments': payments,
    }
    return render(request, 'payments/payment_list.html', context)


@login_required
@user_passes_test(is_admin)
def payment_add(request):
    """Add new payment (admin only)"""
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f'Payment added for {payment.student.name}!')
            return redirect('payment_list')
    else:
        form = FeeForm()
    
    context = {
        'form': form,
        'title': 'Add Payment',
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
def payment_detail(request, pk):
    """View payment details"""
    payment = get_object_or_404(Fee, pk=pk)
    
    # Check permissions
    if not is_admin(request.user):
        try:
            student = Student.objects.get(user=request.user)
            if payment.student != student:
                messages.error(request, 'You do not have permission to view this payment.')
                return redirect('payment_list')
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_detail.html', context)


@login_required
@user_passes_test(is_admin)
def payment_edit(request, pk):
    """Edit payment (admin only)"""
    payment = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        form = FeeForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment updated successfully!')
            return redirect('payment_detail', pk=pk)
    else:
        form = FeeForm(instance=payment)
    
    context = {
        'form': form,
        'title': 'Edit Payment',
        'payment': payment,
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
@user_passes_test(is_admin)
def payment_update_status(request, pk):
    """Update payment status (admin only)"""
    payment = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        form = FeeUpdateForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            # Update status to Paid if marked as paid
            if payment.status == 'Paid':
                pass  # Fee model doesn't have payment_date field
            payment.save()
            messages.success(request, 'Payment status updated successfully!')
            return redirect('payment_detail', pk=pk)
    else:
        form = FeeUpdateForm(instance=payment)
    
    context = {
        'form': form,
        'payment': payment,
        'title': 'Update Payment Status',
    }
    return render(request, 'payments/payment_update.html', context)


@login_required
@user_passes_test(is_admin)
def payment_delete(request, pk):
    """Delete payment (admin only)"""
    payment = get_object_or_404(Fee, pk=pk)
    
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Payment deleted successfully!')
        return redirect('payment_list')
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/payment_confirm_delete.html', context)
