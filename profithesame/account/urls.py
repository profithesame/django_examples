from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('logout/', views.user_logout, name='logout'),

    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]
