from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user model for role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin/Warden'),
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        db_table = 'user_profile'


class Student(models.Model):
    """Student model - EXACTLY matches Supabase Student table"""
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('CHE', 'Chemical Engineering'),
        ('BT', 'Biotechnology'),
    ]
    
    # Primary Key
    studentid = models.AutoField(primary_key=True, db_column='studentid')
    
    # Required field
    name = models.CharField(max_length=100, db_column='name')
    
    # Optional fields
    gender = models.CharField(max_length=10, blank=True, null=True, db_column='gender', choices=GENDER_CHOICES)
    department = models.CharField(max_length=50, blank=True, null=True, db_column='department', choices=DEPARTMENT_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True, db_column='phone')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        managed = False  # Don't let Django manage this table
    
    def get_current_allocation(self):
        """Get student's current room allocation"""
        try:
            return self.allocations.latest('date_of_allocation')
        except:
            return None
    
    def get_current_room(self):
        """Get student's current room"""
        allocation = self.get_current_allocation()
        return allocation.room if allocation else None


class Allocation(models.Model):
    """Allocation model - EXACTLY matches Supabase Allocation table"""
    
    # Primary Key
    allocationid = models.AutoField(primary_key=True, db_column='allocationid')
    
    # Foreign Keys
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='allocations', db_column='studentid')
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, related_name='allocations', db_column='roomid')
    
    # Date field
    date_of_allocation = models.DateField(db_column='date_of_allocation', blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.room.room_number}"
    
    class Meta:
        db_table = 'allocation'
        verbose_name = 'Room Allocation'
        verbose_name_plural = 'Room Allocations'
        ordering = ['-date_of_allocation']
        managed = False  # Don't let Django manage this table
