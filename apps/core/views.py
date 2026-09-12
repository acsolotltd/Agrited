from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    """Renders the main home page with the contact section."""
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def products(request):
    return render(request, 'products.html')


import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage  # <-- Change this import
from django.conf import settings
from anymail.exceptions import AnymailAPIError 

logger = logging.getLogger(__name__)

def contact_submit(request):
    if request.method == 'POST' and request.headers.get('HX-Request'):
        name = request.POST.get('name', '').strip()
        subject = request.POST.get('subject', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        context = {'name': name, 'subject': subject, 'email': email, 'message': message}

        if not name or not email or not message or not subject:
            response = render(request, 'partials/contact_form.html', context, status=200)
            response['HX-Trigger'] = json.dumps({
                "show-toast": {"message": "Please fill out all required fields.", "type": "error"}
            })
            return response

        try:
            full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            
            # --> Use EmailMessage instead of send_mail <--
            email_msg = EmailMessage(
                subject=f"Website Inquiry: {subject}",
                body=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['ibmxxx@gmail.com'], # Ensure this is your receiving email
                reply_to=[email],        # EmailMessage accepts reply_to perfectly!
            )
            email_msg.send(fail_silently=False)
            
            response = render(request, 'partials/contact-us.html', {}, status=200)
            response['HX-Trigger'] = json.dumps({
                "show-toast": {"message": "Your message was sent successfully!", "type": "success"}
            })
            return response
        except AnymailAPIError as e:
            error_details = e.response.json() if e.response else str(e)
            logger.error(f"Brevo API Error: Status {e.status_code} - Details: {error_details}")
            
            # Return an empty HttpResponse instead of trying to render a missing template
            response = HttpResponse("", status=200) 
            response['HX-Trigger'] = json.dumps({
                "show-toast": {"message": "Email server error. Please try again later.", "type": "error"}
            })
            return response
            
        except Exception as e:
            logger.error(f"General Email Dispatch Failed: {e}")
            response = HttpResponse("", status=200)
            response['HX-Trigger'] = json.dumps({
                "show-toast": {"message": "An unexpected error occurred.", "type": "error"}
            })
            return response

    return HttpResponse("Invalid request method.", status=400)