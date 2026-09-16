from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

def send_account_approved_email(user, request=None):
    """
    Sends an account approval notification using send_mail.
    `user` can be a Django User model instance or custom user object.
    """
    subject = "Account Approved - Welcome to Agrited"
    
    login_url = "https://localhost:8000/auth/?login"  
    
    context = {
        'name': user.full_name or user.username,
        'email': user.email,
        'login_url': login_url,
    }

    # 1. Plain-text fallback for email clients that disable HTML
    text_message = (
        f"Hello {context['name']},\n\n"
        f"Great news! Your Agrited account has been approved. "
        f"You can now log in at:\n{login_url}\n\n"
        f"Best regards,\nThe Agrited Team"
    )

    html_message = render_to_string('emails/account_approved.html', context)
    send_mail(
        subject=subject,
        message=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )