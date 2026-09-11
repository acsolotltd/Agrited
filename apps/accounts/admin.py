# admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe 
from django.contrib.auth.admin import UserAdmin
from .models import EmailBasedUser
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.site_header = "Agrited Administration"
admin.site.site_title = "Agrited Admin Portal"
admin.site.index_title = "Welcome to the Operations Dashboard"

class AgritedAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('apps/admin/css/agrited_theme.css',)
        }

@admin.register(EmailBasedUser)
class CustomAccountAdmin(UserAdmin, AgritedAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number')}),
        ('Permissions & Roles', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', )}),
    )
    readonly_fields = ('date_joined',)
    # 2. Add User Page: Configure fields for creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'full_name', 'role_badge', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    def role_badge(self, obj):
        if obj.is_superuser:
            return mark_safe('<span style="background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Admin</span>')
        elif obj.is_staff:
            return mark_safe('<span style="background: #f3e8ff; color: #6b21a8; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Agent</span>')
        return mark_safe('<span style="background: #f3f4f6; color: #4b5563; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Customer</span>')
    role_badge.short_description = 'Account Role'