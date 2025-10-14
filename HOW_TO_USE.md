# 🏢 Hostelocity - Complete Usage Guide

## 📋 Table of Contents
1. [What is Hostelocity?](#what-is-hostelocity)
2. [Who is it for?](#who-is-it-for)
3. [How it Works](#how-it-works)
4. [Setup & Installation](#setup--installation)
5. [User Guide](#user-guide)
6. [Testing Guide](#testing-guide)
7. [API Endpoints](#api-endpoints)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 What is Hostelocity?

**Hostelocity** is a **complete Hostel Management System** built with Django and Supabase PostgreSQL. It's a web-based application that helps manage hostel operations including:

- 👨‍🎓 **Student Management** - Track student information, photos, and details
- 🏠 **Room Management** - Manage rooms, capacity, and allocations
- 💰 **Fee Management** - Track hostel fees and payment status
- 🧾 **Complaint System** - Students can submit complaints, admins can resolve them
- 📊 **Dashboard** - Real-time statistics and insights

---

## 👥 Who is it for?

### **Primary Users:**

1. **Hostel Administrators/Wardens** 
   - Manage all hostel operations
   - Add/edit/delete students and rooms
   - Track fees and payments
   - Resolve student complaints
   - View comprehensive dashboard with statistics

2. **Students**
   - View their room details
   - Check payment status
   - Submit complaints
   - View personal dashboard

3. **Educational Institutions**
   - Universities with hostel facilities
   - Colleges managing student accommodations
   - Boarding schools
   - Training centers with residential facilities

### **Use Cases:**
- Replace manual hostel record keeping
- Digitize student accommodation management
- Track fee payments efficiently
- Provide transparent complaint resolution system
- Generate reports and statistics

---

## ⚙️ How it Works

### **Architecture:**

```
┌─────────────────────────────────────────────────┐
│           USER (Browser)                        │
│  Admin Dashboard  |  Student Dashboard          │
└─────────────┬───────────────────────────────────┘
              │
              │ HTTP Requests
              ▼
┌─────────────────────────────────────────────────┐
│         DJANGO WEB APPLICATION                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Students │  │  Rooms   │  │Complaints│     │
│  │   App    │  │   App    │  │   App    │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│  ┌──────────┐  ┌──────────┐                    │
│  │ Payments │  │   Auth   │                    │
│  │   App    │  │  System  │                    │
│  └──────────┘  └──────────┘                    │
└─────────────┬───────────────────────────────────┘
              │
              │ SQL Queries
              ▼
┌─────────────────────────────────────────────────┐
│      SUPABASE POSTGRESQL DATABASE               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ Student  │  │   Room   │  │ Hostel   │     │
│  │  Table   │  │  Table   │  │  Table   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Fee    │  │Allocation│  │Complaint │     │
│  │  Table   │  │  Table   │  │  Table   │     │
│  └──────────┘  └──────────┘  └──────────┘     │
└─────────────────────────────────────────────────┘
```

### **Database Schema:**

**Core Tables:**
1. **Student** - Stores student information (name, gender, department, phone)
2. **Hostel** - Stores hostel information (name, location, total rooms)
3. **Room** - Stores room details (room number, capacity, type)
4. **Allocation** - Links students to rooms with allocation dates
5. **Fee** - Tracks student fees (amount, due date, status)
6. **Complaint** - Manages student complaints (category, status, remarks)

### **Key Features:**

#### **Role-Based Access Control:**
- **Admin Role**: Full access to all features
- **Student Role**: Limited access to personal data only
- **Staff Role**: Configurable access (future enhancement)

#### **Automatic Calculations:**
- Room occupancy percentage
- Available spaces in rooms
- Total fees collected
- Pending complaints count

#### **Data Relationships:**
- Students → Allocations → Rooms (Many-to-Many through Allocation)
- Students → Fees (One-to-Many)
- Students → Complaints (One-to-Many)
- Hostels → Rooms (One-to-Many)

---

## 🚀 Setup & Installation

### **Prerequisites:**
- Python 3.11 or higher
- pip (Python package manager)
- Supabase account (free tier available)
- Git (optional, for version control)

### **Step-by-Step Installation:**

#### **1. Clone or Download the Project**
```bash
# If using Git
git clone <repository-url>
cd hostelocity

# Or download ZIP and extract
```

#### **2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Django 4.2+ (Web framework)
- psycopg2-binary (PostgreSQL adapter)
- python-decouple (Environment variables)
- Pillow (Image handling)
- django-crispy-forms (Form styling)
- crispy-bootstrap5 (Bootstrap 5 support)
- gunicorn (Production server)
- whitenoise (Static file serving)

#### **4. Setup Supabase Database**

1. **Create Supabase Account:**
   - Go to [supabase.com](https://supabase.com)
   - Sign up for free account
   - Create a new project

2. **Get Database Credentials:**
   - Go to Project Settings → Database
   - Note down:
     - Host (e.g., `db.xxxxx.supabase.co`)
     - Database name (usually `postgres`)
     - User (usually `postgres`)
     - Password (your project password)
     - Port (usually `5432`)

3. **Create Database Tables:**
   - Go to SQL Editor in Supabase
   - Run the following SQL:

```sql
-- Create Hostel table
CREATE TABLE hostel (
    hostelid SERIAL PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    totalrooms INTEGER
);

-- Create Room table
CREATE TABLE room (
    roomid SERIAL PRIMARY KEY,
    hostelid INTEGER REFERENCES hostel(hostelid),
    roomnumber VARCHAR(10),
    capacity INTEGER,
    type VARCHAR(20)
);

-- Create Student table
CREATE TABLE student (
    studentid SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    department VARCHAR(50),
    phone VARCHAR(15)
);

-- Create Allocation table
CREATE TABLE allocation (
    allocationid SERIAL PRIMARY KEY,
    studentid INTEGER REFERENCES student(studentid),
    roomid INTEGER REFERENCES room(roomid),
    date_of_allocation DATE
);

-- Create Fee table
CREATE TABLE fee (
    feeid SERIAL PRIMARY KEY,
    studentid INTEGER REFERENCES student(studentid),
    amount DECIMAL(10, 2),
    duedate DATE,
    status VARCHAR(20)
);

-- Insert sample hostel
INSERT INTO hostel (name, location, totalrooms) 
VALUES ('Main Hostel', 'Campus North', 50);
```

#### **5. Configure Environment Variables**

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Supabase Database Configuration
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-supabase-password
SUPABASE_PORT=5432
```

**To generate a SECRET_KEY:**
```python
# Run in Python shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### **6. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the `Complaint` table and Django's internal tables (User, Session, etc.)

#### **7. Create Superuser (Admin)**
```bash
python manage.py createsuperuser
```

Follow prompts to create admin account:
- Username: admin (or your choice)
- Email: admin@example.com
- Password: (secure password)

#### **8. Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

#### **9. Run Development Server**
```bash
python manage.py runserver
```

#### **10. Access the Application**
Open browser and go to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📖 User Guide

### **For Administrators:**

#### **1. First Login**
1. Go to http://127.0.0.1:8000/
2. Login with superuser credentials
3. You'll see the Admin Dashboard

#### **2. Admin Dashboard Overview**
The dashboard shows:
- **Total Students**: Count of all students
- **Occupied Rooms**: Number of rooms with students
- **Pending Complaints**: Unresolved complaints
- **Fees Collected**: Total fees collected this month
- **Recent Complaints**: Last 5 complaints
- **Recent Students**: Last 5 added students
- **Quick Actions**: Buttons to add students, rooms, payments

#### **3. Managing Students**

**Add New Student:**
1. Click "Students" in navigation or "Add Student" button
2. Fill in student details:
   - Name (required)
   - Gender (optional)
   - Department (optional)
   - Phone (optional)
3. Click "Save"

**View Students:**
1. Go to "Students" → "Student List"
2. See all students in a table
3. Click on student name to view details

**Edit Student:**
1. Go to student detail page
2. Click "Edit" button
3. Update information
4. Click "Save"

**Delete Student:**
1. Go to student detail page
2. Click "Delete" button
3. Confirm deletion

#### **4. Managing Rooms**

**Add New Room:**
1. Click "Rooms" → "Add Room"
2. Fill in:
   - Select Hostel
   - Room Number (e.g., "101", "A-201")
   - Capacity (number of students)
   - Type (e.g., "Single", "Double", "Triple")
3. Click "Save"

**View Rooms:**
1. Go to "Rooms" → "Room List"
2. See all rooms with:
   - Room number
   - Capacity
   - Current occupancy
   - Available spaces
   - Occupancy percentage (progress bar)

**Allocate Student to Room:**
1. Go to "Allocations" (or create allocation form)
2. Select Student
3. Select Room
4. Set Allocation Date
5. Click "Save"

**View Room Details:**
1. Click on room in room list
2. See:
   - Room information
   - Current occupancy
   - List of students in room

#### **5. Managing Fees/Payments**

**Add Fee Entry:**
1. Go to "Payments" → "Add Payment"
2. Fill in:
   - Select Student
   - Amount (e.g., 5000)
   - Due Date
   - Status (Pending/Paid)
3. Click "Save"

**View Payments:**
1. Go to "Payments" → "Payment List"
2. See all fee entries with:
   - Student name
   - Amount
   - Due date
   - Status (color-coded)

**Update Payment Status:**
1. Go to payment detail page
2. Click "Update Status"
3. Change status to "Paid"
4. Add transaction ID (optional)
5. Click "Save"

#### **6. Managing Complaints**

**View All Complaints:**
1. Go to "Complaints" → "Complaint List"
2. See all complaints from all students

**Update Complaint:**
1. Click on complaint to view details
2. Click "Update Status"
3. Change status:
   - Pending → In Progress → Resolved
4. Add admin remarks
5. Click "Save"

**Delete Complaint:**
1. Go to complaint detail page
2. Click "Delete" button
3. Confirm deletion

### **For Students:**

#### **1. Student Login**
1. Go to http://127.0.0.1:8000/
2. Login with student credentials
3. You'll see Student Dashboard

#### **2. Student Dashboard Overview**
The dashboard shows:
- **Profile Information**: Name, department, phone
- **Room Details**: Room number, type, capacity, occupancy
- **Pending Payments**: Count of unpaid fees
- **My Complaints**: Count of submitted complaints
- **Recent Complaints**: Last 5 complaints
- **Recent Payments**: Last 5 fee entries

#### **3. Viewing Room Details**
1. Room information is displayed on dashboard
2. Shows:
   - Room number
   - Room type
   - Floor (if available)
   - Capacity
   - Current occupancy

#### **4. Submitting Complaints**
1. Click "Submit Complaint" button
2. Fill in:
   - Category (Maintenance, Cleanliness, Electricity, Water, Security, Other)
   - Subject (brief title)
   - Description (detailed explanation)
3. Click "Submit"
4. View submitted complaints in "My Complaints"

#### **5. Checking Payment Status**
1. Click "View Payments"
2. See all your fee entries:
   - Amount
   - Due date
   - Status (Pending/Paid)
3. Status color codes:
   - 🔴 Red = Pending
   - 🟢 Green = Paid

---

## 🧪 Testing Guide

### **Manual Testing Checklist:**

#### **1. Authentication Testing**
- [ ] Admin can login
- [ ] Student can login
- [ ] Invalid credentials show error
- [ ] Logout works correctly

#### **2. Admin Dashboard Testing**
- [ ] Statistics display correctly
- [ ] Recent complaints show
- [ ] Recent students show
- [ ] Quick action buttons work

#### **3. Student Management Testing**
- [ ] Can add new student
- [ ] Can view student list
- [ ] Can view student details
- [ ] Can edit student
- [ ] Can delete student
- [ ] Form validation works

#### **4. Room Management Testing**
- [ ] Can add new room
- [ ] Can view room list
- [ ] Occupancy percentage calculates correctly
- [ ] Can view room details
- [ ] Can edit room
- [ ] Can delete room

#### **5. Allocation Testing**
- [ ] Can allocate student to room
- [ ] Room occupancy updates automatically
- [ ] Cannot over-allocate (exceed capacity)
- [ ] Student shows correct room

#### **6. Fee Management Testing**
- [ ] Can add fee entry
- [ ] Can view all payments (admin)
- [ ] Student sees only their payments
- [ ] Can update payment status
- [ ] Status changes reflect correctly

#### **7. Complaint Testing**
- [ ] Student can submit complaint
- [ ] Admin sees all complaints
- [ ] Student sees only their complaints
- [ ] Admin can update status
- [ ] Admin can add remarks
- [ ] Status workflow works (Pending → In Progress → Resolved)

#### **8. Role-Based Access Testing**
- [ ] Admin can access all pages
- [ ] Student cannot access admin pages
- [ ] Student cannot see other students' data
- [ ] Proper redirects on unauthorized access

### **Test Data Creation:**

Run this in Django shell (`python manage.py shell`):

```python
from students.models import Student
from rooms.models import Hostel, Room, Allocation
from payments.models import Fee
from datetime import date

# Create hostel
hostel = Hostel.objects.create(
    name='Test Hostel',
    location='Campus',
    totalrooms=10
)

# Create rooms
for i in range(1, 6):
    Room.objects.create(
        hostelid=hostel,
        roomnumber=f'10{i}',
        capacity=2,
        type='Double'
    )

# Create students
for i in range(1, 11):
    Student.objects.create(
        name=f'Test Student {i}',
        gender='Male' if i % 2 == 0 else 'Female',
        department='Computer Science',
        phone=f'98765432{i:02d}'
    )

# Create allocations
students = Student.objects.all()[:10]
rooms = Room.objects.all()[:5]
for i, student in enumerate(students):
    Allocation.objects.create(
        student=student,
        room=rooms[i // 2],  # 2 students per room
        date_of_allocation=date.today()
    )

# Create fees
for student in students:
    Fee.objects.create(
        studentid=student,
        amount=5000.00,
        duedate=date.today(),
        status='Pending'
    )

print("Test data created successfully!")
```

### **Automated Testing:**

Run Django tests:
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test students
python manage.py test rooms
python manage.py test complaints
python manage.py test payments

# Run with verbosity
python manage.py test --verbosity=2
```

### **Performance Testing:**

Check database queries:
```python
# In Django shell
from django.db import connection
from django.test.utils import override_settings

# Enable query logging
from django.conf import settings
settings.DEBUG = True

# Run your view/query
# Then check queries
print(len(connection.queries))
for query in connection.queries:
    print(query['sql'])
```

---

## 🔌 API Endpoints

### **Authentication Endpoints:**

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET/POST | `/` | Home/Login page | Public |
| POST | `/login/` | Login authentication | Public |
| GET | `/logout/` | Logout user | Authenticated |
| GET/POST | `/register/` | Student registration | Public |
| GET | `/dashboard/` | Role-based dashboard | Authenticated |

### **Student Endpoints:**

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/students/` | List all students | Admin |
| GET | `/students/add/` | Add student form | Admin |
| POST | `/students/add/` | Create student | Admin |
| GET | `/students/<id>/` | Student details | Admin |
| GET | `/students/<id>/edit/` | Edit student form | Admin |
| POST | `/students/<id>/edit/` | Update student | Admin |
| POST | `/students/<id>/delete/` | Delete student | Admin |

### **Room Endpoints:**

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/rooms/` | List all rooms | All |
| GET | `/rooms/add/` | Add room form | Admin |
| POST | `/rooms/add/` | Create room | Admin |
| GET | `/rooms/<id>/` | Room details | All |
| GET | `/rooms/<id>/edit/` | Edit room form | Admin |
| POST | `/rooms/<id>/edit/` | Update room | Admin |
| POST | `/rooms/<id>/delete/` | Delete room | Admin |

### **Complaint Endpoints:**

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/complaints/` | List complaints | All (filtered) |
| GET | `/complaints/add/` | Add complaint form | Student |
| POST | `/complaints/add/` | Create complaint | Student |
| GET | `/complaints/<id>/` | Complaint details | Owner/Admin |
| GET | `/complaints/<id>/update/` | Update form | Admin |
| POST | `/complaints/<id>/update/` | Update complaint | Admin |
| POST | `/complaints/<id>/delete/` | Delete complaint | Admin |

### **Payment Endpoints:**

| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/payments/` | List payments | All (filtered) |
| GET | `/payments/add/` | Add payment form | Admin |
| POST | `/payments/add/` | Create payment | Admin |
| GET | `/payments/<id>/` | Payment details | Owner/Admin |
| GET | `/payments/<id>/edit/` | Edit payment form | Admin |
| POST | `/payments/<id>/edit/` | Update payment | Admin |
| POST | `/payments/<id>/delete/` | Delete payment | Admin |

---

## 🐛 Troubleshooting

### **Common Issues:**

#### **1. Database Connection Error**
```
Error: could not connect to server
```
**Solution:**
- Check `.env` file has correct Supabase credentials
- Verify Supabase project is active
- Check if your IP is whitelisted in Supabase settings
- Test connection: `psql -h <host> -U postgres -d postgres`

#### **2. Static Files Not Loading**
```
404 errors for CSS/JS files
```
**Solution:**
```bash
python manage.py collectstatic --noinput
```
- Ensure `STATIC_ROOT` is set in settings.py
- Check `STATICFILES_DIRS` includes static folder

#### **3. Import Errors**
```
ModuleNotFoundError: No module named 'django'
```
**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

#### **4. Migration Errors**
```
django.db.utils.ProgrammingError: relation does not exist
```
**Solution:**
```bash
# Clear migrations (if needed)
python clear_migrations.py

# Run migrations again
python manage.py makemigrations
python manage.py migrate
```

#### **5. Permission Denied Errors**
```
403 Forbidden
```
**Solution:**
- Check user role (admin vs student)
- Verify login status
- Check view decorators (`@login_required`, `@user_passes_test`)

#### **6. Image Upload Not Working**
```
Error uploading student photo
```
**Solution:**
- Ensure `media` folder exists
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings.py
- Verify file permissions on media folder
- Check file size limits

#### **7. Port Already in Use**
```
Error: That port is already in use
```
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### **Debug Mode:**

Enable detailed error messages:
```python
# In .env file
DEBUG=True
```

View Django debug toolbar (optional):
```bash
pip install django-debug-toolbar
```

### **Logging:**

Check Django logs:
```python
# In settings.py, add:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

---

## 🚀 Deployment

### **Deploy to Render:**

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Create Web Service on Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Name**: hostelocity
     - **Environment**: Python 3
     - **Build Command**: 
       ```bash
       pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
       ```
     - **Start Command**: 
       ```bash
       gunicorn hostel_management.wsgi
       ```

3. **Set Environment Variables:**
   - Add all variables from `.env` file
   - Set `DEBUG=False`
   - Set `ALLOWED_HOSTS=your-app.onrender.com`

4. **Deploy!**
   - Click "Create Web Service"
   - Wait for deployment
   - Access at: `https://your-app.onrender.com`

---

## 📞 Support

### **Documentation Files:**
- `README.md` - Project overview
- `SETUP_GUIDE.md` - Detailed setup
- `PROJECT_STRUCTURE.md` - Architecture details
- `TESTING_GUIDE.md` - Testing procedures
- `FEATURES.md` - Complete feature list
- `QUICKSTART.md` - Quick start guide

### **Need Help?**
1. Check documentation files
2. Review error messages carefully
3. Check Django documentation: [docs.djangoproject.com](https://docs.djangoproject.com)
4. Check Supabase documentation: [supabase.com/docs](https://supabase.com/docs)

---

## 🎉 Summary

**Hostelocity** is a production-ready hostel management system with:
- ✅ Complete CRUD operations
- ✅ Role-based access control
- ✅ Automatic calculations
- ✅ Modern responsive UI
- ✅ Supabase PostgreSQL integration
- ✅ Ready for deployment
- ✅ Comprehensive documentation

**Start managing your hostel efficiently today!** 🏢
