import requests
import folium
import json
from folium.plugins import MarkerCluster
import os
from dotenv import load_dotenv

load_dotenv()

# Replace with your Google API key
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def fetch_restaurants(location="40.7128,-74.0060", radius=5000, place_type="restaurant"):
    """
    Fetch restaurants from Google Places API.
    Args:
        location (str): Latitude,longitude (e.g., "40.7128,-74.0060" for NYC).
        radius (int): Search radius in meters.
        place_type (str): Type of place (e.g., "restaurant").
    Returns:
        list: List of restaurant details (name, address, lat, lng, types).
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": radius,
        "type": place_type,
        "key": API_KEY
    }

    restaurants = []

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])

        for place in results:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "No address available")
            lat = place.get("geometry", {}).get("location", {}).get("lat")
            lng = place.get("geometry", {}).get("location", {}).get("lng")
            types = place.get("types", [])

            if lat and lng:
                restaurants.append({
                    "name": name,
                    "address": address,
                    "lat": lat,
                    "lng": lng,
                    "types": types
                })

        return restaurants

    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

def create_restaurant_map(restaurants, center_location=[40.7128, -74.0060]):
    """
    Create a Folium map with restaurant markers.
    Args:
        restaurants (list): List of restaurant details.
        center_location (list): [lat, lng] for map center.
    Returns:
        folium.Map: Interactive map object.
    """
    # Initialize Folium map
    folium_map = folium.Map(
        location=center_location,
        zoom_start=12,
        tiles="OpenStreetMap"
    )

    # Add MarkerCluster for better visualization of many markers
    marker_cluster = MarkerCluster().add_to(folium_map)

    # Add markers for each restaurant
    for restaurant in restaurants:
        name = restaurant["name"]
        address = restaurant["address"]
        lat = restaurant["lat"]
        lng = restaurant["lng"]
        types = ", ".join(restaurant["types"])

        # Create popup content
        popup_content = f"""
        <b>{name}</b><br>
        Address: {address}<br>
        Types: {types}
        """

        # Add marker to the map
        folium.Marker(
            location=[lat, lng],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color="red", icon="utensils", prefix="fa")
        ).add_to(marker_cluster)

    return folium_map

def main():
    # Define search parameters (default: New York City, 5km radius)
    location = "40.7128,-74.0060"  # NYC coordinates
    radius = 5000  # 5km
    center_location = [40.7128, -74.0060]

    if API_KEY == 'YOUR_API_KEY':
        print("Error: Please replace 'YOUR_API_KEY' with a valid Google API key.")
        return

    # Fetch restaurants
    print("Fetching restaurants from Google Places API...")
    restaurants = fetch_restaurants(location=location, radius=radius)

    if not restaurants:
        print("No restaurants found or an error occurred.")
        return

    print(f"Found {len(restaurants)} restaurants.")

    # Create and save the map
    folium_map = create_restaurant_map(restaurants, center_location)
    output_file = "restaurants_map.html"
    folium_map.save(output_file)
    print(f"Map saved as {output_file}. Open it in a web browser to view.")

if __name__ == "__main__":
    main()