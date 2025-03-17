import requests
from bs4 import BeautifulSoup

# Target URL (McDonald's Hamburger page as an example)
TARGET_URL = "https://www.mcdonalds.com/us/en-us/product/hamburger.html"

# Mock fallback data if scraping fails (based on McDonald's public info)
MOCK_INGREDIENTS = [
    "100% Beef Patty",
    "Regular Bun",
    "Pickle Slices",
    "Ketchup",
    "Mustard",
    "Rehydrated Onions"
]

def fetch_ingredients(url: str) -> list:
    """Scrape ingredients list from a public source or use mock data if fails."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch page: Status {response.status_code}")
            return MOCK_INGREDIENTS
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for ingredients section (McDonald's uses a specific structure)
        # Note: This is approximate; real site uses JS, so this may not work without Selenium
        ingredients_section = soup.find("div", class_="cmp-product-details-main__nutrition-ingredient-legal")
        if not ingredients_section:
            print("Ingredients section not found. Using mock data.")
            return MOCK_INGREDIENTS
        
        # Extract ingredients (simplified parsing; adjust based on actual HTML)
        ingredients = []
        for item in ingredients_section.find_all("li"):
            ingredient = item.get_text(strip=True)
            if ingredient:
                ingredients.append(ingredient)
        
        return ingredients if ingredients else MOCK_INGREDIENTS
    
    except Exception as e:
        print(f"Error fetching ingredients: {e}")
        return MOCK_INGREDIENTS

def print_ingredients_list(item_name: str, ingredients: list):
    """Print the scraped or assumed ingredients list with a disclaimer."""
    print(f"\nAssumed Ingredients List for '{item_name}':")
    for ingredient in ingredients:
        print(f"  - {ingredient}")
    print("Disclaimer: This meal may have different ingredients. Please contact restaurant for further information.")

def main():
    """Run the Ingredients Program."""
    print("Starting Ingredients Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Fetch and print ingredients
    ingredients = fetch_ingredients(TARGET_URL)
    print_ingredients_list(item_name, ingredients)

if __name__ == "__main__":
    main()

"""
\\ Example output: 
Starting Ingredients Program...

Assumed Ingredients List for 'Burger':
  - 100% Beef Patty
  - Regular Bun
  - Pickle Slices
  - Ketchup
  - Mustard
  - Rehydrated Onions
Disclaimer: This meal may have different ingredients. Please contact restaurant for further information.
\\
"""