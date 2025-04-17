# NONFunctional; searches google for recipe websites
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re

def get_recipe_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title (common tags for titles)
        title = soup.find('h1') or soup.find('title')
        title = title.text.strip() if title else "Unknown Title"
        
        # Extract ingredients (common patterns)
        ingredients = []
        for tag in soup.find_all(['li', 'p', 'div'], class_=re.compile('ingredient|ingred', re.I)):
            text = tag.text.strip()
            if text and len(text) > 5 and any(char.isalpha() for char in text):
                ingredients.append(text)
        if not ingredients:
            for tag in soup.find_all('li'):
                text = tag.text.strip()
                if text and len(text) > 5 and any(char.isalpha() for char in text):
                    ingredients.append(text)
        
        # Extract instructions (common patterns)
        instructions = []
        for tag in soup.find_all(['li', 'p', 'div'], class_=re.compile('step|instruction|direction', re.I)):
            text = tag.text.strip()
            if text and len(text) > 20:
                instructions.append(text)
        if not instructions:
            for tag in soup.find_all('li'):
                text = tag.text.strip()
                if text and len(text) > 20:
                    instructions.append(text)
        
        if not ingredients or not instructions:
            return None
        
        return {
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions if instructions else ["Instructions not available"]
        }
    except Exception as e:
        return None

def get_recipes(food_item):
    query = f"{food_item} recipe site:*.edu | site:*.org | site:*.com -inurl:(login | signup)"
    recipes = []
    
    # Search Google for recipe URLs
    urls = []
    try:
        for url in search(query, num_results=10, lang="en"):
            if url not in urls:
                urls.append(url)
                if len(urls) >= 5:  # Get extra URLs to ensure we find 3 valid recipes
                    break
    except Exception as e:
        return f"Error searching Google: {str(e)}"
    
    if not urls:
        return f"No recipe pages found for {food_item}"
    
    # Process each URL to extract recipe data
    for url in urls:
        recipe = get_recipe_from_url(url)
        if recipe and recipe not in recipes:
            recipes.append(recipe)
            if len(recipes) >= 3:  # Stop once we have 3 valid recipes
                break
    
    return recipes if recipes else f"Could not extract valid recipes for {food_item}"

def display_recipes(recipes):
    if isinstance(recipes, str):
        print(recipes)
        return
    
    for i, recipe in enumerate(recipes, 1):
        print(f"\nRecipe {i}: {recipe['title']}")
        print("\nIngredients:")
        for ingredient in recipe['ingredients']:
            print(f"- {ingredient}")
        print("\nInstructions:")
        for j, step in enumerate(recipe['instructions'], 1):
            print(f"{j}. {step}")
        print("-" * 50)

def main():
    food_item = input("Enter a food item (e.g., cheeseburgers): ").strip()
    if not food_item:
        print("Please enter a valid food item.")
        return
    
    print(f"\nFetching recipes for {food_item} from Google search...\n")
    recipes = get_recipes(food_item)
    display_recipes(recipes)

if __name__ == "__main__":
    main()

""" Example output: 
Enter a food item (e.g., cheeseburgers): cheeseburgers

Fetching recipes for cheeseburgers from Google search...

Recipe 1: Best Cheeseburger Recipe
Ingredients:
- 1 lb ground beef
- 1 tsp salt
- 1/2 tsp black pepper
- 4 slices cheddar cheese
- 4 hamburger buns
Instructions:
1. Preheat grill to medium-high heat.
2. Mix beef, salt, and pepper; form into 4 patties.
3. Grill patties 4-5 minutes per side, adding cheese in the last minute.
...

[... Additional recipes follow ...]
"""