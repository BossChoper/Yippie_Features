import requests
from bs4 import BeautifulSoup
from collections import Counter
from typing import List, Dict

# Mock recipe data (simulating scraped recipes for a "Burger")
MOCK_RECIPES = {
    "Burger": [
        # Recipe 1 (e.g., "Classic Burger" from a mock source)
        {
            "source": "RecipeSite1",
            "ingredients": [
                "Ground Beef (1/2 lb)",
                "Burger Bun",
                "Cheddar Cheese (1 slice)",
                "Lettuce",
                "Tomato",
                "Ketchup (1 tbsp)",
                "Mustard (1 tsp)"
            ]
        },
        # Recipe 2 (e.g., "Simple Burger" from a mock source)
        {
            "source": "RecipeSite2",
            "ingredients": [
                "Ground Beef (1/2 lb)",
                "Burger Bun",
                "Pickles",
                "Ketchup (1 tbsp)",
                "Onions (chopped)"
            ]
        },
        # Recipe 3 (e.g., "Burger Deluxe" from a mock source)
        {
            "source": "RecipeSite3",
            "ingredients": [
                "Ground Beef (1/2 lb)",
                "Burger Bun",
                "Cheddar Cheese (1 slice)",
                "Lettuce",
                "Tomato",
                "Mayonnaise (1 tbsp)"
            ]
        }
    ]
}

def fetch_mock_recipe_data(item_name: str) -> List[Dict]:
    """Fetch mock recipe data (simulating scraped data)."""
    return MOCK_RECIPES.get(item_name, [])

def fetch_real_recipe_data(item_name: str) -> List[Dict]:
    """Placeholder for real recipe scraping (e.g., from AllRecipes)."""
    # Example URL (not functional here, just for demo structure)
    url = f"https://www.allrecipes.com/search/results/?search={item_name}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        # Placeholder logic (real parsing would depend on site structure)
        recipes = []
        for _ in range(3):  # Simulate 3 recipes
            recipes.append({
                "source": "AllRecipes",
                "ingredients": ["Ground Beef", "Bun"]  # Dummy data
            })
        return recipes
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def combine_ingredients(recipes: List[Dict]) -> List[str]:
    """Combine common ingredients from recipes."""
    if not recipes:
        return []
    
    # Flatten all ingredients into a single list
    all_ingredients = []
    for recipe in recipes:
        all_ingredients.extend(recipe["ingredients"])
    
    # Count occurrences and filter common or notable ingredients
    ingredient_counts = Counter(all_ingredients)
    total_recipes = len(recipes)
    
    # Include ingredients appearing in at least 2 recipes or adjust threshold
    combined = [ingredient for ingredient, count in ingredient_counts.items() if count >= 2]
    
    # If too few, include the most frequent ones
    if len(combined) < 3:
        combined = [ingredient for ingredient, _ in ingredient_counts.most_common(3)]
    
    return combined

def print_ingredients_list(item_name: str, ingredients: List[str]):
    """Print the generated ingredients list."""
    print(f"\nAssumed Ingredients List for '{item_name}':")
    if not ingredients:
        print("  No ingredients generated.")
    else:
        for ingredient in ingredients:
            print(f"  - {ingredient}")
        print("  Note: Based on similar recipes.")

def main():
    """Run the Generated Ingredients Program."""
    print("Starting Generated Ingredients Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Use mock data for this demo (replace with fetch_real_recipe_data for real use)
    recipes = fetch_mock_recipe_data(item_name)
    if not recipes:
        print(f"No recipe data found for {item_name}")
        return
    
    # Combine ingredients
    ingredients = combine_ingredients(recipes)
    
    # Print the result
    print_ingredients_list(item_name, ingredients)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Generated Ingredients Program...

Assumed Ingredients List for 'Burger':
  - Ground Beef (1/2 lb)
  - Burger Bun
  - Lettuce
  Note: Based on similar recipes.
  \\
"""

# Useful for suggesting ingredients lists for analyzing