import os
from dotenv import load_dotenv
import requests
from typing import Dict, List, Optional
import json

# Load environment variables
load_dotenv()

# Get API keys from environment variables
YELP_API_KEY = os.getenv('YELP_API_KEY')
DOCUMENU_API_KEY = os.getenv('DOCUMENU_API_KEY')  # You'll need to get this from documenu.com

class RestaurantFinder:
    def __init__(self):
        self.yelp_key = YELP_API_KEY
        self.documenu_key = DOCUMENU_API_KEY
        self.yelp_base_url = "https://api.yelp.com/v3"
        self.documenu_base_url = "https://api.documenu.com/v2"
        self.yelp_headers = {
            "Authorization": f"Bearer {self.yelp_key}",
            "accept": "application/json"
        }
        self.documenu_headers = {
            "x-api-key": self.documenu_key
        }

    def search_restaurants(self, location: str, term: str = None, limit: int = 5) -> List[Dict]:
        """Search for restaurants in a given location with optional search term."""
        if not self.yelp_key:
            raise ValueError(
                "Yelp API key not found! Create a .env file with: YELP_API_KEY=your_api_key_here"
            )

        endpoint = f"{self.yelp_base_url}/businesses/search"
        params = {
            "location": location,
            "term": term if term else "restaurants",
            "limit": limit,
            "sort_by": "rating"
        }

        try:
            response = requests.get(endpoint, headers=self.yelp_headers, params=params)
            response.raise_for_status()
            return response.json()["businesses"]
        except requests.exceptions.RequestException as e:
            print(f"Error searching restaurants: {e}")
            return []

    def get_business_details(self, business_id: str) -> Optional[Dict]:
        """Get detailed information about a specific business from Yelp."""
        endpoint = f"{self.yelp_base_url}/businesses/{business_id}"
        
        try:
            response = requests.get(endpoint, headers=self.yelp_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting business details: {e}")
            return None

    def get_menu_items(self, restaurant_name: str, address: str, distance: float = 1) -> List[Dict]:
        """Get menu items for a restaurant using Documenu API."""
        if not self.documenu_key:
            print("Documenu API key not found. Menu items will not be available.")
            return []

        # First, get the restaurant's exact location
        endpoint = f"{self.documenu_base_url}/restaurants/search/fields"
        params = {
            "restaurant_name": restaurant_name,
            "address": address,
            "distance": distance,
            "exact": True
        }

        try:
            response = requests.get(
                endpoint,
                headers=self.documenu_headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()

            if not data.get('data'):
                return []

            # Get menu items for the first matching restaurant
            restaurant_id = data['data'][0]['restaurant_id']
            menu_endpoint = f"{self.documenu_base_url}/restaurant/{restaurant_id}/menuitems"
            menu_response = requests.get(menu_endpoint, headers=self.documenu_headers)
            menu_response.raise_for_status()
            
            return menu_response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error getting menu items: {e}")
            return []

def main():
    finder = RestaurantFinder()
    
    # Get location and search term from user
    location = input("Enter location (e.g., New York, NY): ").strip() or "New York, NY"
    search_term = input("Enter a dish or cuisine type (press Enter for all restaurants): ").strip()
    
    print(f"\nSearching for {search_term if search_term else 'top-rated restaurants'} in {location}...")
    
    try:
        # Search for restaurants
        restaurants = finder.search_restaurants(location, search_term)
        
        if not restaurants:
            print("No restaurants found.")
            return

        # Display results with details
        for restaurant in restaurants:
            print("\n" + "="*50)
            print(f" {restaurant['name']}")
            print(f" Rating: {restaurant['rating']} ({restaurant['review_count']} reviews)")
            print(f" Price: {restaurant.get('price', 'Not available')}")
            address = ', '.join(restaurant['location']['display_address'])
            print(f" Address: {address}")
            print(f" Phone: {restaurant.get('phone', 'Not available')}")
            
            # Get additional details
            details = finder.get_business_details(restaurant['id'])
            if details:
                if 'hours' in details and details['hours']:
                    is_open = details['hours'][0].get('is_open_now', False)
                    status = ' Open now' if is_open else ' Closed'
                    print(f" Status: {status}")
                
                if 'categories' in details:
                    categories = [cat['title'] for cat in details['categories']]
                    print("\n Specialties/Categories:")
                    print(", ".join(categories))

            # Try to get menu items
            menu_items = finder.get_menu_items(restaurant['name'], address)
            if menu_items:
                print("\n Menu Items:")
                for item in menu_items[:5]:  # Show up to 5 menu items
                    print(f"- {item['item_name']}: ${item.get('price', 'N/A')}")
                    if item.get('description'):
                        print(f"  {item['description']}")
            
            print(f"\n More info: {restaurant['url']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nMake sure you have:")
        print("1. Set up your Yelp API key in the .env file")
        print("2. Set up your Documenu API key in the .env file (for menu items)")
        print("3. Installed required packages (pip install python-dotenv requests)")
        print("4. Have an active internet connection")

if __name__ == "__main__":
    main()

# Yelp restaurant finder (NONFUNCTIONAL)
# useful for trying APIs to retrieve restaurants