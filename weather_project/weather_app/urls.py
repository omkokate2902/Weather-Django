# weather_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/weather/', views.get_weather, name='get_weather'),
    path('api/available_cities/', views.get_available_cities, name='get_available_cities'),  # Add this URL pattern
    path('', views.weather_app_home, name='weather_app_home'),
]
