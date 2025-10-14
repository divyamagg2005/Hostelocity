from django.contrib import admin
from .models import Student, UserProfile, Allocation


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'gender', 'department', 'phone']
    list_filter = ['gender', 'department']
    search_fields = ['name', 'phone']


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'date_of_allocation']
    list_filter = ['date_of_allocation', 'room__hostelid']
    search_fields = ['student__name', 'room__roomnumber']
    date_hierarchy = 'date_of_allocation'
