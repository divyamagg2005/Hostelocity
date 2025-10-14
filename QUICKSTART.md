# 🏢 Hostel Management System - Quick Start Guide

## 🚀 Get Started in 5 Minutes!

### Step 1: Install Dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Setup Supabase Database
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get database credentials from Settings → Database

### Step 3: Configure Environment
Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
SUPABASE_HOST=db.xxxxxxxxx.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-password
SUPABASE_PORT=5432
```

### Step 4: Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Step 5: Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 📋 Features

✅ **Student Management** - Add, edit, delete students with photos  
✅ **Room Management** - Track room occupancy automatically  
✅ **Fee Management** - Manage hostel fees and payments  
✅ **Complaint System** - Students submit, admins resolve  
✅ **Role-Based Dashboards** - Separate views for Admin & Students  
✅ **Modern UI** - Bootstrap 5 with responsive design  
✅ **Supabase PostgreSQL** - Cloud database integration  
✅ **Ready to Deploy** - Configured for Render hosting  

---

## 👥 User Roles

### Admin/Warden
- Manage all students, rooms, fees
- View/resolve complaints
- Access complete dashboard with statistics

### Student
- View room details
- Submit complaints
- Check payment status
- Personal dashboard

---

## 📁 Project Structure

```
hostelocity/
├── hostel_management/    # Main project
├── students/             # Student management
├── rooms/                # Room management
├── complaints/           # Complaint system
├── payments/             # Fee management
├── templates/            # HTML templates
└── static/               # CSS/JS files
```

---

## 🔑 Default Login (After Setup)

**Admin:**
- URL: http://127.0.0.1:8000/admin/
- Username: (your superuser)
- Password: (your password)

**Main App:**
- URL: http://127.0.0.1:8000/
- Login with created credentials

---

## 📚 Documentation

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Detailed setup instructions
- **PROJECT_STRUCTURE.md** - Complete folder structure
- **TESTING_GUIDE.md** - Testing checklist
- **BUILD_INSTRUCTIONS.txt** - Quick reference

---

## 🛠️ Tech Stack

- **Backend:** Django 4.2+
- **Database:** PostgreSQL (Supabase)
- **Frontend:** Bootstrap 5
- **Deployment:** Gunicorn + Render

---

## 🐛 Troubleshooting

**Database connection error?**
- Check .env credentials
- Verify Supabase project is active
- Whitelist your IP in Supabase settings

**Static files not loading?**
```bash
python manage.py collectstatic
```

**Import errors?**
```bash
pip install -r requirements.txt
```

---

## 🌐 Deploy to Production

### Quick Deploy to Render:

1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. Create Web Service on Render
3. Set environment variables
4. Deploy!

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn hostel_management.wsgi
```

---

## 📞 Need Help?

1. Check **SETUP_GUIDE.md** for detailed instructions
2. Review **TESTING_GUIDE.md** for common issues
3. See **PROJECT_STRUCTURE.md** for architecture details

---

## ✨ Key Highlights

- **Complete CRUD** operations for all modules
- **Automatic room occupancy** tracking
- **Role-based access** control
- **Beautiful responsive** UI
- **Production-ready** configuration
- **Comprehensive documentation**

---

**Built with ❤️ using Django + Supabase**

Start building your hostel management solution today! 🎉
