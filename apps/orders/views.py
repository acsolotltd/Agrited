import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import BookingRequest

@method_decorator(ensure_csrf_cookie, name='dispatch')
class BookingRequestAPIView(View):
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
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



import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.html import format_html
from .models import BookingRequest

@method_decorator(ensure_csrf_cookie, name='dispatch')
class BookingRequestAPIView(View):
    def post(self, request, *args, **kwargs):
        is_htmx = request.headers.get('HX-Request') == 'true'

        # 1. Parse JSON payload or fallback to standard POST data
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
        except json.JSONDecodeError:
            msg = 'Invalid JSON format.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=400)

        # 2. Extract and sanitize fields
        agent = data.get('agent', 'Headquarters Dispatch').strip()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        product = data.get('product', 'Day Old Chicks').strip()
        quantity = data.get('quantity', '').strip()
        notes = data.get('notes', '').strip()

        # 3. Form Validation
        if not name or not phone:
            msg = 'Full Name and Phone Number are required fields.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=400)

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
            
            if is_htmx:
                return self._render_success(f'Booking request #{booking.id} created successfully.')

            return JsonResponse({
                'status': 'success',
                'message': 'Booking request created successfully.',
                'booking_id': booking.id
            }, status=201)

        except Exception as e:
            msg = 'An internal error occurred while saving your booking.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=500)

    def _render_success(self, message):
        html = format_html(
            '''
            <div class="flex items-start gap-3 rounded-xl border border-emerald-300/30 bg-emerald-500/20 p-3.5 text-xs text-emerald-100 sm:text-sm">
                <svg class="h-5 w-5 flex-shrink-0 text-emerald-300 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                    <p class="font-bold text-white">Success!</p>
                    <p class="mt-0.5 text-emerald-100/90">{}</p>
                </div>
            </div>
            ''',
            message
        )
        return HttpResponse(html, status=200)

    def _render_error(self, message):
        html = format_html(
            '''
            <div class="flex items-start gap-3 rounded-xl border border-red-400/30 bg-red-500/20 p-3.5 text-xs text-red-100 sm:text-sm">
                <svg class="h-5 w-5 flex-shrink-0 text-red-300 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                    <p class="font-bold text-white">Error</p>
                    <p class="mt-0.5 text-red-100/90">{}</p>
                </div>
            </div>
            ''',
            message
        )
        # Status 200 ensures HTMX swaps the error fragment into the DOM target
        return HttpResponse(html, status=200)