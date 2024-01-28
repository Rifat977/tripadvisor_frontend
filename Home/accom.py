import requests

def get_coordinates(api_key, location):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json',
        'limit': 1,
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data:
        coordinates = (float(data[0]['lat']), float(data[0]['lon']))
        return coordinates
    else:
        print(f"Location '{location}' not found.")
        return None

def search_hotels(api_key, coordinates, radius=1000, search_type='tourism', search_vlaue='hotel'):
    base_url = "https://overpass-api.de/api/interpreter"
    query = (
        f"[out:json];"
        f"node(around:{radius},{coordinates[0]},{coordinates[1]})['{search_type}'='{search_vlaue}'];"
        f"out center;"
    )
    response = requests.post(base_url, data=query)
    data = response.json()

    # print("\n===========\n")
    # print(data)

    if 'elements' in data:
        return data['elements']



if __name__ == "__main__":
    # Specify the location (Dhaka, Bangladesh)
    location = "Dhaka, Bangladesh"
    
    # Get coordinates using the Nominatim API
    coordinates = get_coordinates(api_key=None, location=location)

    if coordinates:
        # Specify the search radius in meters (optional, default is 1000 meters)
        radius = 2000
        
        # Search for hotels using the Overpass API
        search_hotels(api_key=None, coordinates=coordinates, radius=radius)
