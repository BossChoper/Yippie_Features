# Nonfunctional; frankly useless. Supposed to search a websites and scrape
import requests
from bs4 import BeautifulSoup
import re

def get_recipes(food_item):
    # Base URL for AllRecipes search
    search_url = f"https://www.allrecipes.com/search/results/?q={food_item}&sort=re"
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send request to search page
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return f"Failed to retrieve search page. Status code: {response.status_code}"
    
    # Parse search page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find recipe card links (limited to first 3+ valid recipes)
    recipe_links = []
    for card in soup.find_all('a', href=True):
        href = card['href']
        if '/recipe/' in href and href not in recipe_links:
            recipe_links.append(href)
            if len(recipe_links) >= 5:  # Get more than 3 to ensure we have at least 3 after filtering
                break
    
    if not recipe_links:
        return f"No recipes found for {food_item}"
    
    # Store results
    recipes = []
    
    # Process each recipe page
    for link in recipe_links[:3]:  # Limit to exactly 3 recipes
        recipe_response = requests.get(link, headers=headers)
        if recipe_response.status_code != 200:
            continue
            
        recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')
        
        # Get recipe title
        title = recipe_soup.find('h1', class_='headline')
        title = title.text.strip() if title else "Unknown Title"
        
        # Get ingredients
        ingredients = []
        ingredient_section = recipe_soup.find_all('li', class_='ingredients-item')
        for item in ingredient_section:
            ingredient = item.text.strip()
            if ingredient:
                ingredients.append(ingredient)
        
        # Get instructions
        instructions = []
        instruction_section = recipe_soup.find_all('li', class_='subcontainer instructions-section-item')
        for step in instruction_section:
            instruction = step.find('p')
            if instruction:
                instructions.append(instruction.text.strip())
        
        # Store recipe data
        recipes.append({
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions if instructions else ["Instructions not available"]
        })
    
    return recipes

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
    
    print(f"\nFetching recipes for {food_item}...\n")
    recipes = get_recipes(food_item)
    display_recipes(recipes)

if __name__ == "__main__":
    main()

""" Example output: 
Enter a food item (e.g., cheeseburgers): cheeseburgers

Fetching recipes for cheeseburgers...

Recipe 1: Juiciest Hamburgers Ever
Ingredients:
- 2 pounds ground beef
- 1 egg, beaten
- 3/4 cup dry bread crumbs
- 3 tablespoons evaporated milk
- 2 tablespoons Worcestershire sauce
- 1/8 teaspoon cayenne pepper
- 2 cloves garlic, minced
Instructions:
1. Preheat grill for high heat.
2. In a large bowl, mix the ground beef, egg, bread crumbs, evaporated milk, Worcestershire sauce, cayenne pepper, and garlic using your hands. Form the mixture into 8 hamburger patties.
3. Lightly oil the grill grate. Grill patties 5 minutes per side, or until well done.

[... Additional recipes follow ...]
"""