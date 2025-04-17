# Non-Functional
import requests
import re
from bs4 import BeautifulSoup

GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

def get_google_maps_place(restaurant_name, location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": restaurant_name,
        "location": location,
        "radius": 5000,
        "key": GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])[0] if data.get("results") else None
    return None

def generate_restaurantji_url(place_details):
    address = place_details.get("formatted_address", "")
    parts = [p.strip() for p in address.split(",")]
    
    if len(parts) < 3:
        return None

    # Extract state (2-letter code)
    state = parts[-2].split()[0].lower()
    
    # Extract and format city
    city = parts[-3].replace(" ", "-").lower()
    
    # Format restaurant name
    name = re.sub(r"[^a-z0-9]+", "-", place_details["name"].lower()).strip("-")
    
    # Create unique identifier from place_id digits
    place_id = place_details.get("place_id", "")
    digits = "".join(filter(str.isdigit, place_id))[-4:] or "1"
    
    return f"https://www.restaurantji.com/{state}/{city}/{name}-{digits}/menu/"

def verify_restaurantji_url(url):
    response = requests.get(url)
    return response.status_code == 200

if __name__ == "__main__":
    restaurant_name = input("Enter restaurant name: ")
    location = input("Enter location (lat,lng): ")
    
    place = get_google_maps_place(restaurant_name, location)
    
    if place:
        print(f"\nGoogle Maps Result: {place['name']}")
        print(f"Address: {place.get('formatted_address', 'N/A')}")
        
        rji_url = generate_restaurantji_url(place)
        print(f"\nGenerated Restaurantji URL:\n{rji_url}")
        
        if verify_restaurantji_url(rji_url):
            print("\n✅ Valid menu page found!")
        else:
            print("\n⚠️ Direct link not found, try searching manually:")
            print(f"https://www.restaurantji.com/search/{urllib.parse.quote(place['name'])}/")
