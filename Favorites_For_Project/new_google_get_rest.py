# Updated version is more effective
# Searches for restaurants in a given city
# Functional
import requests
import csv
import time
from collections import defaultdict
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
FIELDS = "name,formatted_address,place_id,types,website,formatted_phone_number,price_level,rating,user_ratings_total"

def get_restaurants(location, radius=5000, output_file="restaurants.csv"):
    # Geocoding to get coordinates
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    geocode_resp = requests.get(geocode_url).json()
    lat = geocode_resp['results'][0]['geometry']['location']['lat']
    lng = geocode_resp['results'][0]['geometry']['location']['lng']
    
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    search_criteria = [
        {'type': 'bakery', 'keyword': ''},
        {'type': 'cafe', 'keyword': ''},
        {'type': 'restaurant', 'keyword': 'vegan'},
        {'type': 'restaurant', 'keyword': 'health food'},
        {'type': 'meal_takeaway', 'keyword': ''},
        {'type': 'food', 'keyword': 'donut'}
    ]
    
    restaurants = []
    seen_ids = set()
    chain_counts = defaultdict(int)

    for criterion in search_criteria:
        params = {
            'location': f"{lat},{lng}",
            'radius': radius,
            'type': criterion['type'],
            'key': API_KEY
        }
        if criterion['keyword']:
            params['keyword'] = criterion['keyword']

        while True:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            for place in data.get('results', []):
                if place['place_id'] in seen_ids:
                    continue
                
                seen_ids.add(place['place_id'])
                
                # Get detailed information
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place['place_id']}&fields={FIELDS}&key={API_KEY}"
                details = requests.get(details_url).json().get('result', {})
                
                # Track chains by name
                name = place.get('name', '')
                chain_counts[name] += 1
                is_chain = chain_counts[name] > 1
                
                restaurant = {
                    'name': name,
                    'address': details.get('formatted_address', ''),
                    'place_id': place['place_id'],
                    'types': ", ".join(details.get('types', [])),
                    'phone': details.get('formatted_phone_number', ''),
                    'website': details.get('website', ''),
                    'price_level': details.get('price_level', ''),
                    'rating': details.get('rating', ''),
                    'reviews_count': details.get('user_ratings_total', ''),
                    'is_chain': is_chain,
                    'category': criterion['type']  # Add category for filtering
                }
                restaurants.append(restaurant)
            
            if 'next_page_token' not in data:
                break
                
            params['pagetoken'] = data['next_page_token']
            time.sleep(2)

    # Save to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=restaurants[0].keys())
        writer.writeheader()
        writer.writerows(restaurants)

# Example usage
get_restaurants("Washington D.C.", radius=10000)
