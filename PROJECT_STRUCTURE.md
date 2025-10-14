# Hostel Management System - Project Structure

```
hostelocity/
│
├── hostel_management/              # Main Django project folder
│   ├── __init__.py
│   ├── settings.py                 # Project settings with Supabase config
│   ├── urls.py                     # Main URL configuration
│   ├── views.py                    # Authentication and dashboard views
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
│
├── students/                       # Student management app
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Student forms
│   ├── models.py                   # Student and UserProfile models
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # Student URL patterns
│   └── views.py                    # Student views (CRUD operations)
│
├── rooms/                          # Room management app
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Room forms
│   ├── models.py                   # Room model with occupancy tracking
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # Room URL patterns
│   └── views.py                    # Room views (CRUD operations)
│
├── complaints/                     # Complaint system app
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Complaint forms
│   ├── models.py                   # Complaint model
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # Complaint URL patterns
│   └── views.py                    # Complaint views (CRUD operations)
│
├── payments/                       # Payment management app
│   ├── migrations/
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                    # Django admin configuration
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Payment forms
│   ├── models.py                   # Payment model
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # Payment URL patterns
│   └── views.py                    # Payment views (CRUD operations)
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template with Bootstrap 5
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard_admin.html        # Admin dashboard
│   ├── dashboard_student.html      # Student dashboard
│   │
│   ├── students/                   # Student templates
│   │   ├── student_list.html
│   │   ├── student_form.html
│   │   ├── student_detail.html
│   │   └── student_confirm_delete.html
│   │
│   ├── rooms/                      # Room templates
│   │   ├── room_list.html
│   │   ├── room_form.html
│   │   ├── room_detail.html
│   │   └── room_confirm_delete.html
│   │
│   ├── complaints/                 # Complaint templates
│   │   ├── complaint_list.html
│   │   ├── complaint_form.html
│   │   ├── complaint_detail.html
│   │   ├── complaint_update.html
│   │   └── complaint_confirm_delete.html
│   │
│   └── payments/                   # Payment templates
│       ├── payment_list.html
│       ├── payment_form.html
│       ├── payment_detail.html
│       ├── payment_update.html
│       └── payment_confirm_delete.html
│
├── static/                         # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css               # Custom CSS
│   └── js/
│       └── main.js                 # Custom JavaScript
│
├── media/                          # User uploaded files
│   └── student_photos/             # Student photos
│
├── staticfiles/                    # Collected static files (production)
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment configuration for Render
├── runtime.txt                     # Python version for deployment
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── BUILD_INSTRUCTIONS.txt          # Quick build guide
├── PROJECT_STRUCTURE.md            # This file
└── init_project.py                 # Project initialization script
```

## Database Schema

### UserProfile
- user (OneToOne → User)
- role (admin/student/staff)
- phone

### Student
- user (OneToOne → User, nullable)
- name
- roll_number (unique)
- course
- year
- email
- phone
- address
- photo (ImageField)
- room (ForeignKey → Room)
- date_of_admission
- is_active

### Room
- room_number (unique)
- room_type (single/double/triple/quad)
- capacity
- floor
- description
- is_full
- created_at

### Complaint
- student (ForeignKey → Student)
- category (maintenance/cleanliness/electricity/water/security/other)
- subject
- description
- status (pending/in_progress/resolved)
- created_at
- updated_at
- resolved_at
- admin_remarks

### Payment
- student (ForeignKey → Student)
- payment_type (monthly/semester/annual/admission/other)
- amount
- due_date
- payment_date
- status (pending/paid/overdue)
- transaction_id
- remarks
- created_at
- updated_at

## Key Features

### Authentication System
- Login/Logout functionality
- Registration for new students
- Role-based access control (Admin vs Student)
- Django's built-in User model extended with UserProfile

### Student Management
- Add, edit, delete, view students
- Upload student photos
- Assign students to rooms
- Automatic room occupancy tracking

### Room Management
- Add, edit, delete, view rooms
- Automatic capacity tracking
- Visual occupancy indicators
- Auto-mark rooms as full when capacity reached

### Complaint System
- Students can submit complaints
- Categorized complaints
- Status tracking (pending/in progress/resolved)
- Admin can add remarks and update status

### Payment/Fee Management
- Add fees for students
- Track payment status
- Multiple payment types
- Due date tracking
- Transaction ID recording

### Dashboard
- **Admin Dashboard**: Total students, occupied rooms, pending complaints, fees collected
- **Student Dashboard**: Personal info, room details, complaints, payments

### UI/UX
- Bootstrap 5 responsive design
- Modern gradient theme
- Role-based navigation
- Real-time alerts and notifications
- Clean and intuitive interface

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL (Supabase)
- **Frontend**: Django Templates + Bootstrap 5
- **Icons**: Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Static Files**: WhiteNoise
- **Deployment**: Gunicorn + Render

## Security Features

- CSRF protection
- Password hashing
- Role-based access control
- Login required decorators
- Admin-only views protection

## API Endpoints

### Authentication
- `/` - Home (redirects to login or dashboard)
- `/login/` - Login page
- `/logout/` - Logout
- `/register/` - Student registration
- `/dashboard/` - Role-based dashboard

### Students (Admin only)
- `/students/` - List all students
- `/students/add/` - Add new student
- `/students/<id>/` - Student details
- `/students/<id>/edit/` - Edit student
- `/students/<id>/delete/` - Delete student

### Rooms
- `/rooms/` - List all rooms
- `/rooms/add/` - Add new room (Admin)
- `/rooms/<id>/` - Room details
- `/rooms/<id>/edit/` - Edit room (Admin)
- `/rooms/<id>/delete/` - Delete room (Admin)

### Complaints
- `/complaints/` - List complaints (filtered by role)
- `/complaints/add/` - Submit complaint (Student)
- `/complaints/<id>/` - Complaint details
- `/complaints/<id>/update/` - Update status (Admin)
- `/complaints/<id>/delete/` - Delete complaint (Admin)

### Payments
- `/payments/` - List payments (filtered by role)
- `/payments/add/` - Add payment (Admin)
- `/payments/<id>/` - Payment details
- `/payments/<id>/edit/` - Edit payment (Admin)
- `/payments/<id>/update-status/` - Update payment status (Admin)
- `/payments/<id>/delete/` - Delete payment (Admin)

## Environment Variables

Required in `.env` file:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `SUPABASE_HOST` - Supabase database host
- `SUPABASE_DB_NAME` - Database name (usually 'postgres')
- `SUPABASE_USER` - Database user (usually 'postgres')
- `SUPABASE_PASSWORD` - Database password
- `SUPABASE_PORT` - Database port (usually 5432)
