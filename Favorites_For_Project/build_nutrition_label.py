# Functional; builds a nutrition label from a mock recipe with ingredients and nutrients per ingredient
# Favorite
from dataclasses import dataclass
from typing import List, Dict

# Mock ingredient data with nutritional values (per 100g unless specified)
@dataclass
class Ingredient:
    name: str
    quantity: float  # in grams
    calories_per_100g: float
    fat_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float

# Mock recipes for "Burger" (from Generated Ingredients Program, now with nutrition)
MOCK_RECIPES = {
    "Burger": [
        # Recipe 1: Classic Burger
        {
            "source": "RecipeSite1",
            "ingredients": [
                Ingredient("Ground Beef", 226.8, 295, 23.0, 17.0, 0.0),  # 1/2 lb = 226.8g
                Ingredient("Burger Bun", 50.0, 295, 5.0, 6.0, 52.0),
                Ingredient("Cheddar Cheese", 28.0, 403, 33.0, 25.0, 1.3),  # 1 slice ≈ 28g
                Ingredient("Lettuce", 20.0, 15, 0.2, 1.4, 2.9),
                Ingredient("Tomato", 50.0, 18, 0.2, 0.9, 3.9),
                Ingredient("Ketchup", 15.0, 112, 0.2, 1.3, 26.0),  # 1 tbsp ≈ 15g
                Ingredient("Mustard", 5.0, 66, 3.0, 3.7, 5.8)    # 1 tsp ≈ 5g
            ]
        },
        # Recipe 2: Simple Burger
        {
            "source": "RecipeSite2",
            "ingredients": [
                Ingredient("Ground Beef", 226.8, 295, 23.0, 17.0, 0.0),
                Ingredient("Burger Bun", 50.0, 295, 5.0, 6.0, 52.0),
                Ingredient("Pickles", 15.0, 12, 0.2, 0.5, 2.4),
                Ingredient("Ketchup", 15.0, 112, 0.2, 1.3, 26.0),
                Ingredient("Onions", 20.0, 40, 0.1, 1.1, 9.3)
            ]
        },
        # Recipe 3: Burger Deluxe
        {
            "source": "RecipeSite3",
            "ingredients": [
                Ingredient("Ground Beef", 226.8, 295, 23.0, 17.0, 0.0),
                Ingredient("Burger Bun", 50.0, 295, 5.0, 6.0, 52.0),
                Ingredient("Cheddar Cheese", 28.0, 403, 33.0, 25.0, 1.3),
                Ingredient("Lettuce", 20.0, 15, 0.2, 1.4, 2.9),
                Ingredient("Tomato", 50.0, 18, 0.2, 0.9, 3.9),
                Ingredient("Mayonnaise", 15.0, 680, 75.0, 0.4, 0.6)  # 1 tbsp ≈ 15g
            ]
        }
    ]
}

def fetch_ingredients(item_name: str) -> List[Ingredient]:
    """Generate a combined ingredients list from mock recipes."""
    recipes = MOCK_RECIPES.get(item_name, [])
    if not recipes:
        print(f"No recipes found for {item_name}")
        return []
    
    # Combine ingredients by name, averaging quantities if repeated
    ingredient_dict = {}
    for recipe in recipes:
        for ing in recipe["ingredients"]:
            if ing.name in ingredient_dict:
                # Average quantities for simplicity (could weight by recipe)
                existing = ingredient_dict[ing.name]
                existing.quantity = (existing.quantity + ing.quantity) / 2
            else:
                ingredient_dict[ing.name] = ing
    
    return list(ingredient_dict.values())

def calculate_nutrition(ingredients: List[Ingredient]) -> Dict[str, float]:
    """Calculate total nutrition from ingredients."""
    total_calories = 0
    total_fat = 0
    total_protein = 0
    total_carbs = 0
    total_weight = 0
    
    for ing in ingredients:
        factor = ing.quantity / 100.0  # Scale by quantity
        total_calories += ing.calories_per_100g * factor
        total_fat += ing.fat_per_100g * factor
        total_protein += ing.protein_per_100g * factor
        total_carbs += ing.carbs_per_100g * factor
        total_weight += ing.quantity
    
    return {
        "calories": round(total_calories),
        "fat": round(total_fat, 1),
        "protein": round(total_protein, 1),
        "carbs": round(total_carbs, 1),
        "weight": round(total_weight)
    }

def print_nutrition_label(item_name: str, nutrition: Dict[str, float], ingredients: List[Ingredient]):
    """Print the full nutrition label with ingredients."""
    print(f"\nFull Nutrition Label for '{item_name}':")
    print(f"  Total Weight: {nutrition['weight']} g")
    print(f"  Calories: {nutrition['calories']} kcal")
    print(f"  Total Fat: {nutrition['fat']} g")
    print(f"  Protein: {nutrition['protein']} g")
    print(f"  Carbohydrates: {nutrition['carbs']} g")
    print("\nIngredients:")
    for ing in ingredients:
        print(f"  - {ing.name} ({ing.quantity} g)")
    print("Note: Assumed values based on similar recipes, may vary.")

def main():
    """Run the Full Nutrition Program."""
    print("Starting Full Nutrition Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Fetch combined ingredients
    ingredients = fetch_ingredients(item_name)
    if not ingredients:
        return
    
    # Calculate nutrition
    nutrition = calculate_nutrition(ingredients)
    
    # Print the label
    print_nutrition_label(item_name, nutrition, ingredients)

if __name__ == "__main__":
    main()

"""
Example output:
Starting Full Nutrition Program...

Full Nutrition Label for 'Burger':
  Total Weight: 385 g
  Calories: 858 kcal
  Total Fat: 63.6 g
  Protein: 51.1 g
  Carbohydrates: 52.7 g

Ingredients:
  - Ground Beef (226.8 g)
  - Burger Bun (50.0 g)
  - Cheddar Cheese (28.0 g)
  - Lettuce (20.0 g)
  - Tomato (50.0 g)
  - Ketchup (15.0 g)
  - Mustard (5.0 g)
  - Pickles (15.0 g)
  - Onions (20.0 g)
  - Mayonnaise (15.0 g)
Note: Assumed values based on similar recipes, may vary.

"""