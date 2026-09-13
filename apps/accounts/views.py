from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()
def send_pending_approval_email(user_name, user_email):
    subject = "Account Pending Approval - Agrited"
    context = {'name': user_name, 'email': user_email}
    
    # Fallback plain text
    text_content = f"Hello {user_name},\n\nThank you for registering. Your account requires administrative approval before activation. We will notify you once you are approved."
    
    # Render the rich HTML
    html_content = render_to_string('emails/signup_pending.html', context)
    
    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email], 
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send(fail_silently=False)



def _render_toast(request, message, level="error", form_id=""):
    """Helper to render the toast notification partial."""
    return render(request, "partials/toast.html", {
        "message": message,
        "level": level,
        "form_id": form_id,
    })


@require_GET
def auth_page(request):
    """Renders the primary auth page."""
    return render(request, "auth.html")


@require_POST
def htmx_signup(request):
    """Processes user registration."""
    email = request.POST.get("email", "").strip().lower()
    full_name = request.POST.get("full_name", "").strip()
    phone_number = request.POST.get("phone_number", "").strip()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    # Validations
    if not all([email, full_name, password, confirm_password]):
        return _render_toast(request, "Please fill in all required fields.", "error")

    if password != confirm_password:
        return _render_toast(request, "Passwords do not match.", "error")

    if len(password) < 8:
        return _render_toast(request, "Password must be at least 8 characters long.", "error")

    if User.objects.filter(email=email).exists():
        return _render_toast(request, "An account with this email already exists.", "warning")

    # Save user with pending status
    User.objects.create_user(
        email=email,
        password=password,
        full_name=full_name,
        phone_number=phone_number,
        is_active=False
    )
    send_pending_approval_email(full_name, email)
    return _render_toast(
        request,
        "Account created! Registration is pending administrator approval.",
        level="success",
        form_id="signup-form"
    )


@require_POST
def htmx_login(request):
    """Processes login authentication."""
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")

    if not email or not password:
        return _render_toast(request, "Please enter both email and password.", "error")

    try:
        user_obj = User.objects.get(email=email)
        if not user_obj.is_active:
            return _render_toast(
                request, 
                "Account pending approval. You will receive access once approved.", 
                "warning"
            )
    except User.DoesNotExist:
        return _render_toast(request, "Invalid credentials. Please check your email and password.", "error")

    # Authenticate credentials
    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        response = _render_toast(request, "Login successful! Redirecting...", "success")
        response["HX-Redirect"] = "/user/dashboard/"
        return response

    return _render_toast(request, "Invalid credentials. Please check your email and password.", "error")


@require_POST
def htmx_logout(request):
    """Logs out user and redirects to login."""
    logout(request)
    response = HttpResponse()
    response["HX-Redirect"] = "/auth/"
    return response