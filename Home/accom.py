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

def search_hotels(api_key, coordinates, radius=1000):
    base_url = "https://overpass-api.de/api/interpreter"
    query = (
        f"[out:json];"
        f"node(around:{radius},{coordinates[0]},{coordinates[1]})['tourism'='hotel'];"
        f"out;"
    )
    response = requests.post(base_url, data=query)
    data = response.json()

    if 'elements' in data:
        return data['elements']

    # Process the search results
    # if 'elements' in data:
    #     hotels = data['elements']
    #     for hotel in hotels:
    #         print("Hotel Details:")
    #         print(f"  Type: {hotel.get('type', 'N/A')}")
    #         print(f"  ID: {hotel.get('id', 'N/A')}")
    #         print(f"  Latitude: {hotel.get('lat', 'N/A')}")
    #         print(f"  Longitude: {hotel.get('lon', 'N/A')}")
            
    #         tags = hotel.get('tags', {})
    #         print("  Tags:")
    #         for key, value in tags.items():
    #             print(f"    {key}: {value}")

    #         print('-' * 30)
    # else:
    #     print("No results found.")
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
