from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include("apps.orders.urls")),
    path('subscribe/', include("apps.subscribe.urls")),
]
