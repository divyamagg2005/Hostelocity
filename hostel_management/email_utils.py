"""
Email utility functions for sending notifications
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_complaint_confirmation_email(complaint, student_email):
    """
    Send email confirmation when a complaint is submitted
    """
    subject = f'Complaint Submitted Successfully - #{complaint.id}'
    
    # Create HTML email message
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: #fff; margin: 0;">HostelGrid</h1>
                <p style="color: #fff; margin: 10px 0 0 0;">Hostel Management System</p>
            </div>
            
            <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Complaint Submitted Successfully ✅</h2>
                
                <p>Dear <strong>{complaint.student.name}</strong>,</p>
                
                <p>Your complaint has been successfully submitted and received by our team. We will review it and take appropriate action as soon as possible.</p>
                
                <div style="background: #fff; padding: 20px; border-left: 4px solid #FFD700; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #FFD700;">Complaint Details:</h3>
                    <p><strong>Complaint ID:</strong> #{complaint.id}</p>
                    <p><strong>Subject:</strong> {complaint.subject}</p>
                    <p><strong>Description:</strong> {complaint.description}</p>
                    <p><strong>Status:</strong> <span style="background: #FFA500; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;">{complaint.status}</span></p>
                    <p><strong>Submitted:</strong> {complaint.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <p><strong>What happens next?</strong></p>
                <ul>
                    <li>Our admin team will review your complaint</li>
                    <li>You'll receive updates on the status</li>
                    <li>You can track your complaint status on your dashboard</li>
                </ul>
                
                <p>If you have any urgent concerns, please contact the hostel office directly.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #666;">
                    <p style="margin: 5px 0;">Thank you for using HostelGrid!</p>
                    <p style="margin: 5px 0; font-size: 12px;">This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
HostelGrid - Hostel Management System

Complaint Submitted Successfully ✅

Dear {complaint.student.name},

Your complaint has been successfully submitted and received by our team.

Complaint Details:
- Complaint ID: #{complaint.id}
- Subject: {complaint.subject}
- Description: {complaint.description}
- Status: {complaint.status}
- Submitted: {complaint.created_at.strftime('%B %d, %Y at %I:%M %p')}

What happens next?
• Our admin team will review your complaint
• You'll receive updates on the status
• You can track your complaint status on your dashboard

If you have any urgent concerns, please contact the hostel office directly.

Thank you for using HostelGrid!
This is an automated email. Please do not reply to this message.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending complaint email: {str(e)}")
        return False


def send_payment_confirmation_email(fee, payment_type, student_email, student_name):
    """
    Send email confirmation when a payment is made
    """
    subject = f'Payment Confirmation - ₹{fee.amount}'
    
    # Create HTML email message
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: #fff; margin: 0;">HostelGrid</h1>
                <p style="color: #fff; margin: 10px 0 0 0;">Payment Confirmation</p>
            </div>
            
            <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Payment Received Successfully ✅</h2>
                
                <p>Dear <strong>{student_name}</strong>,</p>
                
                <p>Thank you for your payment! We have successfully received your payment and it has been recorded in your account.</p>
                
                <div style="background: #fff; padding: 20px; border-left: 4px solid #4CAF50; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #4CAF50;">Payment Details:</h3>
                    <p><strong>Payment ID:</strong> #{fee.feeid}</p>
                    <p><strong>Payment Type:</strong> {payment_type}</p>
                    <p><strong>Amount Paid:</strong> <span style="font-size: 24px; color: #4CAF50; font-weight: bold;">₹{fee.amount}</span></p>
                    <p><strong>Status:</strong> <span style="background: #4CAF50; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;">PAID</span></p>
                    <p><strong>Date:</strong> {fee.duedate.strftime('%B %d, %Y')}</p>
                </div>
                
                <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #2e7d32;"><strong>📝 Note:</strong> Please keep this email as proof of payment. You can also view your payment history on your dashboard.</p>
                </div>
                
                <p><strong>What's next?</strong></p>
                <ul>
                    <li>Your payment has been recorded in the system</li>
                    <li>You can view your payment history anytime</li>
                    <li>A receipt is available on your dashboard</li>
                </ul>
                
                <p>If you have any questions about this payment, please contact the accounts office.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #666;">
                    <p style="margin: 5px 0;">Thank you for your payment!</p>
                    <p style="margin: 5px 0; font-size: 12px;">This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
HostelGrid - Payment Confirmation

Payment Received Successfully ✅

Dear {student_name},

Thank you for your payment! We have successfully received your payment.

Payment Details:
- Payment ID: #{fee.feeid}
- Payment Type: {payment_type}
- Amount Paid: ₹{fee.amount}
- Status: PAID
- Date: {fee.duedate.strftime('%B %d, %Y')}

📝 Note: Please keep this email as proof of payment. You can also view your payment history on your dashboard.

What's next?
• Your payment has been recorded in the system
• You can view your payment history anytime
• A receipt is available on your dashboard

If you have any questions about this payment, please contact the accounts office.

Thank you for your payment!
This is an automated email. Please do not reply to this message.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending payment email: {str(e)}")
        return False


def send_complaint_resolution_email(complaint, student_email):
    """
    Send email notification when a complaint is resolved
    """
    subject = f'Complaint Resolved - #{complaint.id}'
    
    # Create HTML email message
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: #fff; margin: 0;">HostelGrid</h1>
                <p style="color: #fff; margin: 10px 0 0 0;">Complaint Resolved</p>
            </div>
            
            <div style="background: #f9f9f9; padding: 30px; border: 1px solid #ddd; border-top: none; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-top: 0;">Your Complaint Has Been Resolved ✅</h2>
                
                <p>Dear <strong>{complaint.student.name}</strong>,</p>
                
                <p>We're pleased to inform you that your complaint has been reviewed and resolved by our admin team.</p>
                
                <div style="background: #fff; padding: 20px; border-left: 4px solid #28a745; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #28a745;">Complaint Details:</h3>
                    <p><strong>Complaint ID:</strong> #{complaint.id}</p>
                    <p><strong>Category:</strong> {complaint.get_category_display()}</p>
                    <p><strong>Subject:</strong> {complaint.subject}</p>
                    <p><strong>Description:</strong> {complaint.description}</p>
                    <p><strong>Status:</strong> <span style="background: #28a745; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px;">RESOLVED</span></p>
                    <p><strong>Submitted:</strong> {complaint.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p><strong>Resolved:</strong> {complaint.resolved_at.strftime('%B %d, %Y at %I:%M %p') if complaint.resolved_at else 'Just now'}</p>
                </div>
                
                {f'''<div style="background: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #c3e6cb;">
                    <p style="margin: 0 0 5px 0; color: #155724;"><strong>📝 Admin Remarks:</strong></p>
                    <p style="margin: 0; color: #155724;">{complaint.admin_remarks}</p>
                </div>''' if complaint.admin_remarks else ''}
                
                <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #2e7d32;"><strong>✨ Thank you for bringing this to our attention!</strong> We appreciate your patience and feedback.</p>
                </div>
                
                <p><strong>What's next?</strong></p>
                <ul>
                    <li>Your complaint has been marked as resolved</li>
                    <li>You can view the resolution details on your dashboard</li>
                    <li>If you have any follow-up concerns, feel free to submit a new complaint</li>
                </ul>
                
                <p>If you're not satisfied with the resolution or have additional concerns, please don't hesitate to contact the hostel office or submit a new complaint.</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; text-align: center; color: #666;">
                    <p style="margin: 5px 0;">Thank you for using HostelGrid!</p>
                    <p style="margin: 5px 0; font-size: 12px;">This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
HostelGrid - Complaint Resolved

Your Complaint Has Been Resolved ✅

Dear {complaint.student.name},

We're pleased to inform you that your complaint has been reviewed and resolved by our admin team.

Complaint Details:
- Complaint ID: #{complaint.id}
- Category: {complaint.get_category_display()}
- Subject: {complaint.subject}
- Description: {complaint.description}
- Status: RESOLVED
- Submitted: {complaint.created_at.strftime('%B %d, %Y at %I:%M %p')}
- Resolved: {complaint.resolved_at.strftime('%B %d, %Y at %I:%M %p') if complaint.resolved_at else 'Just now'}

{f"Admin Remarks: {complaint.admin_remarks}" if complaint.admin_remarks else ""}

✨ Thank you for bringing this to our attention! We appreciate your patience and feedback.

What's next?
• Your complaint has been marked as resolved
• You can view the resolution details on your dashboard
• If you have any follow-up concerns, feel free to submit a new complaint

If you're not satisfied with the resolution or have additional concerns, please don't hesitate to contact the hostel office or submit a new complaint.

Thank you for using HostelGrid!
This is an automated email. Please do not reply to this message.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending complaint resolution email: {str(e)}")
        return False

