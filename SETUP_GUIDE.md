# Hostel Management System - Setup Guide

## Prerequisites

- Python 3.11 or higher
- PostgreSQL (Supabase account)
- pip (Python package manager)

## Step-by-Step Setup

### 1. Clone/Download the Project

```bash
cd c:\Users\DIVYAM\Desktop\hostelocity
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/Mac**: `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase Database

1. Go to [Supabase](https://supabase.com/) and create a new project
2. Once created, go to **Settings** → **Database**
3. Copy your database credentials:
   - Host
   - Database name
   - User
   - Password
   - Port (usually 5432)

### 5. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=True
SUPABASE_HOST=db.xxxxxxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-supabase-password
SUPABASE_PORT=5432
```

To generate a SECRET_KEY, run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Create Static Files Directory

```bash
python manage.py collectstatic
```

Type 'yes' when prompted.

### 9. Run the Development Server

```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

## Initial Setup After First Run

### 1. Login as Admin

Go to `http://127.0.0.1:8000/admin/` and login with your superuser credentials.

### 2. Create User Profiles

For the superuser you created, you may need to manually create a UserProfile:
- Go to Django admin
- Navigate to User Profiles
- Create a new profile with role "admin" for your superuser

### 3. Add Rooms

Before adding students, create some rooms:
- Login to the main application
- Navigate to Rooms
- Click "Add Room"
- Add room details (room number, type, capacity, floor)

### 4. Add Students

- Navigate to Students
- Click "Add Student"
- Fill in student details
- Assign them to a room

### 5. Add Payments

- Navigate to Payments
- Click "Add Payment"
- Select student and add fee details

## User Roles

### Admin/Warden
- Full access to all features
- Can manage students, rooms, fees, and complaints
- Access to dashboard with statistics

### Student
- Can view their room details
- Can submit and view complaints
- Can view payment history
- Limited access to personal information

## Default URLs

- **Home**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Register**: http://127.0.0.1:8000/register/
- **Admin**: http://127.0.0.1:8000/admin/
- **Dashboard**: http://127.0.0.1:8000/dashboard/

## Troubleshooting

### Database Connection Error

If you get a database connection error:
1. Check your `.env` file has correct Supabase credentials
2. Ensure your IP is whitelisted in Supabase (Database Settings → Connection Pooling)
3. Try using the connection pooling URL instead

### Static Files Not Loading

Run:
```bash
python manage.py collectstatic --noinput
```

### Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Migration Errors

If migrations fail:
```bash
python manage.py migrate --run-syncdb
```

## Deployment to Render

### 1. Push to GitHub

Initialize git and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your-github-repo-url
git push -u origin main
```

### 2. Configure Render

1. Go to [Render](https://render.com/)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn hostel_management.wsgi`
5. Add environment variables from your `.env` file
6. Set `DEBUG=False` in production

### 3. Update Settings for Production

In `settings.py`, update:
```python
ALLOWED_HOSTS = ['your-app.onrender.com', 'localhost']
```

## Features Overview

✅ **Student Management** - Add, edit, delete, and list students  
✅ **Room Management** - Manage rooms with automatic capacity tracking  
✅ **Fee Management** - Track payments and dues  
✅ **Complaint System** - Students can submit complaints, admin can resolve  
✅ **Dashboard** - Role-based dashboards with statistics  
✅ **Authentication** - Secure login/logout with role-based access  
✅ **Responsive Design** - Modern Bootstrap 5 UI  

## Support

For issues or questions, please refer to the Django documentation:
- [Django Documentation](https://docs.djangoproject.com/)
- [Supabase Documentation](https://supabase.com/docs)
