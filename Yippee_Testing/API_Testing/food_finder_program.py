import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import time
from memory_profiler import profile

# Load Yelp API key from .env
load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")
YELP_BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": f"Bearer {YELP_API_KEY}"}

# Mock data for sample dishes (to supplement Yelp data)
MOCK_DISHES = {
    "burgers": "Classic Cheeseburger",
    "mexican": "Street Tacos",
    "japanese": "Sushi Roll",
    "italian": "Margherita Pizza",
    "default": "House Special"
}

@profile
def fetch_food_data(item_name: str, location: str = "San Francisco, CA", limit: int = 3) -> list:
    """Fetch restaurant data from Yelp API for a given food item."""
    params = {
        "term": item_name,
        "location": location,
        "categories": "restaurants",
        "limit": limit  # Keep small for speed
    }
    
    try:
        response = requests.get(YELP_BASE_URL, headers=HEADERS, params=params, timeout=5)
        if response.status_code != 200:
            print(f"Failed to fetch data: Status {response.status_code}")
            return []
        
        data = response.json().get("businesses", [])
        results = []
        for biz in data:
            cuisine = biz["categories"][0]["alias"] if biz["categories"] else "default"
            results.append({
                "name": biz["name"],
                "cuisine": cuisine,
                "dish": MOCK_DISHES.get(cuisine, MOCK_DISHES["default"]),
                "address": ", ".join(biz["location"]["display_address"])
            })
        return results
    except Exception as e:
        print(f"Error fetching Yelp data: {e}")
        return []

def print_food_finder_results(item_name: str, results: list):
    """Print the food finder results to the console."""
    print(f"\nFood Finder Results for '{item_name}':")
    if not results:
        print("  No results found.")
    else:
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['name']}")
            print(f"     Cuisine: {result['cuisine'].capitalize()}")
            print(f"     Sample Dish: {result['dish']}")
            print(f"     Address: {result['address']}")

def save_food_finder_results(item_name: str, results: list, filename: str = "food_finder_results.txt"):
    """Save the food finder results to a text file."""
    try:
        with open(filename, "w") as file:
            file.write(f"Food Finder Results for '{item_name}'\n")
            file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            if not results:
                file.write("  No results found.\n")
            else:
                for i, result in enumerate(results, 1):
                    file.write(f"{i}. {result['name']}\n")
                    file.write(f"  Cuisine: {result['cuisine'].capitalize()}\n")
                    file.write(f"  Sample Dish: {result['dish']}\n")
                    file.write(f"  Address: {result['address']}\n\n")
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")

def measure_time(func, *args, name: str) -> float:
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n{name} Time: {duration:.4f} seconds")
    return result, duration

def main():
    """Run the Food Finder Program with memory and time checking."""
    print("Starting Food Finder Program...")
    item_name = "Burger"  # Could be interactive with input()
    
    # Fetch data with time measurement
    results, fetch_time = measure_time(fetch_food_data, item_name, "San Francisco, CA", 3, name="Fetch Data")
    
    # Print and save results
    print_food_finder_results(item_name, results)
    save_food_finder_results(item_name, results)

if __name__ == "__main__":
    main()

"""
Starting Food Finder Program...
Filename: /Users/mkonteh88/Documents/Yippee_Testing/food_finder_program.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    23     58.0 MiB     58.0 MiB           1   @profile
    24                                         def fetch_food_data(item_name: str, location: str = "San Francisco, CA", limit: int = 3) -> list:
    25                                             """Fetch restaurant data from Yelp API for a given food item."""
    26     58.0 MiB      0.0 MiB           1       params = {
    27     58.0 MiB      0.0 MiB           1           "term": item_name,
    28     58.0 MiB      0.0 MiB           1           "location": location,
    29     58.0 MiB      0.0 MiB           1           "categories": "restaurants",
    30     58.0 MiB      0.0 MiB           1           "limit": limit  # Keep small for speed
    31                                             }
    32                                             
    33     58.0 MiB      0.0 MiB           1       try:
    34     60.2 MiB      2.3 MiB           1           response = requests.get(YELP_BASE_URL, headers=HEADERS, params=params, timeout=5)
    35     60.2 MiB      0.0 MiB           1           if response.status_code != 200:
    36                                                     print(f"Failed to fetch data: Status {response.status_code}")
    37                                                     return []
    38                                                 
    39     60.3 MiB      0.0 MiB           1           data = response.json().get("businesses", [])
    40     60.3 MiB      0.0 MiB           1           results = []
    41     60.3 MiB      0.0 MiB           4           for biz in data:
    42     60.3 MiB      0.0 MiB           3               cuisine = biz["categories"][0]["alias"] if biz["categories"] else "default"
    43     60.3 MiB      0.0 MiB           6               results.append({
    44     60.3 MiB      0.0 MiB           3                   "name": biz["name"],
    45     60.3 MiB      0.0 MiB           3                   "cuisine": cuisine,
    46     60.3 MiB      0.0 MiB           3                   "dish": MOCK_DISHES.get(cuisine, MOCK_DISHES["default"]),
    47     60.3 MiB      0.0 MiB           3                   "address": ", ".join(biz["location"]["display_address"])
    48                                                     })
    49     60.3 MiB      0.0 MiB           1           return results
    50                                             except Exception as e:
    51                                                 print(f"Error fetching Yelp data: {e}")
    52                                                 return []



Fetch Data Time: 1.1356 seconds

Food Finder Results for 'Burger':
  1. Maillards Smash Burgers
     Cuisine: Popuprestaurants
     Sample Dish: House Special
     Address: 1994 37th Ave, San Francisco, CA 94116
  2. Smish Smash
     Cuisine: Burgers
     Sample Dish: Classic Cheeseburger
     Address: 945 Market St, San Francisco, CA 94103
  3. Beep’s Burgers
     Cuisine: Burgers
     Sample Dish: Classic Cheeseburger
     Address: 1051 Ocean Ave, San Francisco, CA 94112
Results saved to food_finder_results.txt
"""

# Useful for fidning restaurants based on specific food