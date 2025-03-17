import requests
from bs4 import BeautifulSoup

# Target site: AllRecipes search page
BASE_URL = "https://www.allrecipes.com/search"

def fetch_recipes(item_name: str) -> list:
    """Scrape at least 3 recipes for a menu item from AllRecipes."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    params = {"q": item_name}  # Query parameter for search
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch page: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find recipe cards (based on AllRecipes' current structure)
        recipe_cards = soup.find_all("a", class_="card__titleLink")
        if not recipe_cards:
            print("No recipe cards found. Site structure may have changed.")
            return []
        
        # Extract titles and URLs (limit to 3+)
        recipes = []
        for card in recipe_cards[:5]:  # Get up to 5 to ensure 3+ valid ones
            title = card.get("title", "").strip()
            url = card.get("href", "").strip()
            if title and url and "recipe" in url.lower():  # Filter for actual recipes
                recipes.append({"title": title, "url": url})
            if len(recipes) >= 3:  # Stop at 3 valid recipes
                break
        
        return recipes if recipes else []
    
    except Exception as e:
        print(f"Error fetching recipes: {e}")
        return []

def print_recipes(item_name: str, recipes: list):
    """Print the scraped recipe titles and URLs."""
    print(f"\nRecipes for '{item_name}':")
    if not recipes:
        print("  No recipes found.")
    else:
        for i, recipe in enumerate(recipes, 1):
            print(f"  Recipe {i}:")
            print(f"    Title: {recipe['title']}")
            print(f"    URL: {recipe['url']}")
            print()

def main():
    """Run the Recipes Program."""
    print("Starting Recipes Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Fetch and print recipes
    recipes = fetch_recipes(item_name)
    print_recipes(item_name, recipes)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Recipes Program...

Recipes for 'Burger':
  Recipe 1:
    Title: Juiciest Hamburgers Ever
    URL: https://www.allrecipes.com/recipe/14695/juiciest-hamburgers-ever/

  Recipe 2:
    Title: Best Hamburger Ever
    URL: https://www.allrecipes.com/recipe/72657/best-hamburger-ever/

  Recipe 3:
    Title: The Perfect Basic Burger
    URL: https://www.allrecipes.com/recipe/25473/the-perfect-basic-burger/
\\
"""

# Useful for finding associated recipes based on menu item name