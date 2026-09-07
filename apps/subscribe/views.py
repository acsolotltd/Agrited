import json
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.html import format_html


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SubscribeNewsletterAPIView(View):
    def post(self, request, *args, **kwargs):
        is_htmx = request.headers.get('HX-Request') == 'true'

        # 1. Handle both JSON (fetch) and Form-Data (HTMX/Standard form)
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                msg = 'Invalid JSON payload.'
                if is_htmx:
                    return self._render_error(msg)
                return JsonResponse({'status': 'error', 'message': msg}, status=400)
        else:
            data = request.POST

        # 2. Extract and sanitize fields
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()

        if not name or not email:
            msg = 'Both Name and Email are required.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=400)

        # 3. Validate Email format
        try:
            validate_email(email)
        except ValidationError:
            msg = 'Please provide a valid email address.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=400)

        # 4. Save to Database using get_or_create
        from .models import NewsletterSubscriber

        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )

        if not created:
            if not subscriber.is_active:
                # If previously unsubscribed, reactivate them
                subscriber.is_active = True
                subscriber.name = name  # Update name in case it changed
                subscriber.save()
                
                msg = 'Welcome back! You have been re-subscribed.'
                if is_htmx:
                    return self._render_success('Welcome Back!', msg)
                return JsonResponse({'status': 'success', 'message': msg}, status=200)

            # Already an active subscriber
            msg = 'This email address is already subscribed.'
            if is_htmx:
                return self._render_error(msg)
            return JsonResponse({'status': 'error', 'message': msg}, status=400)

        # 5. New Subscription Success
        first_name = name.split(' ')[0]
        msg = f'Thanks for subscribing, {first_name}!'
        
        if is_htmx:
            return self._render_success(
                title=f'Welcome aboard, {first_name}!',
                message="We've sent a confirmation link to your inbox."
            )

        return JsonResponse({
            'status': 'success',
            'message': msg,
            'email': email
        }, status=201)

    def _render_success(self, title, message):
        """Returns HTML component styled for the glassmorphism newsletter section."""
        html = format_html(
            '''
            <div class="flex items-start gap-3 rounded-xl border border-emerald-300/30 bg-emerald-500/20 p-3.5 text-xs text-emerald-100 sm:text-sm">
                <svg class="h-5 w-5 flex-shrink-0 text-emerald-300 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                    <p class="font-bold text-white">{}</p>
                    <p class="mt-0.5 text-emerald-100/90">{}</p>
                </div>
            </div>
            ''',
            title,
            message
        )
        # Returns HTTP 200 so HTMX updates the target DOM container
        response = HttpResponse(html, status=200)
        # Optional: Triggers form reset in frontend if configured
        response['HX-Trigger'] = 'newsletterSubscribed' 
        return response

    def _render_error(self, message):
        """Returns error HTML component matching the section theme."""
        html = format_html(
            '''
            <div class="flex items-start gap-3 rounded-xl border border-red-400/30 bg-red-500/20 p-3.5 text-xs text-red-100 sm:text-sm">
                <svg class="h-5 w-5 flex-shrink-0 text-red-300 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                    <p class="font-bold text-white">Subscription Error</p>
                    <p class="mt-0.5 text-red-100/90">{}</p>
                </div>
            </div>
            ''',
            message
        )
        return HttpResponse(html, status=200)