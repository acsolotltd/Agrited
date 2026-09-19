from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/apply/', views.job_apply, name='job_apply'),
]