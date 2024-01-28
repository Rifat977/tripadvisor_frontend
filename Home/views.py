from datetime import datetime
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from blog.models import *
from .models import *

from .accom import *

from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.template.loader import get_template
import tempfile
from django.template.loader import render_to_string
import weasyprint

import json, base64

from django.shortcuts import render, get_object_or_404
from django.apps import apps

from math import radians, sin, cos, sqrt, atan2

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression  # Import your desired model

import pandas as pd
import numpy as np
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

import os, time, random

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def home(request):
    blogs = Blog.objects.all().order_by('-id')[:5]
    return render(request,'home.html', context={'blogs':blogs})

@csrf_exempt
def hotels(request):
    place_names_param = request.GET.get('placeNames', '')
    place_names = place_names_param.split(',')

    LatLon = []

    for place_name in place_names:
        place = get_object_or_404(Places, place_name=place_names[0])

        location = place.location
        location = location.split(",")
        location = location[len(location) - 1]
        coordinates = get_coordinates(api_key=None, location=location)
        LatLon.append(coordinates)

    return render(request, 'hotels.html', {'lat': coordinates[0], 'lon': coordinates[1], 'LatLon': LatLon})



# Load and preprocess data
df = pd.read_csv('hotels.csv')

features = df[['Description', 'Facilities', 'Min Price (USD)', 'Max Price (USD)']]
labels = df['Hotel Name']

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(features.apply(lambda x: ' '.join(map(str, x)), axis=1))

df['Amenities'] = df.apply(lambda x: ', '.join(x['Facilities']), axis=1) 

# Use Logistic Regression's probability outputs
model = LogisticRegression()
model.fit(X, labels)

@csrf_exempt
def hotels_preference_chatbox(request):

    if request.method == "POST":

        user_message = request.POST.get('userInput', '')
        selectedPlaces = request.POST.getlist('selectedPlaces[]', '')  # Use getlist to retrieve multiple values
        
        user_input_vector = vectorizer.transform([user_message])

        has_dataset = False
        for selectedPlace in selectedPlaces:
            place = get_object_or_404(Places, place_name=selectedPlace)
            if "Patenga" in place.location or "Agrabad" in place.location:
                has_dataset = True
                break

        if has_dataset:
            # Get probability outputs
            probabilities = model.predict_proba(user_input_vector)
            
            # Sort by highest probability
            sorted_indexes = np.argsort(-probabilities, axis=1)[:, :3]
            suggested_hotels = []
            suggested_info = []
            hotel_locations = []

            
            for index in sorted_indexes[0]:
                hotel_name = model.classes_[index]
                hotel_info = df[df['Hotel Name'] == hotel_name].to_dict('records')[0]
                hotel_info['random'] = random.randint(0,99)
                suggested_hotels.append(hotel_name)
                suggested_info.append(hotel_info)
                hotel_locations.append(hotel_info['Address'])

            print(hotel_locations)
                
            # Return top k suggestions
            return JsonResponse({'suggestions': suggested_info, 'hotel_location':hotel_locations}) 
        else:
            place = get_object_or_404(Places, place_name=selectedPlaces[0])
            location = place.location
            location = location.split(",")
            location = location[len(location) - 1]
            coordinates = get_coordinates(api_key=None, location=location)

            hotels_info = []
            
            if coordinates:
                radius = 50000
                hotels = search_hotels(api_key=None, coordinates=coordinates, radius=radius)

                for hotel in hotels:
                    lat = hotel.get('lat', 'N/A')
                    lon = hotel.get('lon', 'N/A')
                    tags = hotel.get('tags', {})

                    if 'name' in tags:
                        hotel_info = {'latitude': lat, 'longitude': lon, 'tags': tags, 'place_name': selectedPlaces[0], 'location': place.location, 'random_number': random.randint(0, 99)}

                        distance = calculate_distance(coordinates[0], coordinates[1], float(lat), float(lon))
                        hotel_info['distance'] = round(distance, 2)

                        hotels_info.append(hotel_info)

            sorted_hotels_info = sorted(hotels_info, key=lambda x: x['distance'])
            top_3_hotels = sorted_hotels_info[:3]  # Take the top 3 hotels

            return JsonResponse({'suggestions2': top_3_hotels, 'location': location})


    return render(request, 'hotel_preference_chat.html')


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
        place_name = request.POST.get('selectedItem', '')

        place = get_object_or_404(Places, place_name=place_name)
        place_location = place.location
        if "," in place_location:
            place_location = place_location.split(",")[1]

        filtered_places = Places.objects.filter(location__icontains=place_location)[:5]

        suggestions = [{'place_name': place.place_name,
                        'location': place.location,
                        'description': place.description,
                        'category': place.category,
                        'fee': place.fee,
                        'opening_hour': place.opening_hour,
                        } for place in filtered_places]


        print(place_location)
        print(suggestions)

        return JsonResponse({'suggestions': suggestions})

    return render(request, 'select_sub_place_chat.html')

@csrf_exempt
def find_place_chatbox(request):
    
    if request.method == 'POST':
        file_path = 'main.csv'  
        df = pd.read_csv(file_path)
    
        user_message = request.POST.get('userInput', '')

        print(user_message)

        # Combine 'Category' and 'Description'
        df['Combined Features'] = df['Place Name'] + ' ' + df['Category'] + ' ' + df['Description']

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
        top_match_indices = cosine_similarities.argsort()[::-1][:3]
    
        suggestions = []
        for index in top_match_indices:
            match_details = df.iloc[index]

            place_name = match_details['Place Name']

            try:

                places_instances = Places.objects.filter(place_name=place_name)

                if not places_instances.exists():
                    print('Place not found')

                # Assuming you want to take the first instance if there are multiple ones
                place = places_instances.first()
                
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
            except Exception as e:
                print(e)

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


def create_pdf(selected_places, hotels_data):
    pdf_filename = "content_pdf.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 700, "TripAdvisor Overview")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 14)

    # Draw selected places
    c.drawString(50, 670, "Selected Places:")
    for i, place in enumerate(selected_places):
        c.drawString(70, 650 - (i * 20), f"{place}")


    # Draw hotels data
    c.drawString(50, 620, "Hotels Data:")
    for i, hotel in enumerate(hotels_data):
        c.drawString(70, 600 - (i * 20), f"{i + 1}. {hotel['name']} - (Distance: {hotel['distance']}KM)")

    c.save()

    # return pdf_filename


@csrf_exempt
def submit_places(request):
    if request.method == 'POST':
        selected_places = json.loads(request.POST.get('selected_places'))
        hotels_data = json.loads(request.POST.get('hotels_data'))

        if not selected_places or not hotels_data:
            return HttpResponseBadRequest()


        pdf_content = create_pdf(selected_places, hotels_data)

        response_data = {
            'success': True,
            'pdf_content': pdf_content,
        }

        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Invalid form data'}, status=400)
        