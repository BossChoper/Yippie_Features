import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def find_nearby_restaurants(latitude, longitude, radius_meters=3218):  # 2 miles default
    if not API_KEY:
        print("Error: Google Maps API key not found!")
        print("Please create a .env file with your API key like this:")
        print("GOOGLE_MAPS_API_KEY=your_api_key_here")
        return
    
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=API_KEY)
    
    try:
        # Get address for the coordinates
        reverse_geocode = gmaps.reverse_geocode((latitude, longitude))
        location_name = reverse_geocode[0]['formatted_address'] if reverse_geocode else "Unknown Location"
        print(f"\nSearching for restaurants near: {location_name}")
        
        # Search for restaurants near the specified location
        places_result = gmaps.places_nearby(
            location=(latitude, longitude),
            radius=radius_meters,
            type='restaurant'
        )
        
        # Process and print results
        if places_result.get('results'):
            print(f"\nFound restaurants within {radius_meters/1609:.1f} miles:")
            print("-" * 50)
            
            # Sort results by rating (highest first)
            sorted_results = sorted(
                places_result['results'],
                key=lambda x: (x.get('rating', 0), x.get('user_ratings_total', 0)),
                reverse=True
            )
            
            for place in sorted_results[:15]:  # Show top 15 results
                name = place['name']
                address = place.get('vicinity', 'Address not available')
                rating = place.get('rating', 'No rating')
                total_ratings = place.get('user_ratings_total', 0)
                price_level = '💰' * place.get('price_level', 0) or 'Price not available'
                open_now = place.get('opening_hours', {}).get('open_now')
                status = '🟢 Open now' if open_now else '🔴 Closed' if open_now is not None else '❓ Status unknown'
                
                print(f"\nName: {name}")
                print(f"Address: {address}")
                print(f"Rating: {rating}⭐ ({total_ratings} reviews)")
                print(f"Price Level: {price_level}")
                print(f"Status: {status}")
                
                # Get additional details for each place
                try:
                    place_details = gmaps.place(place['place_id'], fields=['formatted_phone_number', 'website'])
                    if 'result' in place_details:
                        if 'formatted_phone_number' in place_details['result']:
                            print(f"Phone: {place_details['result']['formatted_phone_number']}")
                        if 'website' in place_details['result']:
                            print(f"Website: {place_details['result']['website']}")
                except Exception:
                    pass  # Skip if we can't get additional details
                
            print("\n💡 Tip: Results are sorted by rating and number of reviews")
        else:
            print("No restaurants found in the specified area.")
            print("Try increasing the search radius or checking a different location.")
            
    except Exception as e:
        print(f"An error occurred while searching for restaurants: {e}")
        if "API key" in str(e):
            print("\nPlease make sure your Google Maps API key is valid and has the required permissions.")

def main():
    # Default to Washington, DC coordinates
    latitude = 38.8977
    longitude = -77.0365
    
    print("Using Washington, DC as the search location")
    
    try:
        find_nearby_restaurants(latitude, longitude)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you have set your Google Maps API key in the .env file!")

if __name__ == "__main__":
    main()

""" Example output:
Phone: (202) 637-1222
Website: http://www.rasikarestaurant.com/pennquarter/

Name: Sequoia DC
Address: 3000 K Street Northwest, Washington
Rating: 4.3⭐ (2770 reviews)
Price Level: 💰💰💰
Status: 🔴 Closed
Phone: (202) 944-4200
Website: https://sequoiadc.com/

Name: The Georgetown Inn
Address: 1310 Wisconsin Avenue Northwest, Washington
Rating: 4.3⭐ (533 reviews)
Price Level: Price not available
Status: 🟢 Open now
Phone: (202) 333-8900
Website: http://www.georgetowninn.com/

💡 Tip: Results are sorted by rating and number of reviews
"""