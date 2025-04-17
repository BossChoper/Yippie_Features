# Functional; gets tags of restaurants near an address
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your Google API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# List of predefined place types from Google Places API documentation
# Source: https://developers.google.com/places/web-service/supported_types
PREDEFINED_PLACE_TYPES = [
    "bakery",
    "bar",
    "cafe",
    "restaurant",
    "meal_delivery",
    "meal_takeaway",
    "food",
    "convenience_store",
    "grocery_or_supermarket",
    "liquor_store",
    "donut_shop",  # Not explicitly listed but commonly observed
    # Add more from the official list as needed
]

def list_predefined_types():
    """Print the predefined Google Places API place types."""
    print("Predefined Google Places API Place Types:")
    for place_type in PREDEFINED_PLACE_TYPES:
        print(f"- {place_type}")

def fetch_place_types_from_api(location="40.7128,-74.0060", radius=5000):
    """
    Query Google Places API to fetch place types dynamically.
    Location: latitude,longitude (default: New York City).
    Radius: search radius in meters.
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": "restaurant",  # Broad category to capture food-related places
        "key": API_KEY
    }

    unique_types = set()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])

        for place in results:
            place_types = place.get("types", [])
            unique_types.update(place_types)

        print("\nDynamically Fetched Place Types from API:")
        for place_type in sorted(unique_types):
            print(f"- {place_type}")

    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")

def main():
    # Step 1: List predefined types
    list_predefined_types()

    # Step 2: Fetch additional types from API (optional)
    if API_KEY != 'YOUR_API_KEY':
        fetch_place_types_from_api()
    else:
        print("\nNote: To fetch dynamic place types, replace 'YOUR_API_KEY' with a valid Google API key.")

if __name__ == "__main__":
    main()

""" Example output:
Predefined Google Places API Place Types:
- bakery
- bar
- cafe
- restaurant
- meal_delivery
- meal_takeaway
- food
- convenience_store
- grocery_or_supermarket
- liquor_store
- donut_shop

Dynamically Fetched Place Types from API:
- art_gallery
- bakery
- bar
- cafe
- establishment
- food
- lodging
- meal_delivery
- meal_takeaway
- night_club
- point_of_interest
- restaurant
- store
(base) mkonteh88@8042388ntehsAir API_Testing % python google_
python: can't open file '/Users/mkonteh88/Desktop/Yippee_Dev/Yippee_Testing/API_Testing/google_': [Errno 2] No such file or directory
(base) mkonteh88@8042388ntehsAir API_Testing % python google_get_tags.py 
Predefined Google Places API Place Types:
- bakery
- bar
- cafe
- restaurant
- meal_delivery
- meal_takeaway
- food
- convenience_store
- grocery_or_supermarket
- liquor_store
- donut_shop

Dynamically Fetched Place Types from API:
- bakery
- bar
- establishment
- food
- lodging
- night_club
- point_of_interest
- restaurant
- store
(base) mkonteh88@8042388ntehsAir API_Testing % 
"""