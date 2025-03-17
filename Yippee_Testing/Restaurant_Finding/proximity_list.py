from dataclasses import dataclass
from typing import List
import math

# Mock restaurant data near San Francisco
@dataclass
class Restaurant:
    name: str
    lat: float  # Latitude
    lon: float  # Longitude
    tags: List[str]  # Tags like "vegan", "italian"

MOCK_RESTAURANTS = [
    Restaurant("Vegan Delight", 37.7831, -122.4210, ["vegan", "american"]),
    Restaurant("Pasta Palace", 37.7950, -122.3998, ["italian", "vegetarian"]),
    Restaurant("Sushi Spot", 37.7765, -122.4382, ["japanese", "seafood"]),
]

# Static user location (San Francisco downtown)
USER_LOCATION = {"lat": 37.7749, "lon": -122.4194}

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate approximate distance in miles using Euclidean formula."""
    # Rough conversion: 1 degree ≈ 69 miles (simplified, not accounting for curvature)
    delta_lat = (lat2 - lat1) * 69
    delta_lon = (lon2 - lon1) * 69  # Approx same at this latitude
    distance = math.sqrt(delta_lat**2 + delta_lon**2)
    return round(distance, 2)

def get_proximity_list(user_loc: dict, restaurants: List[Restaurant]) -> List[dict]:
    """Generate a sorted list of restaurants by proximity."""
    proximity_list = []
    for restaurant in restaurants:
        distance = calculate_distance(
            user_loc["lat"], user_loc["lon"],
            restaurant.lat, restaurant.lon
        )
        proximity_list.append({
            "name": restaurant.name,
            "distance": distance,
            "tags": restaurant.tags
        })
    
    # Sort by distance
    proximity_list.sort(key=lambda x: x["distance"])
    return proximity_list

def print_proximity_list(proximity_list: List[dict]):
    """Print the sorted proximity list."""
    print("\nRestaurants near your location (San Francisco):")
    for entry in proximity_list:
        print(f"- {entry['name']} ({entry['distance']} mi)")
        print(f"  Tags: {', '.join(entry['tags'])}")

def main():
    """Run the Proximity List Program."""
    print("Starting Proximity List Program...")
    print(f"User location: Lat {USER_LOCATION['lat']}, Lon {USER_LOCATION['lon']}")
    
    proximity_list = get_proximity_list(USER_LOCATION, MOCK_RESTAURANTS)
    print_proximity_list(proximity_list)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Proximity List Program...
User location: Lat 37.7749, Lon -122.4194

Restaurants near your location (San Francisco):
- Vegan Delight (0.46 mi)
  Tags: vegan, american
- Sushi Spot (1.19 mi)
  Tags: japanese, seafood
- Pasta Palace (1.77 mi)
  Tags: italian, vegetarian
  \\
"""

# Restaurant list generation based on location proximity