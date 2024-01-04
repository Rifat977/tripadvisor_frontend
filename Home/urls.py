from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
   path('', home, name="Rendiring Homepage"),
   path('places', places, name="Rendiring places"),
   path('chat', chat, name="Rendiring place chat page"),
   path('sub_place', sub_place, name="Rendiring place chat page"),
   path('select_sub_place', sub_sub_place, name="Rendiring place chat page"),
   path('sub_place_chatbox', sub_place_chatbox, name="Rendiring place chat page"),
   path('hotels', hotels, name="hotels"),

   path('login', login, name="login"),
   path('register', register, name="register"),
   path('blog', blog, name="blog"),

   path('info', info, name="info"),

]
