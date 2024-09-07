from django.urls import path
from . import views

app_name = 'restaurant_app'
urlpatterns = [
    path('', views.restaurant_mainPage, name='food_mainPage'),
]
