from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import BookingRequest

@csrf_exempt
@require_POST
def submit_booking(request):
    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    service_type = request.POST.get('service_type', 'consultation')
    preferred_date = request.POST.get('preferred_date', '').strip()
    additional_notes = request.POST.get('additional_notes', '').strip()

    # Helper function to generate the Toast HTML
    def render_toast(message, status="error", form_id="booking-form"):
        themes = {
            "error": {
                "border": "border-red-500",
                "icon_bg": "bg-red-100 dark:bg-red-900/30 text-red-500 dark:text-red-400",
                "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />'
            },
            "warning": {
                "border": "border-amber-500",
                "icon_bg": "bg-amber-100 dark:bg-amber-900/30 text-amber-500 dark:text-amber-400",
                "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />'
            },
            "success": {
                "border": "border-emerald-500",
                "icon_bg": "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-500 dark:text-emerald-400",
                "icon": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />'
            }
        }
        
        theme = themes[status]
        clear_script = f"document.getElementById('{form_id}').reset();" if status == "success" else ""

        return f"""
            <div id="toast-booking" class="fixed bottom-6 right-6 z-[100] flex w-full max-w-sm transform items-center gap-3 rounded-xl border-l-4 {theme['border']} bg-white p-4 shadow-2xl transition-all duration-300 dark:bg-slate-900" role="alert">
                <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg {theme['icon_bg']}">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {theme['icon']}
                    </svg>
                </div>
                
                <div class="text-sm font-medium text-slate-800 dark:text-slate-200">
                    {message}
                </div>
                
                <button type="button" class="ml-auto flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white" onclick="this.closest('#toast-booking').remove()" aria-label="Close">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>

                <script>
                    {clear_script}
                    setTimeout(() => {{
                        const toast = document.getElementById('toast-booking');
                        if (toast) {{
                            toast.style.opacity = '0';
                            toast.style.transform = 'translateY(10px)';
                            setTimeout(() => toast.remove(), 300);
                        }}
                    }}, 5000); // 5 seconds for bookings to give them time to read it
                </script>
            </div>
        """

    # 1. Validation check
    if not full_name or not email or not phone or not preferred_date:
        return HttpResponse(render_toast("Please fill in all required fields (Name, Email, Phone, and Date).", "error"))

    # 2. Spam/Duplicate prevention (Optional: check if they already booked this same service on this same date)
    if BookingRequest.objects.filter(email=email, preferred_date=preferred_date, service_type=service_type).exists():
        return HttpResponse(render_toast("You already have a request pending for this service on this date.", "warning"))

    # 3. Save to Database
    try:
        BookingRequest.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            service_type=service_type,
            preferred_date=preferred_date,
            additional_notes=additional_notes
        )
        return HttpResponse(render_toast(f"Success! Your booking for {preferred_date} has been received.", "success"))
    except Exception as e:
        # Catches database errors (like invalid date formats sent from the browser)
        return HttpResponse(render_toast("Something went wrong. Please check your inputs and try again.", "error"))
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


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse

@login_required
def dashboard(request):
    """Renders the main user dashboard."""
    # Fetch user's bookings, ordered by most recent
    bookings = request.user.bookingrequest_set.all().order_by('-created_at')
    
    # Calculate some quick stats
    total_bookings = bookings.count()
    active_bookings = bookings.filter(status__in=['PENDING', 'CONFIRMED']).count()
    
    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
    }
    return render(request, 'dashboard.html', context)

@login_required
@require_POST
def htmx_cancel_booking(request, booking_id):
    """HTMX endpoint to cancel a booking directly from the table."""
    booking = get_object_or_404(BookingRequest, id=booking_id, user=request.user)
    
    if booking.status in ['PENDING', 'CONFIRMED']:
        booking.status = 'CANCELLED'
        booking.save()
        
        # Return the updated status badge as an HTML snippet
        return HttpResponse('''
            <span class="inline-flex items-center rounded-full bg-red-500/10 px-2 py-1 text-xs font-medium text-red-400 ring-1 ring-inset ring-red-500/20">
                Cancelled
            </span>
        ''')
    return HttpResponse(status=400)