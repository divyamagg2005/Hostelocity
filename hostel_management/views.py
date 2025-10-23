from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from students.models import Student, UserProfile
from rooms.models import Room
from complaints.models import Complaint
from payments.models import Fee
from datetime import datetime


def home(request):
    """Home page - redirects to dashboard if logged in"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def login_view(request):
    """Login view for all users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type', 'admin')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has the correct role for the login type
            if login_type == 'admin':
                if user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin'):
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'You do not have admin privileges.')
            else:  # student login
                if hasattr(user, 'profile') and user.profile.role == 'student':
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'You do not have student privileges.')
        else:
            if login_type == 'student':
                messages.error(request, 'Invalid username or password. If you are a new student, please create an account.')
            else:
                messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')


def register_view(request):
    """Registration view for new students"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create user profile (default role is student)
        UserProfile.objects.create(user=user, role='student')
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


@login_required
def dashboard(request):
    """Dashboard view - different content based on user role"""
    # Check if user is superuser first (no profile needed)
    if request.user.is_superuser:
        role = 'admin'
    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            role = user_profile.role
        except UserProfile.DoesNotExist:
            # Create a default student profile
            UserProfile.objects.create(user=request.user, role='student')
            role = 'student'
    
    if role == 'admin' or request.user.is_superuser:
        # Admin dashboard with statistics
        total_students = Student.objects.count()
        total_rooms = Room.objects.count()
        
        # Count occupied and available rooms correctly
        # Occupied = completely full (current_occupancy == capacity)
        # Available = has at least one bed free (current_occupancy < capacity)
        from students.models import Allocation
        occupied_rooms = 0
        available_rooms = 0
        
        all_rooms = Room.objects.all()
        for room in all_rooms:
            current_occupancy = Allocation.objects.filter(room=room).count()
            if current_occupancy >= room.capacity:
                occupied_rooms += 1
            else:
                available_rooms += 1
        
        pending_complaints = Complaint.objects.filter(status='pending').count()
        
        # Get paid fees (case-insensitive to handle 'Paid', 'paid', 'PAID')
        from django.db.models import Q
        paid_fees = Fee.objects.filter(Q(status__iexact='paid') | Q(status__iexact='Paid'))
        fees_collected = paid_fees.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Recent complaints
        recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
        
        # Get empty/available rooms (rooms that are not fully occupied)
        from django.db.models import Count
        empty_rooms = []
        all_rooms = Room.objects.select_related('hostelid').all()
        
        for room in all_rooms:
            # Count current allocations for this room
            current_allocations = Allocation.objects.filter(room=room).count()
            available_beds = room.capacity - current_allocations
            
            # Only include rooms with available beds
            if available_beds > 0:
                room.available_beds = available_beds
                empty_rooms.append(room)
        
        # Limit to 5 rooms for display
        empty_rooms = empty_rooms[:5]
        
        context = {
            'role': role,
            'total_students': total_students,
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'pending_complaints': pending_complaints,
            'fees_collected': fees_collected,
            'recent_complaints': recent_complaints,
            'empty_rooms': empty_rooms,
        }
        return render(request, 'dashboard_admin.html', context)
    
    else:
        # Student dashboard
        try:
            # Try to find student by username matching
            student = Student.objects.filter(name__icontains=request.user.username).first()
            if not student:
                # If no exact match, try to find by user profile or create a basic student record
                student = Student.objects.filter(studentid=request.user.id).first()
            
            if student:
                # Get or create student profile
                from students.models import StudentProfile
                try:
                    student_profile = StudentProfile.objects.get(student=student)
                except StudentProfile.DoesNotExist:
                    student_profile = StudentProfile.objects.create(student=student)
                
                my_complaints = Complaint.objects.filter(student=student).order_by('-created_at')[:5]
                
                # Get pending/overdue payments (not paid)
                pending_payments_list = Fee.objects.filter(
                    studentid=student
                ).exclude(
                    status__iexact='paid'
                ).order_by('-duedate')[:5]
                pending_payments_count = Fee.objects.filter(studentid=student).exclude(status__iexact='paid').count()
                
                # Get only paid payments for recent payments
                paid_payments = Fee.objects.filter(
                    studentid=student, 
                    status__iexact='paid'
                ).order_by('-duedate')[:5]
                
                context = {
                    'role': role,
                    'student': student,
                    'student_profile': student_profile,
                    'my_complaints': my_complaints,
                    'pending_payments_list': pending_payments_list,
                    'pending_payments_count': pending_payments_count,
                    'paid_payments': paid_payments,
                }
                return render(request, 'dashboard_student.html', context)
            else:
                # Student profile not found - show message to contact admin
                messages.warning(request, 'Your student profile is not found in the system. Please contact the administrator to create your profile.')
                context = {
                    'role': role,
                    'student': None,
                }
                return render(request, 'dashboard_student.html', context)
        except Exception as e:
            # Handle any other errors
            messages.error(request, f'Error loading student dashboard: {str(e)}')
            context = {
                'role': role,
                'student': None,
            }
            return render(request, 'dashboard_student.html', context)
