from django.contrib import admin
from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['studentid', 'amount', 'duedate', 'status']
    list_filter = ['status', 'duedate']
    search_fields = ['studentid__name']
    list_editable = ['status']
    date_hierarchy = 'duedate'
