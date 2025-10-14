from django.contrib import admin
from .models import Room, Hostel


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'totalrooms']
    search_fields = ['name', 'location']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomnumber', 'hostelid', 'type', 'capacity', 'current_occupancy_display']
    list_filter = ['hostelid', 'type']
    search_fields = ['roomnumber', 'hostelid__name']
    
    def current_occupancy_display(self, obj):
        return f"{obj.current_occupancy()}/{obj.capacity}"
    current_occupancy_display.short_description = 'Occupancy'
