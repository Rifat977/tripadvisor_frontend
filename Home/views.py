from datetime import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from blog.models import *
from .models import *

from .accom import *

import json

from django.shortcuts import render, get_object_or_404

from django.apps import apps

# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from scipy.sparse import vstack

# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')

import os

def home(request):
    blogs = Blog.objects.all().order_by('-id')[:5]
    return render(request,'home.html', context={'blogs':blogs})

@csrf_exempt
def hotels(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            places = data.get('places', [])

            if not places:
                return JsonResponse({'status': 'error', 'message': 'No places provided'}, status=400)

            place_name = places[0]

            place = get_object_or_404(Places, place_name=place_name)

            location = place.location

            print(location)

            # Get coordinates using the Nominatim API
            coordinates = get_coordinates(api_key=None, location=location)

            if coordinates:
                # Specify the search radius in meters (optional, default is 1000 meters)
                radius = 2000
                # Search for hotels using the Overpass API
                hotels = search_hotels(api_key=None, coordinates=coordinates, radius=radius)

                # Accumulate hotel information in a list
                hotels_info = []

                for hotel in hotels:
                    lat = hotel.get('lat', 'N/A')
                    lon = hotel.get('lon', 'N/A')
                    tags = hotel.get('tags', {})
                    
                    # Check if 'name' attribute exists in 'tags' dictionary
                    if 'name' in tags:
                        hotel_info = {'latitude': lat, 'longitude': lon, 'tags': tags}
                        hotels_info.append(hotel_info)

                return JsonResponse({'status': 'success', 'hotels': hotels_info})
            else:
                return JsonResponse({'status': 'error', 'message': 'Unable to get coordinates for the location'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

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

    Places = apps.get_model('Home', 'Places')

    if request.method == 'POST':
        user_message = request.POST.get('userInput', '')
        place_name = request.POST.get('selectedItem', '')

        place = get_object_or_404(Places, place_name=place_name)
        place_location = place.location
        if "," in place_location:
            place_location = place_location.split(",")[1]


        filtered_places = Places.objects.filter(location__icontains=place_location)

        vectorizer = TfidfVectorizer()
        documents = df[['Place Name', 'Description', 'Category']].fillna('').values.tolist()
        user_vector = vectorizer.fit_transform([user_message])
        document_vectors = vectorizer.transform([' '.join(doc) for doc in documents])
        similarities = cosine_similarity(user_vector, document_vectors).flatten()

        place_similarity_mapping = dict(zip(filtered_places, similarities))

        sorted_places = [(place, similarity) for place, similarity in place_similarity_mapping.items() if similarity > 0]

        sorted_places = sorted(sorted_places, key=lambda x: x[1], reverse=True)
        
        suggestions = [{'place_name': place.place_name,
                        'location': place.location,
                        'description': place.description,
                        'category': place.category,
                        'fee': place.fee,
                        'opening_hour': place.opening_hour,
                        'similarity': similarity} for place, similarity in sorted_places]

        print(place_location, user_message)
        print(suggestions)

        return JsonResponse({'suggestions': suggestions})

    return render(request, 'select_sub_place_chat.html')

@csrf_exempt
def find_place_chatbox(request):
    file_path = 'main.csv'  
    df = pd.read_csv(file_path)
    
    if request.method == 'POST':
        user_message = request.POST.get('userInput', '')

        print(user_message)

        # Combine 'Category' and 'Description'
        df['Combined Features'] = df['Category'] + ' ' + df['Description']

        # Tokenization and Lemmatization
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        def preprocess(text):
            tokens = word_tokenize(text)
            tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha() and token.lower() not in stop_words]
            return ' '.join(tokens)

        df['Combined Features'] = df['Combined Features'].fillna('').apply(preprocess)
        user_message = preprocess(user_message)

        # TF-IDF Vectorization
        vectorizer = TfidfVectorizer()
        user_message_vector = vectorizer.fit_transform([user_message])
        places_vectors = vectorizer.transform(df['Combined Features'])

        # Cosine Similarity
        cosine_similarities = cosine_similarity(user_message_vector, places_vectors).flatten()

        # Get the index of the top match
        top_match_indices = cosine_similarities.argsort()[::-1][:2]
    
        suggestions = []
        for index in top_match_indices:
            match_details = df.iloc[index]

            place_name = match_details['Place Name']

            place = get_object_or_404(Places, place_name=place_name)
            
            suggestion = {
                'Place Name': place.place_name,
                'Category': place.category,
                'Description': place.description,
                'Location': place.location,
                'Entry Fee': place.fee,
                'Opening Hours': place.opening_hour,
                'Image': place.imeage.url if place.imeage else None,
            }
            
            suggestions.append(suggestion)

        print(suggestions)

        return JsonResponse({'suggestions': suggestions})
    
    return render(request, 'select_place_chat.html')


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