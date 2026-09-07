# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import EmailBasedUser

admin.site.site_header = "Agrited Administration"
admin.site.site_title = "Agrited Admin Portal"
admin.site.index_title = "Welcome to the Operations Dashboard"

class AgritedAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('admin/css/agrited_theme.css',)
        }

@admin.register(EmailBasedUser)
class CustomAccountAdmin(UserAdmin, AgritedAdmin):
    list_display = ('email', 'full_name', 'role_badge', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined') # Add custom roles here
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)
    
    def role_badge(self, obj):
        if obj.is_superuser:
            return format_html('<span style="background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Admin</span>')
        elif obj.is_staff:
            return format_html('<span style="background: #f3e8ff; color: #6b21a8; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Agent</span>')
        return format_html('<span style="background: #f3f4f6; color: #4b5563; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Customer</span>')
    role_badge.short_description = 'Account Role'