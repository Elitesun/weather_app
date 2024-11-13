from django.urls import path
from .views import WeatherView

app_name='weather_app'

urlpatterns=[
    path('',WeatherView.as_view() , name='weather' )
    
]