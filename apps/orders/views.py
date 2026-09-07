import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import BookingRequest

@method_decorator(ensure_csrf_cookie, name='dispatch')
class BookingRequestAPIView(View):
    def post(self, request, *args, **kwargs):
        # 1. Parse JSON payload or fallback to standard POST data
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)

        # 2. Extract and sanitize fields
        agent = data.get('agent', 'Headquarters Dispatch').strip()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        product = data.get('product', 'Day Old Chicks').strip()
        quantity = data.get('quantity', '').strip()
        notes = data.get('notes', '').strip()

        # 3. Form Validation
        if not name or not phone:
            return JsonResponse({
                'status': 'error', 
                'message': 'Full Name and Phone Number are required fields.'
            }, status=400)

        # 4. Save to Database
        try:
            booking = BookingRequest.objects.create(
                agent=agent,
                name=name,
                phone=phone,
                product=product,
                quantity=quantity,
                notes=notes
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Booking request created successfully.',
                'booking_id': booking.id
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'An internal error occurred while saving your booking.'
            }, status=500)