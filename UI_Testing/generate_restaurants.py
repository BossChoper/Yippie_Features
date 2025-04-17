# Functional; good for testing restaurant placement using map data
import folium
import random

def get_sample_restaurants(city_coords, num_restaurants=10):
    """
    Generate sample restaurant data for a given location.
    
    Args:
        city_coords (list): [latitude, longitude] of the city center
        num_restaurants (int): Number of restaurants to generate
    
    Returns:
        list: List of restaurant dictionaries
    """
    restaurant_types = [
        "Pizza Place", "Sushi Restaurant", "Burger Joint", 
        "Cafe", "Steakhouse", "Vegetarian Bistro", 
        "Seafood Restaurant", "Italian Trattoria"
    ]
    
    restaurants = []
    for i in range(num_restaurants):
        # Generate slight variations in coordinates around the city center
        lat_variation = random.uniform(-0.05, 0.05)
        lon_variation = random.uniform(-0.05, 0.05)
        
        restaurant = {
            "name": f"{random.choice(restaurant_types)} {i+1}",
            "coords": [
                city_coords[0] + lat_variation, 
                city_coords[1] + lon_variation
            ],
            "cuisine": random.choice(restaurant_types)
        }
        restaurants.append(restaurant)
    
    return restaurants

def create_restaurant_map(city_name, city_coords):
    """
    Create a map with restaurant markers for a specific city.
    
    Args:
        city_name (str): Name of the city
        city_coords (list): [latitude, longitude] of the city center
    
    Returns:
        folium.Map: Interactive map with restaurant markers
    """
    # Create a map centered on the specified city
    city_map = folium.Map(
        location=city_coords,
        zoom_start=12,
        tiles='CartoDB positron'
    )
    
    # Get sample restaurants
    restaurants = get_sample_restaurants(city_coords)
    
    # Color mapping for different cuisine types
    cuisine_colors = {
        "Pizza Place": "red",
        "Sushi Restaurant": "blue",
        "Burger Joint": "green",
        "Cafe": "purple",
        "Steakhouse": "orange",
        "Vegetarian Bistro": "darkgreen",
        "Seafood Restaurant": "darkblue",
        "Italian Trattoria": "darkred"
    }
    
    # Add restaurant markers
    for restaurant in restaurants:
        # Choose color based on cuisine type, default to gray if not found
        marker_color = cuisine_colors.get(restaurant['cuisine'], 'gray')
        
        # Create a marker with popup information
        folium.Marker(
            location=restaurant['coords'],
            popup=f"<strong>{restaurant['name']}</strong><br>Cuisine: {restaurant['cuisine']}",
            tooltip=restaurant['name'],
            icon=folium.Icon(color=marker_color, icon='utensils')
        ).add_to(city_map)
    
    return city_map

def save_map(map_object, filename='restaurant_map.html'):
    """
    Save the map to an HTML file.
    
    Args:
        map_object (folium.Map): The map to save
        filename (str): Name of the file to save
    """
    map_object.save(filename)
    print(f"Map saved as {filename}")

def main():
    # Example cities with their coordinates
    cities = {
        "New York": [40.7128, -74.0060],
        "San Francisco": [37.7749, -122.4194],
        "Chicago": [41.8781, -87.6298],
        "Los Angeles": [34.0522, -118.2437]
    }
    
    # Let user choose a city
    print("Available Cities:")
    for i, city in enumerate(cities.keys(), 1):
        print(f"{i}. {city}")
    
    choice = int(input("\nEnter the number of the city you want to explore: ")) - 1
    selected_city = list(cities.keys())[choice]
    
    # Create and save the restaurant map
    restaurant_map = create_restaurant_map(
        selected_city, 
        cities[selected_city]
    )
    
    save_map(restaurant_map, f'{selected_city.lower().replace(" ", "_")}_restaurants.html')
    
    print(f"\nRestaurant map for {selected_city} created successfully!")
    print("Open the HTML file in a web browser to explore the restaurants.")

if __name__ == "__main__":
    main()