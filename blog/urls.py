from django.urls import path

from .views import *

urlpatterns = [
   path('all_blog', blog, name="Blog"),


]
