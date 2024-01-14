from django.urls import path

from .views import *

urlpatterns = [
   path('login', login, name="Login"),
   path('register', register, name="Register"),
   path('logout', logout, name="Logout"),
   path('cheak_otp/<int:pk>', cheak_otp, name="Cheak Create account OTP."),

]
