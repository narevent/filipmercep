# website/urls.py - App URL Configuration
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('concerts/', views.concerts, name='concerts'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
]