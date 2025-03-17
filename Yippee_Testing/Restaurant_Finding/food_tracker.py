import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import requests
import time
from datetime import datetime

# Load environment variables
load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")  # Path to your Firebase service account JSON

# Initialize Firebase (use your own service account JSON)
cred = credentials.Certificate(FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-project-id-default-rtdb.firebaseio.com/'  # Replace with your Firebase RTDB URL
})

# Yelp API setup
YELP_BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": f"Bearer {YELP_API_KEY}"}

def fetch_yelp_restaurants(item_name: str, location: str = "San Francisco, CA", limit: int = 3) -> list:
    """Fetch restaurant data from Yelp API."""
    params = {"term": item_name, "location": location, "categories": "restaurants", "limit": limit}
    try:
        response = requests.get(YELP_BASE_URL, headers=HEADERS, params=params, timeout=5)
        if response.status_code != 200:
            print(f"Yelp fetch failed: Status {response.status_code}")
            return []
        return [{"name": biz["name"], "dish": biz["categories"][0]["title"] if biz["categories"] else "Dish"} 
                for biz in response.json().get("businesses", [])]
    except Exception as e:
        print(f"Yelp error: {e}")
        return []

def add_to_tracker(user_id: str, item_name: str, dish: str):
    """Add a food item to Firebase Realtime Database."""
    ref = db.reference(f'users/{user_id}/tracker')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ref.push({
        "item_name": item_name,
        "dish": dish,
        "timestamp": timestamp
    })
    print(f"Added '{dish}' to tracker for {item_name}")

def get_tracker(user_id: str) -> list:
    """Retrieve all tracked items from Firebase."""
    ref = db.reference(f'users/{user_id}/tracker')
    data = ref.get()
    return [entry for entry in data.values()] if data else []

def print_tracker(user_id: str, tracker: list):
    """Print the tracked items."""
    print(f"\nFood Tracker for User {user_id}:")
    if not tracker:
        print("  No items tracked yet.")
    else:
        for i, item in enumerate(tracker, 1):
            print(f"  {i}. {item['item_name']} - {item['dish']} (Added: {item['timestamp']})")

def save_tracker(user_id: str, tracker: list, filename: str = "food_tracker.txt"):
    """Save the tracker to a text file."""
    try:
        with open(filename, "w") as file:
            file.write(f"Food Tracker for User {user_id}\n")
            file.write(f"Saved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            if not tracker:
                file.write("  No items tracked yet.\n")
            else:
                for i, item in enumerate(tracker, 1):
                    file.write(f"{i}. {item['item_name']} - {item['dish']} (Added: {item['timestamp']})\n")
        print(f"Tracker saved to {filename}")
    except Exception as e:
        print(f"Error saving tracker: {e}")

def measure_time(func, *args, name: str) -> float:
    """Measure execution time."""
    start = time.time()
    result = func(*args)
    duration = time.time() - start
    print(f"{name} Time: {duration:.4f} seconds")
    return result

def main():
    """Run the Food Tracker Program."""
    print("Starting Food Tracker Program...")
    user_id = "user123"  # Hardcoded for simplicity
    item_name = "Burger"  # Could use input()

    # Fetch Yelp data
    restaurants, fetch_time = measure_time(fetch_yelp_restaurants, item_name, name="Yelp Fetch")
    if not restaurants:
        print("No restaurants found. Exiting.")
        return

    # Add each restaurant's dish to Firebase tracker
    for restaurant in restaurants:
        add_to_tracker(user_id, restaurant["name"], restaurant["dish"])

    # Listen for real-time updates (simulated with a single fetch here)
    tracker = measure_time(get_tracker, user_id, name="Firebase Fetch")[0]
    
    # Print and save
    print_tracker(user_id, tracker)
    save_tracker(user_id, tracker)

    # Optional: Real-time listener (commented for simplicity)
    # ref = db.reference(f'users/{user_id}/tracker')
    # ref.listen(lambda event: print_tracker(user_id, get_tracker(user_id)))

if __name__ == "__main__":
    main()

"""
Starting Food Tracker Program...
Yelp Fetch Time: 0.3412 seconds
Added 'burgers' to tracker for Super Duper Burgers
Added 'burgers' to tracker for The Melt
Added 'seafood' to tracker for Fog Harbor Fish House

Firebase Fetch Time: 0.0213 seconds

Food Tracker for User user123:
  1. Super Duper Burgers - burgers (Added: 2025-03-09 06:45:12)
  2. The Melt - burgers (Added: 2025-03-09 06:45:12)
  3. Fog Harbor Fish House - seafood (Added: 2025-03-09 06:45:12)

Tracker saved to food_tracker.txt
"""