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
    # Substitutes
    "Impossible patty": {"protein": 19, "fiber": 3, "vitamins": 4},
    "plant-based chicken": {"protein": 20, "fiber": 2, "vitamins": 3},
    "plant-based fish": {"protein": 15, "fiber": 2, "vitamins": 3},
    "vegan cheese": {"protein": 3, "fiber": 0, "vitamins": 2},
    "vegan mayo": {"protein": 0, "fiber": 0, "vitamins": 0.5},
    "flax egg": {"protein": 2, "fiber": 3, "vitamins": 1},
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
    "Impossible patty": 5.50, "plant-based chicken": 4.50, "plant-based fish": 5.50,
    "vegan cheese": 2.50, "vegan mayo": 1.00, "flax egg": 1.00,
    "veggie patty": 4.75, "tofu": 4.00
}

# Diet-specific substitutions
diet_substitutions = {
    "vegan": {
        "beef": {"sub": "Impossible patty", "price_diff": 2.50},
        "chicken": {"sub": "plant-based chicken", "price_diff": 2.00},
        "fish": {"sub": "plant-based fish", "price_diff": 2.25},
        "american cheese": {"sub": "vegan cheese", "price_diff": 1.50},
        "cheddar cheese": {"sub": "vegan cheese", "price_diff": 1.50},
        "mayonnaise": {"sub": "vegan mayo", "price_diff": 0.50},
        "egg": {"sub": "flax egg", "price_diff": 0.25}
    },
    "vegetarian": {
        "beef": {"sub": "veggie patty", "price_diff": 1.75},
        "chicken": {"sub": "tofu", "price_diff": 1.50},
        "fish": {"sub": "veggie patty", "price_diff": 1.75}
    },
    "pescetarian": {
        "beef": {"sub": "fish", "price_diff": 1.00},
        "chicken": {"sub": "fish", "price_diff": 1.25}
    },
    "no-diet": {}  # No substitutions
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

def adjust_diet(item_name, item_details, diet_type, nutrient_focus):
    """Adjust item based on diet and boost specified nutrient"""
    original_ingredients = item_details["ingredients"]
    new_ingredients = original_ingredients.copy()
    price_diff = 0
    changes_made = []
    
    # Apply diet-specific substitutions
    if diet_type in diet_substitutions:
        subs = diet_substitutions[diet_type]
        for i, ingredient in enumerate(new_ingredients):
            if ingredient in subs:
                sub_info = subs[ingredient]
                new_ingredients[i] = sub_info["sub"]
                price_diff += sub_info["price_diff"]
                changes_made.append(f"{ingredient} -> {sub_info['sub']} (+${sub_info['price_diff']:.2f})")
    
    # Add nutrient-boosting ingredient based on focus
    add_ons = {
        "protein": "lentils",
        "fiber": "chia seeds",
        "vitamins": "spinach"
    }
    if nutrient_focus in add_ons:
        add_on = add_ons[nutrient_focus]
        new_ingredients.append(add_on)
        price_diff += nutrition_values[add_on]["price"]
        changes_made.append(f"Added {add_on} for {nutrient_focus} (+${nutrition_values[add_on]['price']:.2f})")
    
    # Calculate nutrition and prices
    original_nutrition = calculate_nutrition(original_ingredients)
    new_nutrition = calculate_nutrition(new_ingredients)
    original_price = calculate_price(original_ingredients)
    new_price = original_price + price_diff
    
    return {
        "original_ingredients": original_ingredients,
        "new_ingredients": new_ingredients,
        "changes": changes_made,
        "original_price": item_details["base_price"],
        "new_price": round(new_price, 2),
        "price_difference": round(new_price - item_details["base_price"], 2),
        "original_nutrition": original_nutrition,
        "new_nutrition": new_nutrition
    }

def display_results(diet_type, nutrient_focus):
    """Display results based on diet and nutrient focus"""
    diet_label = "Original" if diet_type == "no-diet" else diet_type.capitalize()
    print(f"{diet_label} Menu with {nutrient_focus.capitalize()} Focus (March 17, 2025)\n" + "="*50)
    
    for item_name, item_details in menu_items.items():
        result = adjust_diet(item_name, item_details, diet_type, nutrient_focus)
        
        print(f"\nItem: {item_name}")
        print(f"Original Ingredients: {', '.join(result['original_ingredients'])}")
        print(f"{diet_label} Ingredients: {', '.join(result['new_ingredients'])}")
        if result["changes"]:
            print("Changes Made:")
            for change in result["changes"]:
                print(f"  - {change}")
        print(f"Original Price: ${result['original_price']:.2f}")
        print(f"{diet_label} Price: ${result['new_price']:.2f}")
        print(f"Price Difference: ${result['price_difference']:.2f}")
        print("Nutrition Comparison:")
        print(f"  Original - Protein: {result['original_nutrition']['protein']}g, "
              f"Fiber: {result['original_nutrition']['fiber']}g, "
              f"Vitamins: {result['original_nutrition']['vitamins']}mg")
        print(f"  {diet_label} - Protein: {result['new_nutrition']['protein']}g, "
              f"Fiber: {result['new_nutrition']['fiber']}g, "
              f"Vitamins: {result['new_nutrition']['vitamins']}mg")
        print("-"*50)

def get_user_preferences():
    """Prompt user for diet and nutrient focus"""
    valid_diets = ["vegan", "vegetarian", "no-diet", "pescetarian"]
    valid_focus = ["protein", "fiber", "vitamins"]
    
    print("Available diets: vegan, vegetarian, no-diet, pescatarian")
    while True:
        diet = input("Which diet would you like to follow? ").lower().strip()
        if diet in valid_diets:
            break
        print("Invalid diet. Please choose: vegan, vegetarian, no-diet, or pescatarian")
    
    print("\nNutrient focus options: protein, fiber, vitamins")
    while True:
        focus = input("Which nutrient would you like to boost? ").lower().strip()
        if focus in valid_focus:
            break
        print("Invalid choice. Please choose: protein, fiber, or vitamins")
    
    return diet, focus

# Run the program
if __name__ == "__main__":
    diet_type, nutrient_focus = get_user_preferences()
    display_results(diet_type, nutrient_focus)

""" Example output: 
Available diets: vegan, vegetarian, no-diet, pescatarian
Which diet would you like to follow? pescatarian

Nutrient focus options: protein, fiber, vitamins
Which nutrient would you like to boost? protein
Pescatarian Menu with Protein Focus (March 17, 2025)
==================================================

Item: Beef Burger
Original Ingredients: beef, american cheese, lettuce, tomatoes, onions, bun
Pescatarian Ingredients: fish, american cheese, lettuce, tomatoes, onions, bun, lentils
Changes Made:
  - beef -> fish (+$1.00)
  - Added lentils for protein (+$1.00)
Original Price: $7.00
Pescatarian Price: $9.00
Price Difference: $2.00
Nutrition Comparison:
  Original - Protein: 37g, Fiber: 4.5g, Vitamins: 22mg
  Pescatarian - Protein: 40g, Fiber: 12.5g, Vitamins: 25mg
--------------------------------------------------

Item: Chicken Sandwich
Original Ingredients: chicken, mayonnaise, lettuce, tomatoes, bun
Pescatarian Ingredients: fish, mayonnaise, lettuce, tomatoes, bun, lentils
Changes Made:
  - chicken -> fish (+$1.25)
  - Added lentils for protein (+$1.00)
Original Price: $6.50
Pescatarian Price: $8.85
Price Difference: $2.35
Nutrition Comparison:
  Original - Protein: 29g, Fiber: 2.5g, Vitamins: 17mg
  Pescatarian - Protein: 31g, Fiber: 10.5g, Vitamins: 19mg
--------------------------------------------------

Item: Fish Tacos
Original Ingredients: fish, lettuce, tomatoes, tartar sauce
Pescatarian Ingredients: fish, lettuce, tomatoes, tartar sauce, lentils
Changes Made:
  - Added lentils for protein (+$1.00)
Original Price: $8.00
Pescatarian Price: $9.35
Price Difference: $1.35
Nutrition Comparison:
  Original - Protein: 23g, Fiber: 2.5g, Vitamins: 18mg
  Pescatarian - Protein: 32g, Fiber: 10.5g, Vitamins: 21mg
--------------------------------------------------
"""

# Useful for meal building and price planning
# Alert can be received for good price and nutrition
# User diet profiles can be used to set this up