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
   path('select_sub_place', sub_sub_place, name="Rendiring place chat page"),
   path('find_place_chatbox', find_place_chatbox, name="find_place_chatbox"),
   path('sub_place_chatbox', sub_place_chatbox, name="sub_place_chatbox"),
   path('hotels', hotels, name="hotels"),
   path('hotels_preference_chatbox', hotels_preference_chatbox, name="hotels_preference_chatbox"),

   path('submit_places', submit_places, name="submit_places"),


   path('info', info, name="info"),
   
   path('event/<int:pk>', event_view, name="View Event "),
   path('weather', weather, name="weather"),
   path('get_weather/', get_weather, name='get_weather'),


   path('save/', save_main_csv, name='Save main csv'),
   
]
