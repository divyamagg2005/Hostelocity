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
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'You do not have admin privileges.')
            else:  # student login
                if hasattr(user, 'profile') and user.profile.role == 'student':
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
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
    messages.success(request, 'You have been logged out successfully.')
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
        # Count occupied rooms (rooms with allocations)
        from students.models import Allocation
        occupied_room_ids = Allocation.objects.values_list('room_id', flat=True).distinct()
        occupied_rooms = len(occupied_room_ids)
        available_rooms = total_rooms - occupied_rooms
        
        pending_complaints = Complaint.objects.filter(status='pending').count()
        
        # Get paid fees (case-insensitive to handle 'Paid', 'paid', 'PAID')
        from django.db.models import Q
        paid_fees = Fee.objects.filter(Q(status__iexact='paid') | Q(status__iexact='Paid'))
        fees_collected = paid_fees.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Recent complaints
        recent_complaints = Complaint.objects.all().order_by('-created_at')[:5]
        
        # Recent students (limit to 4 to prevent UI overflow)
        recent_students = Student.objects.all().order_by('-studentid')[:4]
        
        context = {
            'role': role,
            'total_students': total_students,
            'total_rooms': total_rooms,
            'occupied_rooms': occupied_rooms,
            'available_rooms': available_rooms,
            'pending_complaints': pending_complaints,
            'fees_collected': fees_collected,
            'recent_complaints': recent_complaints,
            'recent_students': recent_students,
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
                my_payments = Fee.objects.filter(student=student).order_by('-due_date')[:5]
                pending_payments = Fee.objects.filter(student=student, status='Pending').count()
                
                context = {
                    'role': role,
                    'student': student,
                    'student_profile': student_profile,
                    'my_complaints': my_complaints,
                    'my_payments': my_payments,
                    'pending_payments': pending_payments,
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
