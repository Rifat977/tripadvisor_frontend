from datetime import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from blog.models import *
from .models import *

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os


def home(request):
    blogs = Blog.objects.all().order_by('-id')[:5]
    return render(request,'home.html', context={'blogs':blogs})

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

@csrf_exempt
def sub_place_chatbox(request):
    file_path = 'main.csv'  
    df = pd.read_csv(file_path)
    
    if request.method == 'POST':
        user_message = request.POST.get('userInput', '')

        df['Combined Features'] = df['Category'] + ' ' + df['Description']

        vectorizer = TfidfVectorizer(stop_words='english')
        user_message_vector = vectorizer.fit_transform([user_message])

        places_vectors = vectorizer.transform(df['Combined Features'].fillna(''))

        cosine_similarities = cosine_similarity(user_message_vector, places_vectors).flatten()

        best_match_index = cosine_similarities.argmax()

        best_match_details = df.iloc[best_match_index]

        bot_response = "Place Name: {},\nCategory: {},\nDescription: {},\nLocation: {},\nEntry Fee (BDT): {},\nOpening Hours: {}".format(
            best_match_details['Place Name'],
            best_match_details['Category'],
            best_match_details['Description'],
            best_match_details['Location'],
            best_match_details['Entry Fee (BDT)'],
            best_match_details['Opening Hours']
        )

        return JsonResponse({'message': bot_response})
    return render(request,'select_sub_place_chat.html')


def event(request):
    events = Events.objects.all().order_by('-id')
    return render(request, 'event.html',context={'events':events})

def event_view(request,pk):
    try:
        event = Events.objects.get(id=pk)
    except(ObjectDoesNotExist):
        return redirect('/event')
    
    return render(request,'events_view.html', context={'event':event})

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



def profile(request):

    if request.user.is_authenticated:

        if request.method == 'GET':
            return render(request,'info.html')
        
        if request.method == 'POST':

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            details  = request.POST['details']
            profile = request.FILES['profile']
            rating = request.POST['rating']

            user = User.objects.get(email = request.user.email)

            user.first_name = first_name
            user.last_name = last_name
            user.address = details
            user.profile = profile
            user.ratting = rating
            user.save()
            return redirect('/profile')
        
    else:

        return redirect('/auth/login')
        