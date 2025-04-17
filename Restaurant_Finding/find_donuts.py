# Functional
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your Google API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key=API_KEY)

def get_donut_restaurants(location="New York", radius=5000):
    # Search for restaurants that serve donuts
    places_result = gmaps.places(
        query="restaurants serving donuts",
        location=location,
        radius=radius,
        type="restaurant"
    )

    # Extract relevant details
    restaurants = []
    for place in places_result['results']:
        details = {
            'name': place['name'],
            'address': place.get('vicinity', 'N/A'),
            'rating': place.get('rating', 'N/A'),
            'price_level': place.get('price_level', 'N/A')
        }
        restaurants.append(details)
    
    return restaurants

# Example usage
donut_restaurants = get_donut_restaurants(location="New York")
for idx, restaurant in enumerate(donut_restaurants, 1):
    print(f"{idx}. {restaurant['name']}")
    print(f"   Address: {restaurant['address']}")
    print(f"   Rating: {restaurant['rating']}")
    print(f"   Price Level: {restaurant['price_level']}\n")

""" Example output: Wrong location though
python find_donuts.py 
1. Good Company Doughnuts & Cafe - National Landing
   Address: N/A
   Rating: 4.4
   Price Level: 2

2. Astro Doughnuts & Fried Chicken
   Address: N/A
   Rating: 4.3
   Price Level: 2

3. Good Company Doughnuts & Cafe - Penn Quarter
   Address: N/A
   Rating: 4.7
   Price Level: 2

4. Good Company Doughnuts & Cafe - Ballston
   Address: N/A
   Rating: 4.5
   Price Level: 2

5. Good Company Doughnuts & Cafe - Southwest
   Address: N/A
   Rating: 4.5
   Price Level: 1

6. Blondie's Doughnuts
   Address: N/A
   Rating: 4.7
   Price Level: 1

7. Laurel Tavern Donuts
   Address: N/A
   Rating: 4.5
   Price Level: 1

8. Donut Shack
   Address: N/A
   Rating: 4.4
   Price Level: 1

9. Coffee Bar
   Address: N/A
   Rating: 4.5
   Price Level: N/A

10. Milk & Honey Southern Inspired Kitchen
   Address: N/A
   Rating: 4.3
   Price Level: 2

11. Big Bear Cafe
   Address: N/A
   Rating: 4.3
   Price Level: 2

12. Love, Makoto
   Address: N/A
   Rating: 4.8
   Price Level: 2

13. Cinnaholic
   Address: N/A
   Rating: 4.2
   Price Level: 2

14. Founding Farmers & Distillers
   Address: N/A
   Rating: 4.3
   Price Level: 2

15. Sandy Pony Donuts
   Address: N/A
   Rating: 4.9
   Price Level: 1

16. Shipley Do-Nuts
   Address: N/A
   Rating: 4.2
   Price Level: 1

17. Astro Doughnuts & Fried Chicken
   Address: N/A
   Rating: 3.8
   Price Level: N/A

18. PJ's Coffee
   Address: N/A
   Rating: 4.7
   Price Level: 1

19. Ruthie's All-Day
   Address: N/A
   Rating: 4.6
   Price Level: 2

20. Bagels ‘n Grinds
   Address: N/A
   Rating: 4.4
   Price Level: 1
   """