from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('login/', views.htmx_login, name='login'),
    path('signup/', views.htmx_signup, name='signup'),
    path('logout/', views.htmx_logout, name='logout'),
    path('', views.auth_page, name='auth'), #
]