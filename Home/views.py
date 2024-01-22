import os
from datetime import datetime

import pandas as pd
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from authentication.models import User
from blog.models import *

from .models import *


def home(request):
    blogs = Blog.objects.all().order_by('-id')[:5]
    return render(request,'home.html', context={'blogs':blogs})

def hotels(request):
    return render(request, 'hotels.html')

def info(request):
    return render(request, 'info.html')


def places(request):

    first_place = Places.objects.all().last()
    random_two_place = Places.objects.filter(id__lt = 4, id__gt = 1)

    return render(request,'places.html',context={'first_place':first_place,'random_two_place': random_two_place})


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

        top_n_matches_indices = cosine_similarities.argsort()[-2:][::-1]

        suggestions = []
        for index in top_n_matches_indices:
            match_details = df.iloc[index]
            suggestion = {
                'Place Name': match_details['Place Name'],
                'Category': match_details['Category'],
                'Description': match_details['Description'],
                'Location': match_details['Location'],
                'Entry Fee (BDT)': match_details['Entry Fee (BDT)'],
                'Opening Hours': match_details['Opening Hours']
            }
            suggestions.append(suggestion)

        print(suggestions)

        return JsonResponse({'suggestions': suggestions})
    return render(request, 'select_sub_place_chat.html')


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
        



def save_main_csv(request):


    df = pd.read_csv('main.csv', header=None)
    for i, row in df.iterrows():

        print(row[0])
        place_name = row[0]
        category = row[1]
        description = row[2]
        location = row[3]
        fee = row[4]
        opening_hour = row[5]

        objj = Places.objects.create(place_name=place_name,category=category,description=description,location=location,fee=fee,opening_hour=opening_hour)
        objj.save()
    return JsonResponse({'hello':'world'})
