# Ingredient nutritional values (protein g, fiber g, vitamins mg - simplified)
nutrition_values = {
    "beef": {"protein": 25, "fiber": 0, "vitamins": 2},
    "chicken": {"protein": 27, "fiber": 0, "vitamins": 1.5},
    "fish": {"protein": 22, "fiber": 0, "vitamins": 3},
    "american cheese": {"protein": 5, "fiber": 0, "vitamins": 1},
    "cheddar cheese": {"protein": 7, "fiber": 0, "vitamins": 1.2},
    "mayonnaise": {"protein": 0, "fiber": 0, "vitamins": 0},
    "egg": {"protein": 6, "fiber": 0, "vitamins": 2},
    "lettuce": {"protein": 1, "fiber": 1, "vitamins": 5},
    "tomatoes": {"protein": 1, "fiber": 1.5, "vitamins": 10},
    "onions": {"protein": 1, "fiber": 2, "vitamins": 3},
    "bun": {"protein": 4, "fiber": 2, "vitamins": 1},
    "pickles": {"protein": 0, "fiber": 0.5, "vitamins": 1},
    "ketchup": {"protein": 0, "fiber": 0, "vitamins": 0.5},
    "mustard": {"protein": 0, "fiber": 0, "vitamins": 0.5},
    "avocado": {"protein": 2, "fiber": 7, "vitamins": 15},
    "tartar sauce": {"protein": 0, "fiber": 0, "vitamins": 0},
    # Vegetarian substitutes
    "veggie patty": {"protein": 15, "fiber": 5, "vitamins": 4},
    "tofu": {"protein": 20, "fiber": 2, "vitamins": 2},
    # Nutrient-boosting add-ons
    "lentils": {"protein": 9, "fiber": 8, "vitamins": 3, "price": 1.00},
    "chia seeds": {"protein": 5, "fiber": 10, "vitamins": 2, "price": 0.75},
    "spinach": {"protein": 3, "fiber": 2, "vitamins": 20, "price": 0.80}
}

# Base prices for ingredients (in dollars)
base_prices = {
    "beef": 3.00, "chicken": 2.50, "fish": 3.25, "american cheese": 1.00,
    "cheddar cheese": 1.00, "mayonnaise": 0.50, "egg": 0.75, "lettuce": 0.50,
    "tomatoes": 0.60, "onions": 0.40, "bun": 1.00, "pickles": 0.30,
    "ketchup": 0.20, "mustard": 0.20, "avocado": 1.50, "tartar sauce": 0.60,
    "veggie patty": 4.75, "tofu": 4.00
}

# Vegetarian substitutions
vegetarian_subs = {
    "beef": {"sub": "veggie patty", "price_diff": 1.75},
    "chicken": {"sub": "tofu", "price_diff": 1.50},
    "fish": {"sub": "veggie patty", "price_diff": 1.75}
}

# Menu items
menu_items = {
    "Beef Burger": {"ingredients": ["beef", "american cheese", "lettuce", "tomatoes", "onions", "bun"], "base_price": 7.00},
    "Chicken Sandwich": {"ingredients": ["chicken", "mayonnaise", "lettuce", "tomatoes", "bun"], "base_price": 6.50},
    "Fish Tacos": {"ingredients": ["fish", "lettuce", "tomatoes", "tartar sauce"], "base_price": 8.00}
}

def calculate_nutrition(ingredients):
    """Calculate total nutrition for a list of ingredients"""
    total = {"protein": 0, "fiber": 0, "vitamins": 0}
    for ingredient in ingredients:
        if ingredient in nutrition_values:
            for nutrient in total:
                total[nutrient] += nutrition_values[ingredient][nutrient]
    return total

def calculate_price(ingredients):
    """Calculate total price for a list of ingredients"""
    total = 0
    for ingredient in ingredients:
        total += base_prices.get(ingredient, nutrition_values.get(ingredient, {}).get("price", 0))
    return round(total, 2)

def make_vegetarian(item_name, item_details, nutrient_focus):
    """Convert to vegetarian and boost specified nutrient"""
    original_ingredients = item_details["ingredients"]
    veg_ingredients = original_ingredients.copy()
    price_diff = 0
    substitutions_made = []
    
    # Make vegetarian substitutions
    for i, ingredient in enumerate(veg_ingredients):
        if ingredient in vegetarian_subs:
            sub_info = vegetarian_subs[ingredient]
            veg_ingredients[i] = sub_info["sub"]
            price_diff += sub_info["price_diff"]
            substitutions_made.append(f"{ingredient} -> {sub_info['sub']} (+${sub_info['price_diff']:.2f})")
    
    # Add nutrient-boosting ingredient based on focus
    add_ons = {
        "protein": "lentils",   # High protein
        "fiber": "chia seeds",  # High fiber
        "vitamins": "spinach"   # High vitamins
    }
    if nutrient_focus in add_ons:
        add_on = add_ons[nutrient_focus]
        veg_ingredients.append(add_on)
        price_diff += nutrition_values[add_on]["price"]
        substitutions_made.append(f"Added {add_on} for {nutrient_focus} (+${nutrition_values[add_on]['price']:.2f})")
    
    # Calculate nutrition and prices
    original_nutrition = calculate_nutrition(original_ingredients)
    veg_nutrition = calculate_nutrition(veg_ingredients)
    original_price = calculate_price(original_ingredients)
    veg_price = original_price + price_diff
    
    return {
        "original_ingredients": original_ingredients,
        "veg_ingredients": veg_ingredients,
        "substitutions": substitutions_made,
        "original_price": item_details["base_price"],
        "veg_price": round(veg_price, 2),
        "price_difference": round(veg_price - item_details["base_price"], 2),
        "original_nutrition": original_nutrition,
        "veg_nutrition": veg_nutrition
    }

def display_results(nutrient_focus):
    """Display vegetarian conversion results with nutrient focus"""
    print(f"Vegetarian Conversion Results with {nutrient_focus.capitalize()} Focus (March 17, 2025)\n" + "="*50)
    
    for item_name, item_details in menu_items.items():
        result = make_vegetarian(item_name, item_details, nutrient_focus)
        
        print(f"\nItem: {item_name}")
        print(f"Original Ingredients: {', '.join(result['original_ingredients'])}")
        print(f"Vegetarian Ingredients: {', '.join(result['veg_ingredients'])}")
        if result["substitutions"]:
            print("Changes Made:")
            for sub in result["substitutions"]:
                print(f"  - {sub}")
        print(f"Original Price: ${result['original_price']:.2f}")
        print(f"Vegetarian Price: ${result['veg_price']:.2f}")
        print(f"Price Difference: ${result['price_difference']:.2f}")
        print("Nutrition Comparison:")
        print(f"  Original - Protein: {result['original_nutrition']['protein']}g, "
              f"Fiber: {result['original_nutrition']['fiber']}g, "
              f"Vitamins: {result['original_nutrition']['vitamins']}mg")
        print(f"  Vegetarian - Protein: {result['veg_nutrition']['protein']}g, "
              f"Fiber: {result['veg_nutrition']['fiber']}g, "
              f"Vitamins: {result['veg_nutrition']['vitamins']}mg")
        print("-"*50)

def get_user_preferences():
    """Prompt user for nutrient focus"""
    valid_focus = ["protein", "fiber", "vitamins"]
    print("As a vegetarian, which nutrient would you like to focus on?")
    print("Options: protein, fiber, vitamins")
    while True:
        focus = input("Enter your choice: ").lower().strip()
        if focus in valid_focus:
            return focus
        print("Invalid choice. Please choose: protein, fiber, or vitamins")

# Run the program
if __name__ == "__main__":
    nutrient_focus = get_user_preferences()
    display_results(nutrient_focus)

""" Example output:
As a vegetarian, which nutrient would you like to focus on?
Options: protein, fiber, vitamins
Enter your choice: protein
Vegetarian Conversion Results with Protein Focus (March 17, 2025)
==================================================

Item: Beef Burger
Original Ingredients: beef, american cheese, lettuce, tomatoes, onions, bun
Vegetarian Ingredients: veggie patty, american cheese, lettuce, tomatoes, onions, bun, lentils
Changes Made:
  - beef -> veggie patty (+$1.75)
  - Added lentils for protein (+$1.00)
Original Price: $7.00
Vegetarian Price: $9.25
Price Difference: $2.25
Nutrition Comparison:
  Original - Protein: 37g, Fiber: 6.5g, Vitamins: 22mg
  Vegetarian - Protein: 36g, Fiber: 19.5g, Vitamins: 27mg
--------------------------------------------------

Item: Chicken Sandwich
Original Ingredients: chicken, mayonnaise, lettuce, tomatoes, bun
Vegetarian Ingredients: tofu, mayonnaise, lettuce, tomatoes, bun, lentils
Changes Made:
  - chicken -> tofu (+$1.50)
  - Added lentils for protein (+$1.00)
Original Price: $6.50
Vegetarian Price: $7.60
Price Difference: $1.10
Nutrition Comparison:
  Original - Protein: 33g, Fiber: 4.5g, Vitamins: 17.5mg
  Vegetarian - Protein: 35g, Fiber: 14.5g, Vitamins: 21mg
--------------------------------------------------

Item: Fish Tacos
Original Ingredients: fish, lettuce, tomatoes, tartar sauce
Vegetarian Ingredients: veggie patty, lettuce, tomatoes, tartar sauce, lentils
Changes Made:
  - fish -> veggie patty (+$1.75)
  - Added lentils for protein (+$1.00)
Original Price: $8.00
Vegetarian Price: $7.70
Price Difference: $-0.30
Nutrition Comparison:
  Original - Protein: 24g, Fiber: 2.5g, Vitamins: 18mg
  Vegetarian - Protein: 26g, Fiber: 15.5g, Vitamins: 22mg
--------------------------------------------------
"""

# Subsitution for nutritional meal planning program
# Helpful for certain diets