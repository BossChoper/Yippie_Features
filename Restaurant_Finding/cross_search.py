import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_google_maps_place(restaurant_name, location):
    """
    Fetch restaurant details from Google Maps Places API.
    """
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": restaurant_name,
        "location": location,
        "radius": 5000,  # Search within 5 km radius
        "key": GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            return data["results"][0]  # Return the first result
        else:
            print("No results found on Google Maps.")
            return None
    else:
        print(f"Error fetching data from Google Maps: {response.status_code}")
        return None

def search_restaurantji(restaurant_name):
    """
    Search for the restaurant on the Restaurantji website.
    """
    base_url = "https://www.restaurantji.com/search/"
    search_query = urllib.parse.quote(restaurant_name)
    search_url = f"{base_url}{search_query}/"
    
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='restaurant')
        
        if results:
            print(f"Found {len(results)} results on Restaurantji:")
            for result in results[:5]:  # Display top 5 results
                name = result.find('h2').text.strip()
                address = result.find('p', class_='address').text.strip() if result.find('p', class_='address') else "No address available"
                print(f"- {name}, Address: {address}")
        else:
            print("No matching restaurants found on Restaurantji.")
    else:
        print(f"Error fetching data from Restaurantji: {response.status_code}")

if __name__ == "__main__":
    # Input restaurant name and location (latitude,longitude)
    restaurant_name = input("Enter the restaurant name: ")
    location = input("Enter the location (latitude,longitude): ")
    
    # Step 1: Find the restaurant on Google Maps
    place_details = get_google_maps_place(restaurant_name, location)
    
    if place_details:
        print("\nRestaurant found on Google Maps:")
        print(f"Name: {place_details['name']}")
        print(f"Address: {place_details.get('formatted_address', 'No address available')}")
        
        # Step 2: Search for the restaurant on Restaurantji
        print("\nSearching for the restaurant on Restaurantji...")
        search_restaurantji(place_details['name'])
