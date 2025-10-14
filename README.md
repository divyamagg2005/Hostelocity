# Hostel Management System

A complete hostel management system built with Django and Supabase PostgreSQL.

## Features

- **Student Management**: Add, edit, delete, and list students
- **Room Management**: Manage rooms with capacity tracking
- **Fee Management**: Track hostel fees and payments
- **Complaint System**: Students can log complaints, admin can resolve them
- **Dashboard**: Admin dashboard with key metrics
- **Role-based Access**: Admin/Warden and Student roles

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: Supabase PostgreSQL
- **Frontend**: Django Templates + Bootstrap 5
- **Authentication**: Django built-in User model with custom roles

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd hostelocity
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory and add your Supabase credentials:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
SUPABASE_HOST=your_supabase_host_url
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_supabase_password
SUPABASE_PORT=5432
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## User Roles

- **Admin/Warden**: Full access to manage students, rooms, fees, and complaints
- **Student**: Can view room details, complaints, and payment status

## Project Structure

```
hostel_management/
├── manage.py
├── hostel_management/          # Main project settings
├── students/                   # Student management app
├── rooms/                      # Room management app
├── complaints/                 # Complaint system app
├── payments/                   # Fee/Payment management app
├── templates/                  # Global templates
├── static/                     # Static files
└── media/                      # User uploads
```

## Deployment

This project is ready to deploy on Render or any platform that supports Django.

1. Update `ALLOWED_HOSTS` in settings.py
2. Set `DEBUG=False` in production
3. Configure your Supabase database credentials
4. Run `python manage.py collectstatic`
5. Deploy using the provided Procfile

## License

MIT License
