from django.urls import path

from .views import *

urlpatterns = [
   path('all_blog', blog, name="Blog"),
   path('create_blog', create_blog, name="Create Blog"),


]
