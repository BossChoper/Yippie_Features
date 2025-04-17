# Functional; creates URLs to get RestaurantJi pages
import pandas as pd
import re

def clean_name(name):
    """Clean business name or city for URL formatting."""
    cleaned = re.sub(r'[^\w\s-]', '', name).strip()
    cleaned = re.sub(r'\s+', '-', cleaned).lower()
    return cleaned

def get_state_and_city(address):
    """Extract state and city from address, ignoring zip code and country."""
    parts = [p.strip() for p in address.split(',')]
    if len(parts) >= 3:
        city = parts[1]  # second part is city
        state_zip = parts[2].split()  # third part contains state and zip
        if state_zip:
            state = state_zip[0]  # first word is state abbreviation
            return state.lower(), city.lower()
    return None, None

def generate_restaurantji_menu_url(business_name, csv_file="/Users/mkonteh88/Desktop/Yippee_Dev/Yippee_Testing/API_Testing/restaurants.csv"):
    """Generate Restaurantji menu URL for a given business name."""
    try:
        df = pd.read_csv(csv_file)
        business = df[df['name'].str.lower() == business_name.lower()]
        if business.empty:
            return f"Business '{business_name}' not found in the dataset."
        business = business.iloc[0]
        address = business['address']
        name = business['name']
        state, city = get_state_and_city(address)
        if not state or not city:
            return "Could not extract state or city from address."
        cleaned_city = clean_name(city)
        cleaned_name = clean_name(name)
        url = f"https://www.restaurantji.com/{state}/{cleaned_city}/{cleaned_name}-/menu/"
        return url
    except FileNotFoundError:
        return "CSV file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    test_names = [
        "Donut Run",
        "Dodah's Kitchen",
        "Red Velvet Cupcakery"
    ]
    for name in test_names:
        print(f"Business: {name}")
        print(f"Menu URL: {generate_restaurantji_menu_url(name)}\n")

""" Example output: 
python ji_search.py 
Business: Donut Run
Menu URL: https://www.restaurantji.com/dc/washington/donut-run-/menu/

Business: Dodah's Kitchen
Menu URL: https://www.restaurantji.com/md/mt-rainier/dodahs-kitchen-/menu/

Business: Red Velvet Cupcakery
Menu URL: https://www.restaurantji.com/dc/washington/red-velvet-cupcakery-/menu/
"""