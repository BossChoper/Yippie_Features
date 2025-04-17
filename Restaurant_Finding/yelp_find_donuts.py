import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your Yelp API key
API_KEY = os.getenv('YELP_API_KEY')

def find_donut_shops(location="New York"):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "term": "donuts",
        "location": location,
        "categories": "donuts",
        "sort_by": "rating",
        "limit": 20  # Max results per request
    }

    response = requests.get(
        "https://api.yelp.com/v3/businesses/search",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        results = response.json()
        shops = []
        for business in results.get("businesses", []):
            shop_info = {
                "name": business["name"],
                "rating": business["rating"],
                "address": ", ".join(business["location"]["display_address"]),
                "phone": business.get("phone", "N/A"),
                "reviews": business["review_count"]
            }
            shops.append(shop_info)
        return shops
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# Example usage
donut_shops = find_donut_shops(location="San Francisco")
for idx, shop in enumerate(donut_shops, 1):
    print(f"{idx}. {shop['name']} (⭐ {shop['rating']})")
    print(f"   📍 {shop['address']}")
    print(f"   📞 {shop['phone']}")
    print(f"   📊 {shop['reviews']} reviews\n")
