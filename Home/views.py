from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import datetime 

def home(request):
    return render(request,'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def blog(request):
    return render(request, 'blog.html')

def hotels(request):
    return render(request, 'hotels.html')

def info(request):
    return render(request, 'info.html')


def places(request):
    return render(request,'places.html')


def chat(request):
    return render(request,'place_chat.html')


def sub_place(request):
    return render(request,'select_place.html')


def sub_sub_place(request):
    return render(request,'select-sub-place.html')


def sub_place_chatbox(request):
    return render(request,'select_sub_place_chat.html')


def event(request):
    return render(request, 'event.html')

def weather(request):
    return render(request, 'weather.html')

def get_weather(request):
    input_date = request.GET.get('selected_date')
    city = request.GET.get('selected_city')

    api_key = "69a115bda020439bbab164500240601"
    base_url = "http://api.weatherapi.com/v1/history.json?"

    year, month, day = map(int, input_date.split('-'))
    date = datetime(year, month, day)
    
    formatted_date = date.strftime('%Y-%m-%d')

    complete_url = f"{base_url}key={api_key}&q={city}&dt={formatted_date}"
    
    response = requests.get(complete_url)
    
    data = response.json()
    

    return JsonResponse({'weather_data': data})