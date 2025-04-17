# Functional
import folium
import random

def get_sample_restaurants(city_coords, num_restaurants=10):
    """
    Generate sample restaurant data for a given location.

    Args:
        city_coords (list): [latitude, longitude] of the city center
        num_restaurants (int): Number of restaurants to generate

    Returns:
        list: List of restaruant dictionaries
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
        lon_Variation = random.uniform(-0.05, 0.05)

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