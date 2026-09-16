from django.urls import path
from .views import submit_booking, htmx_cancel_booking, dashboard, booking_details

urlpatterns = [
    path('bookings', submit_booking, name='submit_booking'),
    path('dashboard/', dashboard, name='dashboard'),
    path('booking-details/', booking_details, name='booking_details'),
    path('dashboard/booking/<int:booking_id>/cancel/', htmx_cancel_booking, name='cancel_booking'),
]