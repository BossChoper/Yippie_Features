# Probably nonfunctional; can't scrape from yelp
import requests
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class YelpMenuScraper:
    def __init__(self):
        self.api_key = os.getenv("YELP_API_KEY")
        if not self.api_key:
            raise ValueError("YELP_API_KEY environment variable not set")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
        self.base_url = "https://api.yelp.com/v3"
    
    def search_restaurants(self, location, term=None, limit=5):
        """Search for restaurants in a specific location"""
        endpoint = f"{self.base_url}/businesses/search"
        params = {
            "location": location,
            "term": term if term else "restaurants",
            "limit": limit,
            "categories": "restaurants"
        }
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Error searching restaurants: {response.status_code}")
            print(response.text)
            return []
        
        return response.json().get("businesses", [])
    
    def get_business_details(self, business_id):
        """Get detailed information about a business"""
        endpoint = f"{self.base_url}/businesses/{business_id}"
        
        response = requests.get(endpoint, headers=self.headers)
        if response.status_code != 200:
            print(f"Error getting business details: {response.status_code}")
            print(response.text)
            return None
        
        return response.json()

    def get_reviews(self, business_id, limit=5):
        """Get reviews for a business which might contain menu item mentions"""
        endpoint = f"{self.base_url}/businesses/{business_id}/reviews"
        params = {"limit": limit}
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            print(f"Error getting reviews: {response.status_code}")
            print(response.text)
            return []
        
        return response.json().get("reviews", [])
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
    
    def get_menu_data_for_location(self, location, term=None, limit=5):
        """Get menu-related data for restaurants in a location"""
        restaurants = self.search_restaurants(location, term, limit)
        results = []
        
        for i, restaurant in enumerate(restaurants):
            print(f"Processing {i+1}/{len(restaurants)}: {restaurant.get('name')}")
            
            restaurant_data = {
                "id": restaurant.get("id"),
                "name": restaurant.get("name"),
                "url": restaurant.get("url"),
                "categories": restaurant.get("categories"),
                "details": None,
                "reviews": []
            }
            
            # Get detailed business information
            business_id = restaurant.get("id")
            if business_id:
                details = self.get_business_details(business_id)
                restaurant_data["details"] = details
                
                # Get reviews which might mention menu items
                reviews = self.get_reviews(business_id)
                restaurant_data["reviews"] = reviews
            
            results.append(restaurant_data)
            # Respect rate limits
            time.sleep(0.5)
        
        return results

def extract_potential_menu_items(data):
    """
    Analyze the data to extract potential menu items from reviews and other metadata
    This is a simple implementation that could be enhanced with NLP techniques
    """
    all_restaurants_menu_items = {}
    
    for restaurant in data:
        restaurant_name = restaurant.get("name")
        menu_items = set()
        
        # Check categories for food types
        for category in restaurant.get("categories", []):
            if category and "title" in category:
                menu_items.add(category["title"])
        
        # Extract potential menu items from reviews using simple heuristics
        for review in restaurant.get("reviews", []):
            review_text = review.get("text", "").lower()
            
            # Look for phrases that might indicate menu items
            indicators = ["tried the", "ordered the", "had the", "recommend the"]
            for indicator in indicators:
                if indicator in review_text:
                    # Extract what might be a menu item after the indicator
                    parts = review_text.split(indicator)
                    for part in parts[1:]:
                        # Take the first 50 characters after the indicator
                        # as a potential menu item reference
                        potential_item = part[:50].strip()
                        if potential_item and len(potential_item) > 3:
                            # Cut off at punctuation
                            for punct in ['.', ',', '!', '?', ';']:
                                if punct in potential_item:
                                    potential_item = potential_item.split(punct)[0].strip()
                            menu_items.add(potential_item)
        
        all_restaurants_menu_items[restaurant_name] = list(menu_items)
    
    return all_restaurants_menu_items

def main():
    # Example usage
    try:
        scraper = YelpMenuScraper()
        
        # Choose a location to test
        location = input("Enter a location to search for restaurants (e.g., 'San Francisco, CA'): ")
        term = input("Enter a cuisine or restaurant type (optional, press Enter to skip): ")
        if not term:
            term = None
        
        limit = input("How many restaurants to fetch? (default: 5): ")
        limit = int(limit) if limit else 5
        
        print(f"\nFetching data for {limit} restaurants in {location}...")
        restaurant_data = scraper.get_menu_data_for_location(location, term, limit)
        
        # Save raw data
        scraper.save_to_json(restaurant_data, "restaurant_data_raw.json")
        
        # Extract potential menu items
        print("\nAnalyzing data to extract potential menu items...")
        menu_items = extract_potential_menu_items(restaurant_data)
        scraper.save_to_json(menu_items, "extracted_menu_items.json")
        
        print("\nData collection complete! Check the JSON files for results.")
        print("\nNote: This is a basic implementation to test the API.")
        print("For full menu data, you may need to explore additional approaches.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()

""" Example output: 

Enter a location to search for restaurants (e.g., 'San Francisco, CA'): San Francisco, CA
Enter a cuisine or restaurant type (optional, press Enter to skip): Italian
How many restaurants to fetch? (default: 5): 5

Fetching data for 5 restaurants in San Francisco...
Processing 1/5: Bottega
"""

# Yelp Restaurant finder based on cuisines