# Testing Guide - Hostel Management System

## Manual Testing Checklist

### 1. Authentication Testing

#### Login Functionality
- [ ] Admin can login with correct credentials
- [ ] Student can login with correct credentials
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard
- [ ] Logout functionality works correctly

#### Registration Functionality
- [ ] New users can register
- [ ] Password confirmation validation works
- [ ] Duplicate username/email prevention works
- [ ] Successful registration redirects to login
- [ ] Default role 'student' is assigned

### 2. Admin Dashboard Testing

- [ ] Total students count is accurate
- [ ] Occupied rooms count is correct
- [ ] Pending complaints count is accurate
- [ ] Fees collected calculation is correct
- [ ] Recent complaints list displays correctly
- [ ] Recent students list displays correctly
- [ ] Quick action buttons work

### 3. Student Dashboard Testing

- [ ] Student profile information displays correctly
- [ ] Student photo displays (or placeholder)
- [ ] Room information is shown correctly
- [ ] Pending payments count is accurate
- [ ] Recent complaints list works
- [ ] Recent payments list works
- [ ] Quick action buttons work

### 4. Student Management (Admin Only)

#### Add Student
- [ ] Form displays all required fields
- [ ] Form validation works (required fields)
- [ ] Photo upload works
- [ ] Room assignment works
- [ ] Success message displays
- [ ] Student appears in list

#### Edit Student
- [ ] Edit form pre-fills with current data
- [ ] Changes are saved correctly
- [ ] Photo update works
- [ ] Room change updates occupancy

#### Delete Student
- [ ] Confirmation dialog appears
- [ ] Student is deleted successfully
- [ ] Room occupancy updates

#### View Student
- [ ] All student details display correctly
- [ ] Photo displays correctly
- [ ] Room link works
- [ ] Edit/Delete buttons work (admin only)

### 5. Room Management

#### List Rooms
- [ ] All rooms display correctly
- [ ] Occupancy progress bar shows correct percentage
- [ ] Status badges (Full/Available) are accurate
- [ ] Statistics (Total/Occupied/Available) are correct

#### Add Room
- [ ] Form validation works
- [ ] Room is created successfully
- [ ] Success message displays

#### Edit Room
- [ ] Form pre-fills correctly
- [ ] Changes save successfully

#### Delete Room
- [ ] Warning shows if students are assigned
- [ ] Confirmation dialog works
- [ ] Room is deleted

#### View Room Details
- [ ] Room information displays correctly
- [ ] Occupancy percentage is accurate
- [ ] Students in room list correctly
- [ ] Links to student profiles work

### 6. Complaint System

#### Submit Complaint (Student)
- [ ] Student can access complaint form
- [ ] All categories are available
- [ ] Form validation works
- [ ] Complaint is created successfully
- [ ] Student can see their complaint in list

#### View Complaints
- [ ] Admin sees all complaints
- [ ] Student sees only their complaints
- [ ] Status badges display correctly
- [ ] Filters work properly

#### Update Complaint (Admin)
- [ ] Admin can update status
- [ ] Admin can add remarks
- [ ] Resolved_at timestamp updates when resolved
- [ ] Changes reflect in complaint detail

#### Delete Complaint (Admin)
- [ ] Confirmation dialog appears
- [ ] Complaint is deleted successfully

### 7. Payment Management

#### Add Payment (Admin)
- [ ] Form displays all fields
- [ ] Student selection works
- [ ] Amount validation works
- [ ] Date picker works
- [ ] Payment is created successfully

#### View Payments
- [ ] Admin sees all payments
- [ ] Student sees only their payments
- [ ] Status badges display correctly
- [ ] Amount formatting is correct

#### Update Payment Status (Admin)
- [ ] Admin can update payment status
- [ ] Payment_date auto-fills when marked as paid
- [ ] Transaction ID can be added
- [ ] Changes save successfully

#### Edit Payment (Admin)
- [ ] Form pre-fills correctly
- [ ] All fields can be edited
- [ ] Changes save successfully

#### Delete Payment (Admin)
- [ ] Confirmation dialog appears
- [ ] Payment is deleted successfully

### 8. Role-Based Access Control

#### Admin Access
- [ ] Can access all pages
- [ ] Can see all CRUD buttons
- [ ] Can perform all operations

#### Student Access
- [ ] Cannot access admin pages
- [ ] Cannot see admin-only buttons
- [ ] Can only view own data
- [ ] Redirects when trying to access restricted pages

### 9. UI/UX Testing

- [ ] Navigation menu displays correctly
- [ ] All links work properly
- [ ] Responsive design works on mobile
- [ ] Buttons have proper styling
- [ ] Forms are user-friendly
- [ ] Alert messages display and dismiss
- [ ] Cards and tables render properly
- [ ] Icons display correctly

### 10. Database Integration

- [ ] Data persists after refresh
- [ ] Relationships work correctly (Student-Room, etc.)
- [ ] Auto-increment IDs work
- [ ] Cascade deletes work properly
- [ ] Date/time fields store correctly

## Automated Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test students
python manage.py test rooms
python manage.py test complaints
python manage.py test payments
```

### Test Coverage

To check test coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report
```

## Performance Testing

### Database Queries
- [ ] Pages load within 2 seconds
- [ ] No N+1 query problems
- [ ] Proper use of select_related and prefetch_related

### Load Testing
- [ ] System handles multiple concurrent users
- [ ] No memory leaks
- [ ] Proper caching where needed

## Security Testing

### Authentication
- [ ] Passwords are hashed (not stored in plain text)
- [ ] Login required for protected pages
- [ ] Role-based access is enforced
- [ ] CSRF tokens are present in forms

### Data Validation
- [ ] Form inputs are validated
- [ ] SQL injection prevention works
- [ ] XSS prevention works
- [ ] File upload validation works

## Browser Compatibility

Test on:
- [ ] Google Chrome
- [ ] Mozilla Firefox
- [ ] Microsoft Edge
- [ ] Safari (if on Mac)

## Test Data Setup

### Create Test Data Script

```python
# Add to init_project.py or create separate script
from django.contrib.auth.models import User
from students.models import Student, UserProfile
from rooms.models import Room
from payments.models import Payment
from complaints.models import Complaint
from datetime import date, timedelta

def create_test_data():
    # Create admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@hostel.com',
        password='admin123'
    )
    UserProfile.objects.create(user=admin, role='admin')
    
    # Create rooms
    for i in range(1, 11):
        Room.objects.create(
            room_number=f'R{i:03d}',
            room_type='double',
            capacity=2,
            floor=(i-1)//4 + 1
        )
    
    # Create students
    rooms = Room.objects.all()
    for i in range(1, 21):
        user = User.objects.create_user(
            username=f'student{i}',
            email=f'student{i}@hostel.com',
            password='student123'
        )
        UserProfile.objects.create(user=user, role='student')
        
        Student.objects.create(
            user=user,
            name=f'Student {i}',
            roll_number=f'2024{i:03d}',
            course='Computer Science',
            year='2',
            email=f'student{i}@hostel.com',
            phone=f'123456{i:04d}',
            address=f'Address {i}',
            room=rooms[i//2] if i <= 20 else None
        )
```

## Common Issues and Solutions

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: Database connection error
**Solution**: Check .env file credentials and Supabase connection

### Issue: Image upload not working
**Solution**: Ensure media folder exists and MEDIA_ROOT is configured

### Issue: Permission denied errors
**Solution**: Check file permissions and user roles

### Issue: 404 errors
**Solution**: Verify URL patterns and ensure apps are in INSTALLED_APPS

## Continuous Testing

1. Test after every major feature addition
2. Test before deploying to production
3. Test after database migrations
4. Test with real user scenarios
5. Gather user feedback and iterate

## Bug Reporting Template

When reporting bugs, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Browser and OS information
- Error messages (if any)
