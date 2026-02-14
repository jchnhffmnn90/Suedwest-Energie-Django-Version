from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ueber-uns/', views.about, name='about'),
    path('leistungen/', views.services, name='services'),
    path('ablauf/', views.process, name='process'),
    path('kontakt/', views.contact, name='contact'),
    path('impressum/', views.imprint, name='imprint'),
    path('datenschutz/', views.privacy, name='privacy'),
    path('health/', views.health_check, name='health_check'),
    path('status/', views.status_view, name='status'),
    path('agb/', views.terms, name='terms'),
]