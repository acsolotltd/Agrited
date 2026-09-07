from django.contrib import admin
from .models import BookingRequest
from apps.accounts.admin import AgritedAdmin
@admin.register(BookingRequest)
class OrderAdmin(AgritedAdmin):
    # Assuming your Order model has fields like order_id, customer, product, quantity, status
    list_display = ( 'user', 'product', 'quantity', 'payment_status_badge', 'created_at')
    list_filter = ('status', 'product', 'created_at')
    search_fields = ('order_id', 'user', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('user', 'phone_number', 'email')
        }),
        ('Order Details', {
            'fields': ('product', 'quantity', 'notes')
        }),
        ('Processing', {
            'fields': ('status', 'assigned_agent', 'created_at', 'updated_at')
        }),
    )

    def payment_status_badge(self, obj):
        # Color-code based on Agrited order statuses (e.g., Pending, Confirmed, Shipped)
        colors = {
            'pending': ('#fef3c7', '#92400e'),   # Amber
            'confirmed': ('#dbeafe', '#1e40af'), # Blue
            'shipped': ('#d1fae5', '#065f46'),   # Emerald
            'cancelled': ('#fee2e2', '#991b1b'), # Red
        }
        bg_color, text_color = colors.get(obj.status.lower(), ('#f3f4f6', '#374151'))
        
        return format_html(
            f'<span style="background-color: {bg_color}; color: {text_color}; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase;">{obj.status}</span>'
        )
    payment_status_badge.short_description = 'Order Status'
