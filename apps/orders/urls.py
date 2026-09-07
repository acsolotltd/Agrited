from django.urls import path
from .views import BookingRequestAPIView

urlpatterns = [
    path('', BookingRequestAPIView.as_view(), name='api_create_booking'),
]