from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('submit-contact/', views.contact_submit, name='submit_contact'),
    path('products/', views.products, name='products'),
]