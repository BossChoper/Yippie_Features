# Functional; scan CSV, output restaurantji URLs
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

def generate_restaurantji_url(name, address):
    """Generate Restaurantji URL for a given business name and address."""
    state, city = get_state_and_city(address)
    if not state or not city:
        return None
    cleaned_city = clean_name(city)
    cleaned_name = clean_name(name)
    url = f"https://www.restaurantji.com/{state}/{cleaned_city}/{cleaned_name}-/"
    return url

def generate_urls_for_csv(input_csv_path, output_csv_path):
    """Read CSV, generate URLs for each business, and save to new CSV."""
    try:
        df = pd.read_csv(input_csv_path)
        
        # Check required columns exist
        if 'name' not in df.columns or 'address' not in df.columns:
            raise ValueError("CSV must contain 'name' and 'address' columns.")
        
        # Generate URLs for each row
        df['restaurantji_url'] = df.apply(
            lambda row: generate_restaurantji_url(row['name'], row['address']), axis=1
        )
        
        # Save to new CSV
        df.to_csv(output_csv_path, index=False)
        print(f"New CSV with URLs saved to: {output_csv_path}")
    except FileNotFoundError:
        print("Input CSV file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_csv = "/Users/mkonteh88/Desktop/Yippee_Dev/Yippee_Testing/API_Testing/restaurants.csv"
    output_csv = "/Users/mkonteh88/Desktop/Yippee_Dev/Yippee_Testing/API_Testing/restaurants_with_urls.csv"
    generate_urls_for_csv(input_csv, output_csv)
