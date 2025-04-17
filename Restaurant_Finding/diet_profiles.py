# FUNCTIONAL
# Finds restaurants based on user diet; vegan resaurants for vegan, vegeterian  + vegan for vegeterians
from dataclasses import dataclass
from typing import List, Dict

# Mock restaurant data
@dataclass
class Restaurant:
    name: str
    menu_items: Dict[str, List[str]]  # {category: [items]}
    diet_tags: List[str]  # Tags like "vegan-friendly", "gluten-free"
    warnings: List[str]  # Warnings like "No separate vegan equipment"

MOCK_RESTAURANTS = [
    Restaurant(
        name="Green Leaf Cafe",
        menu_items={
            "Mains": ["Vegan Burger", "Grilled Chicken"],
            "Desserts": ["Vegan Cheesecake", "Chocolate Cake"]
        },
        diet_tags=["vegan-friendly", "vegetarian"],
        warnings=["No separate vegan equipment"]
    ),
    Restaurant(
        name="Meat Lovers Haven",
        menu_items={
            "Mains": ["Beef Steak", "Pork Ribs"],
            "Desserts": ["Ice Cream"]
        },
        diet_tags=["omnivore"],
        warnings=["No vegan options"]
    ),
    Restaurant(
        name="Veggie Delight",
        menu_items={
            "Mains": ["Vegan Pasta", "Tofu Stir-Fry"],
            "Desserts": ["Fruit Salad"]
        },
        diet_tags=["vegan", "gluten-free"],
        warnings=["Allergen-free kitchen"]
    ),
]

# Supported diet preferences
DIET_PREFERENCES = ["vegan", "vegetarian", "gluten-free", "omnivore"]

def get_user_diet():
    """Prompt user for diet preference and validate input."""
    print("Available diet preferences:", ", ".join(DIET_PREFERENCES))
    while True:
        diet = input("Enter your diet preference: ").lower().strip()
        if diet in DIET_PREFERENCES:
            return diet
        print("Invalid preference. Please choose from:", ", ".join(DIET_PREFERENCES))

def filter_restaurants(diet: str, restaurants: List[Restaurant]) -> List[Restaurant]:
    """Filter restaurants based on diet preference."""
    filtered = []
    for restaurant in restaurants:
        # Check if diet is explicitly supported or compatible
        if diet in restaurant.diet_tags or (diet == "vegetarian" and "vegan" in restaurant.diet_tags):
            filtered.append(restaurant)
    return filtered

def print_results(diet: str, restaurants: List[Restaurant]):
    """Print filtered restaurant results with tags and warnings."""
    print(f"\nRestaurants matching '{diet}' preference:")
    if not restaurants:
        print("No matching restaurants found.")
        return
    
    for restaurant in restaurants:
        print(f"\n- {restaurant.name}")
        print("  Menu Items:")
        for category, items in restaurant.menu_items.items():
            # Filter items based on diet (simplified logic)
            relevant_items = [item for item in items if diet in item.lower() or diet == "omnivore" or "vegan" in item.lower()]
            if relevant_items:
                print(f"    {category}: {', '.join(relevant_items)}")
        print("  Tags:", ", ".join(restaurant.diet_tags))
        print("  Warnings:", ", ".join(restaurant.warnings) if restaurant.warnings else "None")

def main():
    """Run the Diet Profiles Program."""
    print("Starting Diet Profiles Program...")
    user_diet = get_user_diet()
    filtered_restaurants = filter_restaurants(user_diet, MOCK_RESTAURANTS)
    print_results(user_diet, filtered_restaurants)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Diet Profiles Program...
Available diet preferences: vegan, vegetarian, gluten-free, omnivore
Enter your diet preference: vegan

Restaurants matching 'vegan' preference:

- Green Leaf Cafe
  Menu Items:
    Mains: Vegan Burger
    Desserts: Vegan Cheesecake
  Tags: vegan-friendly, vegetarian
  Warnings: No separate vegan equipment

- Veggie Delight
  Menu Items:
    Mains: Vegan Pasta, Tofu Stir-Fry
  Tags: vegan, gluten-free
  Warnings: Allergen-free kitchen
  \\
"""

# Find restaurants based on diet
# Useful for querying practice