from django.urls import path
from .views import submit_booking, htmx_cancel_booking, dashboard

urlpatterns = [
    path('bookings', submit_booking, name='booking'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/booking/<int:booking_id>/cancel/', htmx_cancel_booking, name='cancel_booking'),
]