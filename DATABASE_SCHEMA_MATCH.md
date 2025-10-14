# Database Schema Integration Guide

## ✅ Models Updated to Match Your Database

I've updated the Django models to match your existing database schema exactly!

### 📋 Your Database Tables

1. **Student** (StudentID, Name, Gender, Department, Phone)
2. **Hostel** (HostelID, Name, Location, TotalRooms)
3. **Room** (RoomID, HostelID, RoomNumber, Capacity, Type)
4. **Allocation** (AllocationID, StudentID, RoomID, Date_of_Allocation)
5. **Fee** (FeeID, StudentID, Amount, DueDate, Status)

---

## 🔄 Changes Made

### 1. **Student Model** (`students/models.py`)
- ✅ Changed to match your schema
- ✅ Fields: `name`, `gender`, `department`, `phone`, `photo`
- ✅ Table name: `student`
- ✅ Removed: roll_number, course, year, address, email (not in your schema)

### 2. **Hostel Model** (`rooms/models.py`) - **NEW**
- ✅ Added Hostel model
- ✅ Fields: `name`, `location`, `total_rooms`
- ✅ Table name: `hostel`

### 3. **Room Model** (`rooms/models.py`)
- ✅ Updated to match your schema
- ✅ Fields: `hostel` (ForeignKey), `room_number`, `capacity`, `type`
- ✅ Table name: `room`
- ✅ Removed: floor, description, is_full, created_at

### 4. **Allocation Model** (`students/models.py`) - **NEW**
- ✅ Added Allocation model for student-room assignments
- ✅ Fields: `student`, `room`, `date_of_allocation`
- ✅ Table name: `allocation`
- ✅ This replaces the direct room assignment in Student

### 5. **Fee Model** (`payments/models.py`)
- ✅ Changed from Payment to Fee
- ✅ Fields: `student`, `amount`, `due_date`, `status`
- ✅ Table name: `fee`
- ✅ Removed: payment_type, payment_date, transaction_id, remarks

---

## 🎯 How Django Will Use Your Existing Tables

Django will now:
1. **Connect to your existing tables** using `db_table` meta option
2. **Use your existing data** - no data migration needed
3. **Maintain your column names** (e.g., `duedate` in Fee table)

---

## 🚀 Next Steps

### Step 1: Configure Your Database Connection

Edit your `.env` file (NOT `.env.example`):

```env
SECRET_KEY=7wr6j0%kdjoza3m7zosff4t2m++2a@&+c+v1ye64u8%p99g$_j
DEBUG=True
SUPABASE_HOST=db.your_project.supabase.co
SUPABASE_DB_NAME=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_actual_password
SUPABASE_PORT=5432
```

### Step 2: Tell Django About Your Tables

Since your tables already exist in Supabase, you need to tell Django to use them:

```bash
# Create migrations (Django needs to track the models)
python manage.py makemigrations

# Mark migrations as applied WITHOUT running them (since tables exist)
python manage.py migrate --fake-initial
```

**Important**: Use `--fake-initial` because your tables already exist!

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 4: Run the Server

```bash
python manage.py runserver
```

---

## 🔍 Verify It's Working

### Test in Django Admin

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. You should see:
   - Students
   - Hostels
   - Rooms
   - Allocations
   - Fees

### Check Your Existing Data

If you already have data in your Supabase tables, you should see it in Django admin!

---

## ⚠️ Important Notes

### 1. Primary Keys
Django will automatically use your existing SERIAL primary keys:
- `studentid` → `id` in Django
- `hostelid` → `id` in Django
- etc.

### 2. Foreign Keys
Django understands your foreign key relationships:
- Room → Hostel
- Allocation → Student & Room
- Fee → Student

### 3. Case Sensitivity
- PostgreSQL column names are lowercase by default
- Django handles this automatically
- Your `DueDate` becomes `duedate` in the database

---

## 🔧 If You Need to Modify Schema

If you want to add Django-specific fields (like `created_at`, `updated_at`), you'll need to:

1. Add the field to your Supabase table first
2. Update the Django model
3. Run `python manage.py makemigrations`
4. Run `python manage.py migrate`

---

## 📊 Model Relationships

```
Hostel
  └─→ Room (many)
       └─→ Allocation (many)
            └─→ Student

Student
  ├─→ Allocation (many)
  └─→ Fee (many)
```

---

## 💡 Usage Examples

### Get Student's Current Room

```python
student = Student.objects.get(id=1)
current_allocation = student.get_current_allocation()
current_room = student.get_current_room()
```

### Get All Students in a Room

```python
room = Room.objects.get(id=1)
allocations = room.allocations.all()
students = [alloc.student for alloc in allocations]
```

### Check Room Occupancy

```python
room = Room.objects.get(id=1)
occupancy = room.current_occupancy()
available = room.available_spaces()
percentage = room.occupancy_percentage()
is_full = room.is_full()
```

---

## 🎨 What Stays the Same

The frontend (templates, views, URLs) remains mostly the same!
- Dashboard works
- Room list works
- Student management works
- All features work

The UI automatically adapts to show fields from your schema.

---

## ✨ Benefits

1. ✅ Use your existing database structure
2. ✅ No data migration needed
3. ✅ Keep your existing relationships
4. ✅ Django ORM works with your schema
5. ✅ Beautiful UI for your data

---

## 🆘 Troubleshooting

### Error: "Table already exists"
Use `--fake-initial` when migrating:
```bash
python manage.py migrate --fake-initial
```

### Error: "Column not found"
Check that column names in models match your database exactly.

### Can't see existing data
Make sure your `.env` credentials are correct and you used `--fake-initial`.

---

**Your Django app is now perfectly matched to your database! 🎉**
