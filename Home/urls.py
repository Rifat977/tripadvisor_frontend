from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
   path('', home, name="home"),
   path('event', event, name="event"),
   path('profile', profile, name = 'edit your profile' ),




   path('places', places, name="places"),
   path('chat', chat, name="Rendiring place chat page"),
   path('sub_place', sub_place, name="Rendiring place chat page"),
   path('select_sub_place', sub_sub_place, name="select_sub_place"),
   path('sub_place_chatbox', sub_place_chatbox, name="sub_place_chatbox"),
   path('hotels', hotels, name="hotels"),


   path('info', info, name="info"),
   
   path('event/<int:pk>', event_view, name="View Event "),
   path('weather', weather, name="weather"),
   path('get_weather/', get_weather, name='get_weather'),

]
