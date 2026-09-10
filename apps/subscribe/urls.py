from django.urls import path
from .views import subscribe_newsletter

urlpatterns = [
    # Ensure this matches the hx-post url or JS fetch url
    path('news/', subscribe_newsletter, name='subscribe'),
]