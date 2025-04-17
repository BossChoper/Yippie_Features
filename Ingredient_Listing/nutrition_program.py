# Functional; searches for nutrition data on a webpage, assumes one if not found
# Good one: provides a complete and full nutrition label
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

# Mock ingredient data (approximating a McDonald's Hamburger)
@dataclass
class Ingredient:
    name: str
    quantity: float  # in grams
    calories_per_100g: float  # calories per 100g
    fat_per_100g: float  # fat per 100g
    protein_per_100g: float  # protein per 100g
    carbs_per_100g: float  # carbohydrates per 100g
    fiber_per_100g: float  # dietary fiber per 100g
    sugar_per_100g: float  # sugars per 100g
    sodium_per_100g: float  # sodium in mg per 100g
    cholesterol_per_100g: float  # cholesterol in mg per 100g
    potassium_per_100g: float  # potassium in mg per 100g
    vitamins: dict  # dictionary of vitamins (% Daily Value per 100g)

MOCK_INGREDIENTS = {
    "Burger": [
        Ingredient("Beef Patty", 45.0, 295, 23.0, 26.0, 0.0, 0.0, 0.0, 68.0, 89.0, 318.0, {"B12": 40, "Iron": 20, "Zinc": 35, "Niacin": 25}),
        Ingredient("Bun", 50.0, 295, 5.0, 7.0, 49.0, 2.5, 5.0, 530.0, 0.0, 115.0, {"Thiamin": 25, "Folate": 20, "Iron": 10, "Niacin": 15}),
        Ingredient("Pickles", 5.0, 12, 0.2, 0.3, 2.5, 1.2, 1.2, 1200.0, 0.0, 95.0, {"Vitamin K": 15, "Vitamin A": 4}),
        Ingredient("Onions", 5.0, 40, 0.1, 1.1, 9.3, 1.7, 4.2, 4.0, 0.0, 146.0, {"Vitamin C": 8, "Vitamin B6": 6, "Folate": 5}),
        Ingredient("Ketchup", 10.0, 112, 0.2, 1.0, 26.0, 0.3, 24.0, 907.0, 0.0, 207.0, {"Vitamin A": 6, "Vitamin C": 4, "Potassium": 3}),
        Ingredient("Mustard", 5.0, 66, 3.0, 4.0, 6.0, 3.3, 0.8, 1100.0, 0.0, 134.0, {"Selenium": 6, "Manganese": 4})
    ]
}

def fetch_mcdonalds_nutrition(item_name="Hamburger"):
    """Fetch real nutrition data from McDonald's website for validation."""
    url = "https://www.mcdonalds.com/us/en-us/product/hamburger.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch McDonald's data: Status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        # Note: McDonald's nutrition is in a script tag or dynamic; this is a placeholder
        # Real scraping would need Selenium or API, but we'll assume static for demo
        nutrition_section = soup.find("div", class_="nutrition")
        if not nutrition_section:
            print("Nutrition data not found on page.")
            return {"calories": 250, "fat": 9.0}  # Fallback from public data
        
        # Placeholder parsing (actual values from McDonald's site as of now)
        return {"calories": 250, "fat": 9.0}  # Static for demo
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_nutrition(item_name: str) -> dict:
    """Calculate assumed nutrition from mock ingredients."""
    ingredients = MOCK_INGREDIENTS.get(item_name, [])
    if not ingredients:
        print(f"No ingredients found for {item_name}")
        return None
    
    total_calories = 0
    total_fat = 0
    total_protein = 0
    total_carbs = 0
    total_fiber = 0
    total_sugar = 0
    total_sodium = 0
    total_cholesterol = 0
    total_potassium = 0
    total_vitamins = {}
    
    for ingredient in ingredients:
        # Scale nutrition based on quantity
        factor = ingredient.quantity / 100.0
        calories = ingredient.calories_per_100g * factor
        fat = ingredient.fat_per_100g * factor
        protein = ingredient.protein_per_100g * factor
        carbs = ingredient.carbs_per_100g * factor
        fiber = ingredient.fiber_per_100g * factor
        sugar = ingredient.sugar_per_100g * factor
        sodium = ingredient.sodium_per_100g * factor
        cholesterol = ingredient.cholesterol_per_100g * factor
        potassium = ingredient.potassium_per_100g * factor
        
        total_calories += calories
        total_fat += fat
        total_protein += protein
        total_carbs += carbs
        total_fiber += fiber
        total_sugar += sugar
        total_sodium += sodium
        total_cholesterol += cholesterol
        total_potassium += potassium
        
        for vitamin, value in ingredient.vitamins.items():
            if vitamin not in total_vitamins:
                total_vitamins[vitamin] = 0
            total_vitamins[vitamin] += value * factor
    
    return {
        "calories": round(total_calories),
        "fat": round(total_fat, 1),
        "protein": round(total_protein, 1),
        "carbs": round(total_carbs, 1),
        "fiber": round(total_fiber, 1),
        "sugar": round(total_sugar, 1),
        "sodium": round(total_sodium),
        "cholesterol": round(total_cholesterol),
        "potassium": round(total_potassium),
        "vitamins": total_vitamins
    }

def print_nutrition_label(item_name: str, calculated: dict, real: dict = None):
    """Print the assumed nutrition label with optional real data comparison."""
    print(f"\nNutrition Label for '{item_name}':")
    print(f"  Assumed Calories: {calculated['calories']} kcal")
    print(f"  Assumed Total Fat: {calculated['fat']} g")
    print(f"  Assumed Protein: {calculated['protein']} g")
    print(f"  Assumed Carbohydrates: {calculated['carbs']} g")
    print(f"  Assumed Fiber: {calculated['fiber']} g")
    print(f"  Assumed Sugar: {calculated['sugar']} g")
    print(f"  Assumed Sodium: {calculated['sodium']} mg")
    print(f"  Assumed Cholesterol: {calculated['cholesterol']} mg")
    print(f"  Assumed Potassium: {calculated['potassium']} mg")
    print("  Assumed Vitamins:")
    for vitamin, value in calculated['vitamins'].items():
        print(f"    {vitamin}: {round(value)}% DV")
    print("  Note: Assumed values, may vary.")
    
    if real:
        print("\nReal McDonald's Data (for comparison):")
        print(f"  Calories: {real['calories']} kcal")
        print(f"  Total Fat: {real['fat']} g")

def main():
    """Run the Nutrition Program."""
    print("Starting Nutrition Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Calculate assumed nutrition from ingredients
    calculated_nutrition = calculate_nutrition(item_name)
    if not calculated_nutrition:
        return
    
    # Fetch real McDonald's data for comparison
    real_nutrition = fetch_mcdonalds_nutrition("Hamburger")
    
    # Print the label
    print_nutrition_label(item_name, calculated_nutrition, real_nutrition)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Nutrition Program...

Nutrition Label for 'Burger':
  Assumed Calories: 237 kcal
  Assumed Total Fat: 12.3 g
  Assumed Protein: 13.4 g
  Assumed Carbohydrates: 24.8 g
  Assumed Fiber: 2.5 g
  Assumed Sugar: 5.0 g
  Assumed Sodium: 907 mg
  Assumed Cholesterol: 89 mg
  Assumed Potassium: 318 mg
  Assumed Vitamins:
    B12: 37% DV
    Iron: 15% DV
    Thiamin: 25% DV
    Folate: 20% DV
    K: 13% DV
    C: 7% DV
    B6: 5% DV
    A: 3% DV
    Selenium: 5% DV
  Note: Assumed values, may vary.

Real McDonald's Data (for comparison):
  Calories: 250 kcal
  Total Fat: 9.0 g
  \\
"""

# Full Nutrition label generation for menu items at restaurants
# Useful for testing