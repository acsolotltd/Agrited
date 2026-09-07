import json
from django.http import JsonResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

# If you are passing the CSRF token via headers in JS, keep this. 
# If you want it completely open (not recommended), use @csrf_exempt
@method_decorator(ensure_csrf_cookie, name='dispatch')
class SubscribeNewsletterAPIView(View):
    def post(self, request, *args, **kwargs):
        # 1. Handle both JSON (fetch) and Form-Data (HTMX/Standard form)
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload.'}, status=400)
        else:
            data = request.POST

        # 2. Extract and sanitize fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()

        if not name or not email:
            return JsonResponse({'status': 'error', 'message': 'Both Name and Email are required.'}, status=400)

        # 3. Validate Email format
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'}, status=400)

        # 4. Save to Database using get_or_create to handle duplicates gracefully
        from .models import NewsletterSubscriber # Import here to avoid circular imports if necessary
        
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )

        if not created:
            if not subscriber.is_active:
                # If they previously unsubscribed, reactivate them
                subscriber.is_active = True
                subscriber.name = name # Update name in case it changed
                subscriber.save()
                return JsonResponse({'status': 'success', 'message': 'Welcome back! You have been re-subscribed.'}, status=200)
            
            # If they are already an active subscriber
            return JsonResponse({'status': 'error', 'message': 'This email is already subscribed.'}, status=400)

        # 5. Success Response
        first_name = name.split(' ')[0]
        return JsonResponse({
            'status': 'success',
            'message': f'Thanks for subscribing, {first_name}!',
            'email': email
        }, status=201)