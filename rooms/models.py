from django.db import models


class Hostel(models.Model):
    """Hostel model - EXACTLY matches Supabase Hostel table"""
    
    # Primary Key
    hostelid = models.AutoField(primary_key=True, db_column='hostelid')
    
    # Fields
    name = models.CharField(max_length=100, blank=True, null=True, db_column='name')
    location = models.CharField(max_length=100, blank=True, null=True, db_column='location')
    totalrooms = models.IntegerField(blank=True, null=True, db_column='totalrooms')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'hostel'
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        managed = False  # Don't let Django manage this table


class Room(models.Model):
    """Room model - EXACTLY matches Supabase Room table"""
    
    # Primary Key
    roomid = models.AutoField(primary_key=True, db_column='roomid')
    
    # Foreign Key
    hostelid = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms', db_column='hostelid')
    
    # Fields
    roomnumber = models.CharField(max_length=10, blank=True, null=True, db_column='roomnumber')
    capacity = models.IntegerField(blank=True, null=True, db_column='capacity')
    type = models.CharField(max_length=20, blank=True, null=True, db_column='type')
    
    def __str__(self):
        return f"{self.hostelid.name if self.hostelid else 'N/A'} - Room {self.roomnumber}"
    
    @property
    def hostel(self):
        """Alias for hostelid for backward compatibility"""
        return self.hostelid
    
    @property
    def room_number(self):
        """Alias for roomnumber for backward compatibility"""
        return self.roomnumber
    
    class Meta:
        db_table = 'room'
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['hostelid', 'roomnumber']
        managed = False  # Don't let Django manage this table
    
    def current_occupancy(self):
        """Get current number of students allocated to this room"""
        from students.models import Allocation
        return Allocation.objects.filter(room=self).count()
    
    def available_spaces(self):
        """Get number of available spaces"""
        return self.capacity - self.current_occupancy()
    
    def is_full(self):
        """Check if room is full"""
        return self.current_occupancy() >= self.capacity
    
    def occupancy_percentage(self):
        """Get occupancy percentage"""
        if self.capacity == 0:
            return 0
        return (self.current_occupancy() / self.capacity) * 100
    
    def get_room_type_display(self):
        """Get display value for room type"""
        return self.type if self.type else 'N/A'
