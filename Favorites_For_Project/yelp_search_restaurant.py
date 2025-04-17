# Functional; searches for rstaurants on yelp in popular cities
# Useful for iterating through retrieved restaurant lists for websites, menus, etc
import os
from dotenv import load_dotenv
import requests
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Get API key from environment variable
YELP_API_KEY = os.getenv('YELP_API_KEY')

class YelpRestaurantFinder:
    def __init__(self):
        self.api_key = YELP_API_KEY
        self.base_url = "https://api.yelp.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }

    def search_restaurants(self, location: str, limit: int = 5) -> List[Dict]:
        """Search for restaurants in a given location."""
        if not self.api_key:
            raise ValueError(
                "Yelp API key not found! Create a .env file with: YELP_API_KEY=your_api_key_here"
            )

        endpoint = f"{self.base_url}/businesses/search"
        params = {
            "location": location,
            "term": "restaurants",
            "limit": limit,
            "sort_by": "rating"
        }

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()["businesses"]
        except requests.exceptions.RequestException as e:
            print(f"Error searching restaurants: {e}")
            return []

    def get_business_details(self, business_id: str) -> Optional[Dict]:
        """Get detailed information about a specific business."""
        endpoint = f"{self.base_url}/businesses/{business_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error getting business details: {e}")
            return None

def main():
    finder = YelpRestaurantFinder()
    
    # Example location
    location = "New York, NY"
    print(f"\nSearching for top-rated restaurants in {location}...")
    
    try:
        # Search for restaurants
        restaurants = finder.search_restaurants(location)
        
        if not restaurants:
            print("No restaurants found.")
            return

        # Display results with details / Good for project
        for restaurant in restaurants:
            print("\n" + "="*50)
            print(f"📍 {restaurant['name']}")
            print(f"📈 Rating: {restaurant['rating']}⭐ ({restaurant['review_count']} reviews)")
            print(f"💰 Price: {restaurant.get('price', 'Not available')}")
            print(f"📍 Address: {', '.join(restaurant['location']['display_address'])}")
            print(f"📞 Phone: {restaurant.get('phone', 'Not available')}")
            
            # Get additional details including menu items if available
            details = finder.get_business_details(restaurant['id'])
            if details:
                if 'hours' in details and details['hours']:
                    is_open = details['hours'][0].get('is_open_now', False)
                    status = '🟢 Open now' if is_open else '🔴 Closed'
                    print(f"🕒 Status: {status}")
                
                # Display some popular menu items or categories
                if 'categories' in details:
                    categories = [cat['title'] for cat in details['categories']]
                    print("\n🍽️ Specialties/Categories:")
                    print(", ".join(categories))
                
            print(f"🌐 More info: {restaurant['url']}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nMake sure you have:")
        print("1. Set up your Yelp API key in the .env file")
        print("2. Installed required packages (pip install python-dotenv requests)")
        print("3. Have an active internet connection")

if __name__ == "__main__":
    main()

# Yelp Restaurnat querying
# NONFUNCTIONAL
# Useful for API requesting