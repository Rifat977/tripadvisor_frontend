from django.urls import path

from .views import *

urlpatterns = [
   path('login', login, name="Login"),
   path('register', register, name="Register"),
   path('logout', logout, name="Logout"),
   path('cheak_otp/<int:pk>', cheak_otp, name="Cheak Create account OTP."),
   path('forgot_password', forgot_password, name="forgot_password"),
   path('reset_password/<str:pk>/<int:uid>', reset_password, name="Cheak Create account OTP."),
   path('change_passeord', change_password, name="Change Password"),

]
