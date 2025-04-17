# Nonfunctional; supposed to search for restaurant menus using google
import requests
import os
import json
import time
import argparse
import urllib.parse
import base64
from datetime import datetime

class RestaurantMenuFinder:
    def __init__(self, google_maps_api_key, google_search_api_key, search_engine_id, output_folder="restaurant_menus"):
        """
        Initialize the Restaurant Menu Finder.
        
        Args:
            google_maps_api_key: API key for Google Maps Platform
            google_search_api_key: API key for Google Custom Search
            search_engine_id: Google Custom Search Engine ID
            output_folder: Folder to save results
        """
        self.maps_api_key = google_maps_api_key
        self.search_api_key = google_search_api_key
        self.search_engine_id = search_engine_id
        self.output_folder = output_folder
        
        # Create output directories
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Create a subfolder for the current run with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_run_folder = os.path.join(output_folder, f"search_{timestamp}")
        os.makedirs(self.current_run_folder)
        os.makedirs(os.path.join(self.current_run_folder, "images"))
    
    def find_restaurants(self, location, radius=1000, keyword="restaurant", max_results=5):
        """
        Find restaurants in a specific location using Google Places API.
        
        Args:
            location: Location string (e.g., "New York, NY")
            radius: Search radius in meters
            keyword: Type of establishment to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of restaurant details
        """
        # First, geocode the location to get coordinates
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(location)}&key={self.maps_api_key}"
        
        try:
            geocode_response = requests.get(geocode_url)
            geocode_data = geocode_response.json()
            
            if geocode_data['status'] != 'OK':
                print(f"Geocoding error: {geocode_data['status']}")
                return []
            
            # Get the coordinates
            lat = geocode_data['results'][0]['geometry']['location']['lat']
            lng = geocode_data['results'][0]['geometry']['location']['lng']
            
            # Now search for restaurants near these coordinates
            places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&keyword={keyword}&type=restaurant&key={self.maps_api_key}"
            
            places_response = requests.get(places_url)
            places_data = places_response.json()
            
            if places_data['status'] != 'OK':
                print(f"Places API error: {places_data['status']}")
                return []
            
            # Process the results
            restaurants = []
            for place in places_data['results'][:max_results]:
                restaurant = {
                    'name': place['name'],
                    'address': place.get('vicinity', 'Address not available'),
                    'rating': place.get('rating', 'No rating'),
                    'place_id': place['place_id'],
                    'location': {
                        'lat': place['geometry']['location']['lat'],
                        'lng': place['geometry']['location']['lng']
                    }
                }
                
                # Get additional details using the Place Details API
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place['place_id']}&fields=name,formatted_address,formatted_phone_number,website,price_level,url&key={self.maps_api_key}"
                details_response = requests.get(details_url)
                details_data = details_response.json()
                
                if details_data['status'] == 'OK':
                    result = details_data['result']
                    restaurant['full_address'] = result.get('formatted_address', restaurant['address'])
                    restaurant['phone'] = result.get('formatted_phone_number', 'Phone not available')
                    restaurant['website'] = result.get('website', 'Website not available')
                    restaurant['price_level'] = result.get('price_level', 'Price level not available')
                    restaurant['maps_url'] = result.get('url', 'Maps URL not available')
                
                restaurants.append(restaurant)
                
                # Add a small delay to avoid hitting rate limits
                time.sleep(0.2)
            
            return restaurants
            
        except Exception as e:
            print(f"Error finding restaurants: {e}")
            return []
    
    def search_menu_images(self, restaurant_name, location=None, max_images=5):
        """
        Search for menu images related to a specific restaurant using Google Custom Search API.
        
        Args:
            restaurant_name: Name of the restaurant
            location: Optional location to add to the search query
            max_images: Maximum number of images to return
            
        Returns:
            List of image URLs and metadata
        """
        # Construct the search query
        search_query = f"{restaurant_name} menu"
        if location:
            search_query += f" {location}"
        
        # Build the search URL
        search_url = f"https://www.googleapis.com/customsearch/v1?key={self.search_api_key}&cx={self.search_engine_id}&q={urllib.parse.quote(search_query)}&searchType=image&num={max_images}&safe=active"
        
        try:
            search_response = requests.get(search_url)
            search_data = search_response.json()
            
            if 'items' not in search_data:
                print(f"No images found for {restaurant_name}")
                return []
            
            # Process the search results
            images = []
            for item in search_data['items']:
                image = {
                    'title': item.get('title', 'No title'),
                    'url': item.get('link', ''),
                    'thumbnail': item.get('image', {}).get('thumbnailLink', ''),
                    'context_url': item.get('image', {}).get('contextLink', ''),
                    'width': item.get('image', {}).get('width', 0),
                    'height': item.get('image', {}).get('height', 0),
                    'size': item.get('image', {}).get('byteSize', 0),
                    'type': item.get('mime', '')
                }
                images.append(image)
            
            return images
            
        except Exception as e:
            print(f"Error searching for menu images: {e}")
            return []
    
    def download_image(self, image_url, file_path):
        """
        Download an image from a URL and save it to a file.
        
        Args:
            image_url: URL of the image
            file_path: Path to save the image to
            
        Returns:
            Success status (bool)
        """
        try:
            response = requests.get(image_url, stream=True, timeout=10)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return True
            else:
                print(f"Failed to download image. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False
    
    def process_restaurant(self, restaurant, location=None, max_images=5):
        """
        Process a restaurant by finding menu images and saving them.
        
        Args:
            restaurant: Restaurant details
            location: Optional location to add to the search query
            max_images: Maximum number of images to download
            
        Returns:
            Restaurant object with added menu image information
        """
        print(f"\nProcessing restaurant: {restaurant['name']}")
        
        # Search for menu images
        menu_images = self.search_menu_images(restaurant['name'], location, max_images)
        
        if not menu_images:
            print(f"No menu images found for {restaurant['name']}")
            restaurant['menu_images'] = []
            return restaurant
        
        # Download the images
        downloaded_images = []
        for i, image in enumerate(menu_images):
            if not image['url']:
                continue
                
            # Create a filename based on restaurant name and image index
            safe_name = "".join(c if c.isalnum() else "_" for c in restaurant['name'])
            filename = f"{safe_name}_menu_{i+1}.{image['url'].split('.')[-1]}"
            file_path = os.path.join(self.current_run_folder, "images", filename)
            
            print(f"Downloading image {i+1}/{len(menu_images)} for {restaurant['name']}")
            success = self.download_image(image['url'], file_path)
            
            if success:
                image['local_path'] = file_path
                downloaded_images.append(image)
                
            # Add a small delay
            time.sleep(0.5)
        
        restaurant['menu_images'] = downloaded_images
        return restaurant
    
    def save_results(self, restaurants):
        """
        Save the search results to a JSON file.
        
        Args:
            restaurants: List of restaurant objects with menu images
        """
        output_path = os.path.join(self.current_run_folder, "results.json")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2)
        
        print(f"\nResults saved to {output_path}")
        
        # Also create a simple HTML report
        html_report = self.create_html_report(restaurants)
        html_path = os.path.join(self.current_run_folder, "report.html")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"HTML report saved to {html_path}")
    
    def create_html_report(self, restaurants):
        """
        Create a simple HTML report of the search results.
        
        Args:
            restaurants: List of restaurant objects with menu images
            
        Returns:
            HTML string
        """
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Restaurant Menu Search Results</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 1200px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .restaurant { margin-bottom: 40px; border-bottom: 1px solid #ccc; padding-bottom: 20px; }
                .restaurant-header { display: flex; justify-content: space-between; }
                .restaurant-info { margin-bottom: 20px; }
                .restaurant-info p { margin: 5px 0; }
                .menu-images { display: flex; flex-wrap: wrap; gap: 10px; }
                .menu-image { margin-bottom: 15px; }
                .menu-image img { max-width: 300px; max-height: 300px; border: 1px solid #ddd; }
                .no-images { color: #999; font-style: italic; }
            </style>
        </head>
        <body>
            <h1>Restaurant Menu Search Results</h1>
            <p>Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        """
        
        for restaurant in restaurants:
            html += f"""
            <div class="restaurant">
                <div class="restaurant-header">
                    <h2>{restaurant['name']}</h2>
                    <p>Rating: {restaurant['rating']}</p>
                </div>
                <div class="restaurant-info">
                    <p><strong>Address:</strong> {restaurant.get('full_address', restaurant['address'])}</p>
                    <p><strong>Phone:</strong> {restaurant.get('phone', 'N/A')}</p>
                    <p><strong>Website:</strong> <a href="{restaurant.get('website', '#')}" target="_blank">{restaurant.get('website', 'N/A')}</a></p>
                    <p><strong>Google Maps:</strong> <a href="{restaurant.get('maps_url', '#')}" target="_blank">View on Maps</a></p>
                </div>
                <h3>Menu Images</h3>
            """
            
            if restaurant['menu_images']:
                html += '<div class="menu-images">'
                for image in restaurant['menu_images']:
                    # Create a relative path for the image
                    rel_path = os.path.relpath(image['local_path'], self.current_run_folder)
                    html += f"""
                    <div class="menu-image">
                        <a href="{rel_path}" target="_blank">
                            <img src="{rel_path}" alt="{image['title']}">
                        </a>
                        <p>{image['title']}</p>
                    </div>
                    """
                html += '</div>'
            else:
                html += '<p class="no-images">No menu images found for this restaurant.</p>'
            
            html += '</div>'
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def run(self, location, radius=1000, keyword="restaurant", max_restaurants=5, max_images_per_restaurant=5):
        """
        Run the complete search process.
        
        Args:
            location: Location string (e.g., "New York, NY")
            radius: Search radius in meters
            keyword: Type of establishment to search for
            max_restaurants: Maximum number of restaurants to search for
            max_images_per_restaurant: Maximum number of menu images to find per restaurant
        """
        print(f"Searching for restaurants in {location}...")
        restaurants = self.find_restaurants(location, radius, keyword, max_restaurants)
        
        if not restaurants:
            print("No restaurants found.")
            return
        
        print(f"Found {len(restaurants)} restaurants.")
        
        processed_restaurants = []
        for restaurant in restaurants:
            processed = self.process_restaurant(restaurant, location, max_images_per_restaurant)
            processed_restaurants.append(processed)
        
        self.save_results(processed_restaurants)
        print("\nSearch complete!")

def main():
    """
    Main function to run the restaurant menu finder.
    """
    parser = argparse.ArgumentParser(description='Find restaurant menus using Google APIs')
    parser.add_argument('--location', required=True, help='Location to search for restaurants (e.g., "New York, NY")')
    parser.add_argument('--radius', type=int, default=1000, help='Search radius in meters (default: 1000)')
    parser.add_argument('--max-restaurants', type=int, default=5, help='Maximum number of restaurants to search (default: 5)')
    parser.add_argument('--max-images', type=int, default=5, help='Maximum number of menu images per restaurant (default: 5)')
    parser.add_argument('--output', default='restaurant_menus', help='Output folder for results (default: restaurant_menus)')

    args = parser.parse_args()

    # Load API keys from environment variables
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    google_search_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
    search_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

    if not all([google_maps_api_key, google_search_api_key, search_engine_id]):
        print("Error: Missing required API keys in environment variables.")
        print("Please set GOOGLE_MAPS_API_KEY, GOOGLE_SEARCH_API_KEY, and GOOGLE_SEARCH_ENGINE_ID")
        return

    # Initialize the restaurant menu finder
    finder = RestaurantMenuFinder(
        google_maps_api_key=google_maps_api_key,
        google_search_api_key=google_search_api_key,
        search_engine_id=search_engine_id,
        output_folder=args.output
    )

    # Find restaurants in the specified location
    print(f"\nSearching for restaurants in {args.location}...")
    restaurants = finder.find_restaurants(
        location=args.location,
        radius=args.radius,
        max_results=args.max_restaurants
    )

    if not restaurants:
        print("No restaurants found.")
        return

    # Process each restaurant
    for restaurant in restaurants:
        processed_restaurant = finder.process_restaurant(
            restaurant,
            location=args.location,
            max_images=args.max_images
        )

        # Save restaurant details to JSON
        restaurant_file = os.path.join(
            finder.current_run_folder,
            f"{base64.urlsafe_b64encode(restaurant['name'].encode()).decode()}.json"
        )
        with open(restaurant_file, 'w', encoding='utf-8') as f:
            json.dump(processed_restaurant, f, indent=2)

    print(f"\nResults have been saved to: {finder.current_run_folder}")

if __name__ == '__main__':
    main()

# Useful for finding restaurant details