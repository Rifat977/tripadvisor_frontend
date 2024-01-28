from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('Please enter an email address'))

        email=self.normalize_email(email)

        new_user=self.model(email=email,**extra_fields)

        new_user.set_password(password)

        new_user.save()

        return new_user


    def create_superuser(self,email,password,**extra_fields):

        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)


        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))


        return self.create_user(email,password,**extra_fields)
    



class User(AbstractUser):

    username = None
    email = models.EmailField(_("email address"),unique=True)
    create_account_otp = models.CharField(max_length=5,null=True, blank = True)

    dateEnrolled=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length = 255, null=True, blank=True)
    ratting = models.FloatField(default=0)
    profile = models.ImageField(upload_to='ProfilePhoto/',null=True,blank=True)
    password_reset_token = models.CharField(max_length=255, null=True, blank=True)
    password_reset_OTP = models.CharField(max_length=50, null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"