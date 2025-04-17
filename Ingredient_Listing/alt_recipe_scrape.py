# Functional; takes websites and retrieves ingredients list
# Favorite
import requests
from bs4 import BeautifulSoup

def get_ingredients(url):
    """
    Retrieves a list of ingredients from a recipe webpage.

    Args:
        url (str): The URL of the recipe webpage.

    Returns:
        list: A list of strings, where each string is an ingredient.
              Returns None if the ingredients list cannot be found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for common patterns in ingredient list formatting.  This may need
        # adjustment based on the specific website structure.
        
        # Attempt 1: Look for a specific section with ingredient list (common on many recipe sites)
        ingredient_sections = soup.find_all('div', class_='ingredients')  # Adjust class name as needed
        if ingredient_sections:
            ingredients = []
            for section in ingredient_sections:
                items = section.find_all('li') # Find list items within the section
                for item in items:
                    ingredients.append(item.text.strip())
            if ingredients:
                return ingredients
        
        # Attempt 2: Look for ingredient lists within a 'recipe' or similar div
        recipe_div = soup.find('div', class_='recipe') #Adjust class name as needed
        if recipe_div:
            ingredients_heading = recipe_div.find('h4', string=lambda text: "Ingredients" in text) or \
                                recipe_div.find('h3', string=lambda text: "Ingredients" in text) or \
                                recipe_div.find('h2', string=lambda text: "Ingredients" in text)
            if ingredients_heading:
                ingredients_list = ingredients_heading.find_next('ul')  #Assumes list is after the heading
                if ingredients_list:
                    ingredients = [item.text.strip() for item in ingredients_list.find_all('li')]
                    return ingredients

        # Attempt 3:  Specific to rabbitandwolves.com based on inspection
        ingredients_heading = soup.find('h3', string='Ingredients')
        if ingredients_heading:
            ingredients = []
            current_element = ingredients_heading.find_next()
            while current_element and current_element.name != 'h3':  # Stop at next heading
                if current_element.name == 'ul':
                    for item in current_element.find_all('li'):
                        ingredients.append(item.text.strip())
                current_element = current_element.find_next()
            if ingredients:
                return ingredients


        print("Could not find ingredients using common patterns.  Inspect the webpage and adjust the script.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage:
url = "https://veggiesociety.com/best-vegan-ribs-recipe-jackfruit/"
# website 1: https://www.rabbitandwolves.com/vegan-chinese-style-ribs/
ingredients = get_ingredients(url)

if ingredients:
    print("Ingredients:")
    for ingredient in ingredients:
        print(f"- {ingredient}")
else:
    print("Ingredients not found.")

""" IT WORKED! Courtesy of Perplexity. Scraping web requires an AI that can
search the web, like perplexity.
 Output:
Ingredients:
- 1 1/4 C. Vital wheat gluten
- 2 Tbsp. Nutritional yeast
- 1 tsp. Garlic powder
- 1/2 tsp. Chinese 5 spice
- 3/4 C. Vegetable broth
- 1 Tbsp. Tahini
- 1 Tbsp. Soy sauce
- 1 Tbsp. Hoisin sauce
- 1 tsp. Liquid smoke
- 1/2 C. Hoisin sauce
- 1/4 C. Soy sauce
- 2 Tbsp. Agave nectar
- 1/2 tsp. Chinese 5 spice
- 1/2 tsp. Garlic powder
- 1/4 tsp. Ginger powder
- Natural red food coloring, optional ( I used Watkins food coloring)

Website 2:
Ingredients:
- 20 oz canned green jackfruit (packed in water not syrup)
- 1.25 cups vital wheat gluten + more as needed
- 3 tbsp nutritional yeast
- 1 tbsp sweet smoked paprika
- 1 tbsp onion powder
- 1 tsp garlic powder
- 1 tsp mustard powder
- 1/2 tsp red chili flakes , or to taste
- 4 cloves garlic , grated
- 3/4 cups  water (or low sodium vegetable stock)
- 3 tbsp tamari or coco aminos
- 1 cup BBQ sauce  + more for dipping
- 2 leaves bay
- 1/3 cup fresh chives , for garnish
- 1 tsp liquid smoke (optional, only if you want a very smoky flavor)
- sea salt + black pepper to taste  (1/2 tsp each)
"""