from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^about/', views.about, name='about'),
    re_path(r'^contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
]