import random

from django.contrib import messages
from django.contrib.auth.models import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from authentication.models import User


def register(request):

    if request.method == 'GET':
        return render(request,'register.html')
    
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:
            first_name = request.POST['first_name']
        except:
            first_name = None
        try:

            last_name = request.POST['last_name']
        except:
            last_name = None

        print(email)
        print(password)
        try:
            user = User.objects.create(email=email)
            user.set_password(password)
            user.save()
        except:
            messages.error(request,'Email Already Exist.')
            return redirect('/auth/register')
        otp = random.randint(1000,9999)
        user.create_account_otp = otp
        if first_name is not None:
            user.first_name = first_name
        
        if last_name is not None:
            user.last_name = last_name
        user.is_active = False
        user.save()

        send_mail(
            "OTP for Activate Your Account",
            f"{user.create_account_otp}",
            "shossain201214@bscse.uiu.ac.bd", # Email
            [user.email],
            fail_silently= False,
            )
            

        return redirect(f'/auth/cheak_otp/{user.id}')


def cheak_otp(request,pk):

    if request.method == 'GET':
        return render(request,'cheak_otp.html',context={'user':pk})
    
    if request.method == 'POST':
        otp_1 = request.POST['otp_1']
        otp_2 = request.POST['otp_2']
        otp_3 = request.POST['otp_3']
        otp_4 = request.POST['otp_4']
        otp = otp_1+otp_2+otp_3+otp_4
        try:
            user = User.objects.get(id=pk)
        except(ObjectDoesNotExist):
            return redirect('/auth/register')
        
        if user.create_account_otp !=otp:
            otp = random.randint(1000,9999)
            user.create_account_otp = otp
            user.save()
            messages.error(request,'OTP NOT CORRECT')
            return redirect(f'/auth/cheak_otp{user.id}')
        
        else:
            user.is_active = True
            user.create_account_otp = random.randint(1000,9999)
            user.save()
            auth.login(request,user)
            



        return redirect('/')
        

        
def login(request):

    if request.method == 'GET':

        return render(request,'login.html')
    
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                auth.login(request,user)
            else:
                messages.error(request,'Account is not Active .')
                return redirect('/auth/cheak_otp')
        else:

            messages.error(request,'User Not Found.')
            return redirect('/auth/login')
        return redirect('/')

        

def logout(request):

    auth.logout(request)
    return redirect('/')


def forgot_password(request):

    if request.method == 'GET':
        return render(request,'enter_email_for_forget_password.html')
    
    if request.method == 'POST':

        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except(ObjectDoesNotExist):
            return render(request,'msg.html',context={'msg':'User Not Exist.'})
        
        user.password_reset_token = random.randint(1000,9999)
        user.save(update_fields=["password_reset_token"])

        send_mail(
            "For Reset Password ",
            f"http://localhost:8000/auth/reset_password/{user.password_reset_token}/{user.id}",
            "shossain201214@bscse.uiu.ac.bd", # Email
            [user.email],
            fail_silently= False,
            )

        return render(request,'msg.html',context={'msg':'Password Reset URL Send to your Email'})
    


def reset_password(request,pk,uid):

    if request.method == 'GET':
        try:
            user = User.objects.get(id=uid)
        except(ObjectDoesNotExist):
            return render(request,'msg.html',context={'msg':'User Not Exist.'})
        
        if user.password_reset_token == pk:

            auth.login(request,user)

            return render(request,'forget_pass.html')
        
def change_password(request):
        
    if request.method == 'POST':

        new_pass = request.POST['password']

        user = request.user
        user.set_password(new_pass)
        user.save()

        return redirect('/auth/login')
        

  
