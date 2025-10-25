# Email Notifications Guide

## Overview
The HostelGrid system now sends automated email notifications to students when they:
1. **Submit a complaint** - Confirmation email with complaint details
2. **Make a payment** - Confirmation email with payment receipt

## Features Implemented

### 📧 Complaint Submission Email
When a student submits a complaint, they receive:
- ✅ **Complaint confirmation** with unique Complaint ID
- ✅ **Full complaint details** (subject, description, status)
- ✅ **Submission timestamp**
- ✅ **Next steps** information
- ✅ **Beautiful HTML formatted email**

### 💳 Payment Confirmation Email
When a student makes a payment, they receive:
- ✅ **Payment receipt** with unique Payment ID
- ✅ **Payment details** (amount, payment type, status)
- ✅ **Payment date**
- ✅ **Proof of payment** for records
- ✅ **Beautiful HTML formatted email** with green theme

## How It Works

### Current Setup (Development Mode)

**Email Backend**: Console  
**Behavior**: Emails are printed to the terminal/console where the server is running

This is perfect for testing because:
- ✅ No email server configuration needed
- ✅ Instant feedback in console
- ✅ Easy to debug
- ✅ Free (no email service costs)

### Example Console Output

When a student submits a complaint, you'll see in your terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Complaint Submitted Successfully - #42
From: noreply@hostelgrid.com
To: student@example.com

HostelGrid - Hostel Management System

Complaint Submitted Successfully ✅

Dear John Doe,

Your complaint has been successfully submitted and received by our team.

[... rest of email content ...]
```

## Production Setup (Real Emails)

### Option 1: Using Gmail

1. **Open `hostel_management/settings.py`**

2. **Comment out the development backend:**
```python
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

3. **Uncomment and configure Gmail settings:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'youremail@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-app-password'  # Gmail App Password (NOT your regular password)
DEFAULT_FROM_EMAIL = 'youremail@gmail.com'
```

4. **Generate Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in to your Google Account
   - Select "Mail" and "Other (Custom name)"
   - Generate password
   - Copy the 16-character password and use it in `EMAIL_HOST_PASSWORD`

### Option 2: Using Other Email Services

**SendGrid:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

**Mailgun:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@yourdomain.com'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## Testing the Email System

### Test 1: Complaint Submission

1. **Login as a student**
2. **Navigate to**: Complaints → Submit New Complaint
3. **Fill in the form:**
   - Subject: "Test Complaint"
   - Description: "Testing email notification"
4. **Submit**
5. **Check your terminal** (dev mode) or **inbox** (production)

**Expected Email:**
- Subject: "Complaint Submitted Successfully - #[ID]"
- Contains: Complaint details, ID, status, timestamp
- Design: Yellow/gold theme with HostelGrid branding

### Test 2: Payment Submission

1. **Login as a student**
2. **Navigate to**: Payments → Make Payment
3. **Fill in the form:**
   - Payment Type: "Hostel Fee"
   - Amount: "5000"
4. **Submit**
5. **Check your terminal** (dev mode) or **inbox** (production)

**Expected Email:**
- Subject: "Payment Confirmation - ₹5000"
- Contains: Payment details, receipt, ID, timestamp
- Design: Green theme with HostelGrid branding

## Email Templates

### Complaint Email Features:
- 📋 **Complaint ID**: Unique identifier for tracking
- 📝 **Full Details**: Subject, description, status
- ⏰ **Timestamp**: When the complaint was submitted
- 📱 **Responsive**: Works on all devices
- 🎨 **Branded**: HostelGrid logo and colors

### Payment Email Features:
- 💰 **Amount Display**: Large, prominent amount
- 🆔 **Payment ID**: Unique receipt number
- ✅ **Status Badge**: Visual payment confirmation
- 📅 **Date**: When payment was recorded
- 💚 **Success Theme**: Green colors for positive action

## File Structure

```
Hostelocity/
├── hostel_management/
│   ├── email_utils.py          # Email sending functions ⭐ NEW
│   └── settings.py              # Email configuration
├── complaints/
│   └── views.py                 # Updated with email sending
└── payments/
    └── views.py                 # Updated with email sending
```

## Code Overview

### Email Utility Functions

**Location**: `hostel_management/email_utils.py`

**Functions:**
1. `send_complaint_confirmation_email(complaint, student_email)`
2. `send_payment_confirmation_email(fee, payment_type, student_email, student_name)`

Both functions:
- ✅ Send HTML formatted emails
- ✅ Include plain text fallback
- ✅ Handle errors gracefully (won't crash if email fails)
- ✅ Print errors to console for debugging

### Integration Points

**Complaints View** (`complaints/views.py` line 72-79):
```python
# Send email confirmation to student
try:
    from hostel_management.email_utils import send_complaint_confirmation_email
    if request.user.email:
        send_complaint_confirmation_email(complaint, request.user.email)
except Exception as e:
    print(f"Email sending failed: {str(e)}")
```

**Payments View** (`payments/views.py` line 235-242):
```python
# Send email confirmation to student
try:
    from hostel_management.email_utils import send_payment_confirmation_email
    if request.user.email:
        send_payment_confirmation_email(fee, payment_type, request.user.email, student.name)
except Exception as e:
    print(f"Email sending failed: {str(e)}")
```

## Important Notes

### Email Requirements
- ✅ Students must have email addresses in their User accounts
- ✅ Emails are sent to `request.user.email`
- ✅ If user has no email, notification is skipped (no error)

### Error Handling
- ✅ Email failures don't break the complaint/payment submission
- ✅ Errors are logged to console
- ✅ User still sees success message even if email fails
- ✅ Graceful degradation ensures system stability

### Security
- ✅ Never store email passwords in code (use environment variables in production)
- ✅ Use App Passwords for Gmail (not regular passwords)
- ✅ Emails are sent asynchronously (don't block user actions)

## Environment Variables (Production Best Practice)

Instead of hardcoding email credentials, use environment variables:

1. **Create `.env` file** (already exists):
```bash
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

2. **Update settings.py**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

## Troubleshooting

### Issue: Emails not appearing in console
**Solution**: Make sure EMAIL_BACKEND is set to console mode in settings.py

### Issue: Gmail authentication fails
**Solution**: 
- Enable 2-factor authentication on your Google account
- Generate an App Password (don't use your regular password)
- Use the 16-character app password in settings

### Issue: Emails go to spam
**Solution**: 
- Use a proper FROM email address
- Consider using a transactional email service (SendGrid, Mailgun)
- Set up SPF, DKIM records for your domain

### Issue: Student doesn't receive email
**Check:**
- Does the user have an email address in their account?
- Check console for error messages
- Verify email settings are correct
- Check spam folder

## Future Enhancements

Potential additions:
- 📧 Email when complaint status changes
- 📧 Email reminders for pending payments
- 📧 Weekly summary emails
- 📧 Email when admin responds to complaint
- 📧 Payment due date reminders
- 📧 Welcome email on registration

## Support

For issues or questions:
1. Check console for error messages
2. Verify email configuration in settings.py
3. Test with development mode first
4. Check user has email address registered

---

**Status**: ✅ Fully Implemented  
**Mode**: Development (Console)  
**Ready for Production**: Yes (configure Gmail or SMTP)  
**Testing**: Required before production deployment

