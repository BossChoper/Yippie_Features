# Dictionary of ingredient substitutions by diet type
# Switches meal builds for diets only; provides pricing differences and add-ons/substitutes
# Good one
substitutions = {
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
    }
}

# Base prices for ingredients (in dollars)
base_prices = {
    "beef": 3.00,
    "chicken": 2.50,
    "fish": 3.25,
    "american cheese": 1.00,
    "cheddar cheese": 1.00,
    "mayonnaise": 0.50,
    "egg": 0.75,
    "lettuce": 0.50,
    "tomatoes": 0.60,
    "onions": 0.40,
    "bun": 1.00,
    "pickles": 0.30,
    "ketchup": 0.20,
    "mustard": 0.20,
    "avocado": 1.50,
    "tartar sauce": 0.60
}

# Expanded menu items
menu_items = {
    "Beef Burger": {
        "ingredients": ["beef", "american cheese", "lettuce", "tomatoes", "onions", "bun"],
        "base_price": 7.00
    },
    "Chicken Sandwich": {
        "ingredients": ["chicken", "mayonnaise", "lettuce", "tomatoes", "bun"],
        "base_price": 6.50
    },
    "Breakfast Burger": {
        "ingredients": ["beef", "cheddar cheese", "egg", "bun", "ketchup"],
        "base_price": 7.50
    },
    "Fish Tacos": {
        "ingredients": ["fish", "lettuce", "tomatoes", "tartar sauce"],
        "base_price": 8.00
    },
    "Avocado Chicken Wrap": {
        "ingredients": ["chicken", "avocado", "lettuce", "tomatoes", "mayonnaise"],
        "base_price": 7.75
    }
}

def calculate_original_price(ingredients):
    """Calculate total price based on individual ingredient prices"""
    total = 0
    for ingredient in ingredients:
        total += base_prices.get(ingredient, 0)
    return round(total, 2)

def convert_diet(item_name, item_details, diet_type):
    """Convert item to specified diet and calculate price differences"""
    if diet_type not in substitutions:
        return None
    
    original_ingredients = item_details["ingredients"]
    new_ingredients = original_ingredients.copy()
    price_diff = 0
    substitutions_made = []
    
    diet_subs = substitutions[diet_type]
    
    for i, ingredient in enumerate(new_ingredients):
        if ingredient in diet_subs:
            sub_info = diet_subs[ingredient]
            new_ingredients[i] = sub_info["sub"]
            price_diff += sub_info["price_diff"]
            substitutions_made.append(f"{ingredient} -> {sub_info['sub']} (+${sub_info['price_diff']:.2f})")
    
    original_calc_price = calculate_original_price(original_ingredients)
    new_price = original_calc_price + price_diff
    
    return {
        "original_ingredients": original_ingredients,
        "new_ingredients": new_ingredients,
        "substitutions": substitutions_made,
        "original_price": item_details["base_price"],
        "new_price": round(new_price, 2),
        "price_difference": round(new_price - item_details["base_price"], 2),
        "calculated_original": original_calc_price
    }

def display_results(diet_type):
    """Display conversion results for all menu items based on chosen diet"""
    print(f"{diet_type.capitalize()} Conversion Results (March 17, 2025)\n" + "="*40)
    
    for item_name, item_details in menu_items.items():
        result = convert_diet(item_name, item_details, diet_type)
        if not result:
            print(f"Invalid diet type: {diet_type}")
            return
        
        print(f"\nItem: {item_name}")
        print(f"Original Ingredients: {', '.join(result['original_ingredients'])}")
        print(f"{diet_type.capitalize()} Ingredients: {', '.join(result['new_ingredients'])}")
        if result["substitutions"]:
            print("Substitutions Made:")
            for sub in result["substitutions"]:
                print(f"  - {sub}")
        print(f"Original Menu Price: ${result['original_price']:.2f}")
        print(f"Calculated Ingredient Price: ${result['calculated_original']:.2f}")
        print(f"{diet_type.capitalize()} Price: ${result['new_price']:.2f}")
        print(f"Price Difference: ${result['price_difference']:.2f}")
        print("-"*40)

def get_user_diet():
    """Prompt user for diet preference"""
    valid_diets = ["vegan", "vegetarian", "pescetarian"]
    print("Available diets: vegan, vegetarian, pescetarian")
    while True:
        diet = input("Which diet would you like to convert the menu to? ").lower().strip()
        if diet in valid_diets:
            return diet
        print("Invalid diet. Please choose: vegan, vegetarian, or pescetarian")

# Run the program
if __name__ == "__main__":
    chosen_diet = get_user_diet()
    display_results(chosen_diet)

# Substituion for basic diet consumption (no nutrition)