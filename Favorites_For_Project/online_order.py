#Functional
# Simulates an online ordering mechanism for getting menu items from Yelp and planning an order
# Favorite
import os
from dotenv import load_dotenv
import random

# Load environment variables (for future API integration)
load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")

# Mock menu data
MOCK_MENU = {
    "Burger Joint": {
        "items": [
            {"name": "Classic Burger", "price": 8.99, "description": "Beef patty, lettuce, tomato"},
            {"name": "Veggie Burger", "price": 7.99, "description": "Veggie patty, avocado"},
            {"name": "Fries", "price": 3.49, "description": "Crispy golden fries"}
        ],
        "location": "123 Food St, San Francisco, CA"
    },
    "Pizza Palace": {
        "items": [
            {"name": "Pepperoni Pizza", "price": 12.99, "description": "Pepperoni, cheese"},
            {"name": "Margherita Pizza", "price": 11.49, "description": "Tomato, basil"},
            {"name": "Garlic Bread", "price": 4.99, "description": "Toasted with garlic"}
        ],
        "location": "456 Slice Ave, San Francisco, CA"
    }
}

def fetch_menu(restaurant_name: str) -> dict:
    """Fetch mock menu items for a given restaurant."""
    return MOCK_MENU.get(restaurant_name, {"items": [], "location": "Unknown"})

def print_menu(restaurant_name: str, menu: dict):
    """Print menu items as order options."""
    print(f"\nMenu for {restaurant_name} ({menu['location']}):")
    if not menu["items"]:
        print("  No items available.")
        return
    
    for i, item in enumerate(menu["items"], 1):
        print(f"  {i}. {item['name']} - ${item['price']:.2f}")
        print(f"     {item['description']}")

def simulate_order(restaurant_name: str, menu: dict):
    """Simulate placing an order with random selection."""
    if not menu["items"]:
        print("Cannot place order: No items available.")
        return
    
    selected_item = random.choice(menu["items"])
    print(f"\nOrder placed at {restaurant_name}:")
    print(f"  Item: {selected_item['name']}")
    print(f"  Price: ${selected_item['price']:.2f}")
    print(f"  Estimated Delivery: 30-45 minutes")

def main():
    """Run the Online Ordering Program."""
    print("Starting Online Ordering Program...")
    restaurant_name = "Burger Joint"  # Could be made interactive
    
    # Fetch and display menu
    menu = fetch_menu(restaurant_name)
    print_menu(restaurant_name, menu)
    
    # Simulate an order
    simulate_order(restaurant_name, menu)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Online Ordering Program...

Menu for Burger Joint (123 Food St, San Francisco, CA):
  1. Classic Burger - $8.99
     Beef patty, lettuce, tomato
  2. Veggie Burger - $7.99
     Veggie patty, avocado
  3. Fries - $3.49
     Crispy golden fries

Order placed at Burger Joint:
  Item: Veggie Burger
  Price: $7.99
  Estimated Delivery: 30-45 minutes
\\
"""

# Menu order practice
# Useful for planning meal orders prior to placement/vendors
