from django.db import models
from students.models import Student


class Fee(models.Model):
    """Fee model - EXACTLY matches Supabase Fee table"""
    
    # Primary Key
    feeid = models.AutoField(primary_key=True, db_column='feeid')
    
    # Foreign Key
    studentid = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees', db_column='studentid')
    
    # Fields
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='amount')
    duedate = models.DateField(blank=True, null=True, db_column='duedate')
    status = models.CharField(max_length=20, blank=True, null=True, db_column='status')
    
    def __str__(self):
        return f"{self.studentid.name if self.studentid else 'N/A'} - ₹{self.amount}"
    
    @property
    def student(self):
        """Alias for studentid for backward compatibility"""
        return self.studentid
    
    @property
    def due_date(self):
        """Alias for duedate for backward compatibility"""
        return self.duedate
    
    class Meta:
        db_table = 'fee'
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'
        ordering = ['-duedate']
        managed = False  # Don't let Django manage this table


class PaymentRecord(models.Model):
    """Payment record model to track payment types and details"""
    
    PAYMENT_TYPE_CHOICES = [
        ('Fees', 'Fees'),
        ('Hostel', 'Hostel'),
        ('Fests', 'Fests'),
        ('Clubs/Chapters', 'Clubs/Chapters'),
    ]
    
    fee = models.OneToOneField(Fee, on_delete=models.CASCADE, related_name='payment_record')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fee.studentid.name if self.fee.studentid else 'N/A'} - {self.payment_type} - ₹{self.fee.amount}"
    
    class Meta:
        verbose_name = 'Payment Record'
        verbose_name_plural = 'Payment Records'


# Keep Payment model for backward compatibility with existing code
class Payment(Fee):
    """Proxy model for Fee to maintain compatibility"""
    class Meta:
        proxy = True
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
