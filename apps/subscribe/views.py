

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber

@csrf_exempt
@require_POST
def subscribe_newsletter(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()

    # Helper function to generate the Toast HTML
    def render_toast(message, status="error"):
        # Tailwind configurations based on status
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
        
        # Only clear the form if the subscription was successful
        clear_script = "document.getElementById('newsletter-form').reset();" if status == "success" else ""

        return f"""
            <div id="toast-notification" class="fixed bottom-6 right-6 z-[100] flex w-full max-w-sm transform items-center gap-3 rounded-xl border-l-4 {theme['border']} bg-white p-4 shadow-2xl transition-all duration-300 dark:bg-slate-900" role="alert">
                <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg {theme['icon_bg']}">
                    <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        {theme['icon']}
                    </svg>
                </div>
                
                <div class="text-sm font-medium text-slate-800 dark:text-slate-200">
                    {message}
                </div>
                
                <button type="button" class="ml-auto flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition-colors hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-slate-800 dark:hover:text-white" onclick="this.closest('#toast-notification').remove()" aria-label="Close">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>

                <!-- HTMX executes this script automatically upon swapping -->
                <script>
                    {clear_script}
                    setTimeout(() => {{
                        const toast = document.getElementById('toast-notification');
                        if (toast) {{
                            toast.style.opacity = '0';
                            toast.style.transform = 'translateY(10px)';
                            setTimeout(() => toast.remove(), 300); // Wait for transition to finish
                        }}
                    }}, 4000);
                </script>
            </div>
        """

    # 1. Validation check
    if not name or not email:
        return HttpResponse(render_toast("Please provide both your name and email address.", "error"))

    # 2. Existing user check
    if NewsletterSubscriber.objects.filter(email=email).exists():
        return HttpResponse(render_toast("This email is already on our subscriber list!", "warning"))

    # 3. Save to Database
    NewsletterSubscriber.objects.create(name=name, email=email)

    # 4. Success Response
    return HttpResponse(render_toast("Success! You've been added to our newsletter.", "success"))


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