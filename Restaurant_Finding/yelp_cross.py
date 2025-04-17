import requests
import re
from urllib.parse import quote

# API Configuration
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_API_KEY"
YELP_API_KEY = "YOUR_YELP_API_KEY"

def get_google_restaurant(restaurant_name, location):
    """Fetch restaurant details from Google Maps API"""
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

def search_yelp_business(restaurant_name, location):
    """Search for matching restaurant on Yelp"""
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "term": restaurant_name,
        "latitude": location.split(",")[0],
        "longitude": location.split(",")[1],
        "limit": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("businesses", [])[0] if data.get("businesses") else None
    return None

def compare_restaurants(google_data, yelp_data):
    """Compare details between Google and Yelp listings"""
    comparison = {
        "name": (google_data.get("name"), yelp_data.get("name")),
        "address": (google_data.get("formatted_address"), 
                   ", ".join(yelp_data.get("location", {}).get("display_address", []))),
        "rating": (google_data.get("rating"), yelp_data.get("rating")),
        "reviews": (google_data.get("user_ratings_total"), yelp_data.get("review_count")),
        "website": (f"https://www.google.com/maps/place/?q=place_id:{google_data.get('place_id')}",
                   yelp_data.get("url"))
    }
    return comparison

def format_comparison(comparison):
    """Format the comparison results for display"""
    print("\n🔍 Restaurant Comparison Results:")
    print(f"Name: {comparison['name'][0]} (Google) vs {comparison['name'][1]} (Yelp)")
    print(f"\n📍 Address:")
    print(f"- Google: {comparison['address'][0]}")
    print(f"- Yelp: {comparison['address'][1]}")
    print(f"\n⭐ Ratings:")
    print(f"- Google: {comparison['rating'][0]}/5")
    print(f"- Yelp: {comparison['rating'][1]}/5")
    print(f"\n📝 Reviews:")
    print(f"- Google: {comparison['reviews'][0]}")
    print(f"- Yelp: {comparison['reviews'][1]}")
    print(f"\n🌐 Links:")
    print(f"- Google Maps: {comparison['website'][0]}")
    print(f"- Yelp: {comparison['website'][1]}")

if __name__ == "__main__":
    # User input
    restaurant_name = input("Enter restaurant name: ")
    location = input("Enter location (latitude,longitude): ")
    
    # Get data from both platforms
    google_data = get_google_restaurant(restaurant_name, location)
    
    if not google_data:
        print("No results found on Google Maps")
        exit()
    
    yelp_data = search_yelp_business(restaurant_name, location)
    
    if not yelp_data:
        print("No matching Yelp listing found")
        exit()
    
    # Compare and display results
    comparison = compare_restaurants(google_data, yelp_data)
    format_comparison(comparison)


""" Example output:
🔍 Restaurant Comparison Results:
Name: Magnolia Bakery (Google) vs Magnolia Bakery (Yelp)

📍 Address:
- Google: 401 Bleecker St, New York, NY 10014, USA
- Yelp: 401 Bleecker St, New York, NY 10014

⭐ Ratings:
- Google: 4.5/5
- Yelp: 4.0/5

📝 Reviews:
- Google: 12543
- Yelp: 2847

🌐 Links:
- Google Maps: https://www.google.com/maps/place/?q=place_id:ChIJW6...
- Yelp: https://www.yelp.com/biz/magnolia-bakery-new-york

"""