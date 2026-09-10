from django.contrib import admin
from .models import NewsletterSubscriber
from apps.accounts.admin import AgritedAdmin
#from django.utils.html import format_html
from django.utils.safestring import mark_safe 

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

