from django.contrib import admin
from .models import NewsletterSubscriber
from apps.accounts.admin import AgritedAdmin
from django.utils.safestring import mark_safe 
"""
@admin.register(NewsletterSubscriber)
class SubscriberAdmin(AgritedAdmin):
    list_display = ('email', 'name', 'status_badge', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    date_hierarchy = 'subscribed_at'
    
    def status_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Active</span>'
            )
        return mark_safe(
            '<span style="background-color: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Unsubscribed</span>'
        )
    status_badge.short_description = 'Subscription Status'
"""


# admin.py
from django.contrib import admin, messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import BulkEmailForm

@admin.action(description="Send email blast to selected subscribers")
def send_bulk_email_admin_action(modeladmin, request, queryset):
    # Filter for active subscribers
    active_subscribers = queryset.filter(is_active=True)
    
    if not active_subscribers.exists():
        modeladmin.message_user(request, "No active subscribers were selected.", messages.WARNING)
        return None

    # Dynamically resolve the changelist URL for the cancel button
    changelist_url = reverse(f"admin:{modeladmin.model._meta.app_label}_{modeladmin.model._meta.model_name}_changelist")

    if 'apply' in request.POST:
        form = BulkEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']

            # 1. Extract a flat list of email addresses
            recipient_emails = list(active_subscribers.values_list('email', flat=True))

            # 2. Render the HTML fallback template 
            html_content = render_to_string('emails/bulk_email_base.html', {'message': message_text})

            # 3. Build a SINGLE email message
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_emails,  # Pass all emails into the 'to' list
            )
            msg.attach_alternative(html_content, "text/html")

            # 4. THE MAGIC BULLET: Force Anymail/Brevo into Batch Mode
            msg.merge_data = {email: {} for email in recipient_emails}

            try:
                # Dispatches the single API request to Brevo
                msg.send(fail_silently=False)
                
                modeladmin.message_user(
                    request, 
                    f"Success! Campaign dispatched to {len(recipient_emails)} subscribers.", 
                    messages.SUCCESS
                )
            except Exception as e:
                modeladmin.message_user(
                    request, 
                    f"Brevo API Error: {str(e)}", 
                    messages.ERROR
                )

            return HttpResponseRedirect(changelist_url)
    else:
        form = BulkEmailForm()

    # Render intermediate confirmation form
    return render(
        request,
        'admin/send_bulk_email.html',
        context={
            'title': 'Compose Email Blast',
            'subscribers': active_subscribers,
            'form': form,
            'opts': modeladmin.model._meta,
            'queryset': active_subscribers,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
            'cancel_url': changelist_url,
        }
    )

@admin.register(NewsletterSubscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active',)
    actions = [send_bulk_email_admin_action]
