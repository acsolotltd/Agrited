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

def contact_submit(request):
    """Handles the HTMX POST request for the contact form."""
    if request.method == 'POST' and request.headers.get('HX-Request'):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic manual validation
        if not name or not email or not message:
            return render(request, 'partials/contact.html', {
                'error': 'All fields are required.',
                'name': name,
                'email': email,
                'message': message
            })

        try:
            # Send the email
            send_mail(
                subject=f"New Contact Inquiry from {name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['support@yourdomain.com'], # Update with your destination email
                fail_silently=False,
            )
            # Return a success fragment
            return render(request, 'partials/contact_success.html')
            
        except Exception as e:
            # Handle email server errors
            return render(request, 'partials/contact_form.html', {
                'error': 'An error occurred while sending the email. Please try again.',
                'name': name,
                'email': email,
                'message': message
            })

    return HttpResponse("Invalid request method.", status=400)