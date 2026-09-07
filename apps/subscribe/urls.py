from django.urls import path
from .views import SubscribeNewsletterAPIView

urlpatterns = [
    # Ensure this matches the hx-post url or JS fetch url
    path('news/', SubscribeNewsletterAPIView.as_view(), name='api_newsletter_subscribe'),
]