from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("apps.core.urls")),
    path('user/', include("apps.orders.urls")),
    path('auth/', include("apps.accounts.urls")),
    path('subscribe/', include("apps.subscribe.urls")),
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]