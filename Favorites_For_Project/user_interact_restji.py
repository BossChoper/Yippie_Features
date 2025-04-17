# Functional; gives user input to provide a csv and get back a csv with restaurantJi urls
# Menu Scraping
import pandas as pd
import re
import os
import requests

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

def check_url_exists(url):
    """Check if a URL exists by sending a HEAD request."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_csv(input_csv_path, output_csv_path):
    """Read CSV, generate URLs, check existence, and save new CSV."""
    if not os.path.exists(input_csv_path):
        print("CSV file not found at the provided path.")
        return
    try:
        df = pd.read_csv(input_csv_path)
        if 'name' not in df.columns or 'address' not in df.columns:
            print("CSV must contain 'name' and 'address' columns.")
            return
        # Generate URLs and check if they exist
        urls = []
        url_status = []
        for _, row in df.iterrows():
            url = generate_restaurantji_url(row['name'], row['address'])
            urls.append(url if url else "")
            exists = check_url_exists(url) if url else False
            url_status.append("Exists" if exists else "Not Found")
        df['restaurantji_url'] = urls
        df['url_status'] = url_status
        df.to_csv(output_csv_path, index=False)
        print(f"Processed CSV saved to: {output_csv_path}")
    except Exception as e:
        print(f"An error occurred while processing CSV: {e}")

def manual_entry():
    """Allow user to manually enter restaurant name and address, generate URL and check existence."""
    name = input("Enter the restaurant name: ").strip()
    address = input("Enter the restaurant address (e.g. '6904 4th St NW, Washington, DC 20012, USA'): ").strip()
    url = generate_restaurantji_url(name, address)
    if not url:
        print("Could not generate URL from the given address.")
        return
    print(f"Generated URL: {url}")
    exists = check_url_exists(url)
    print("URL exists on server." if exists else "URL does NOT exist on server.")

def main():
    print("Choose an option:")
    print("1. Upload CSV file to generate URLs for all restaurants")
    print("2. Manually enter a restaurant name and address")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        csv_path = input("Enter full path to the CSV file: ").strip()
        output_path = input("Enter full path for the output CSV file: ").strip()
        process_csv(csv_path, output_path)
    elif choice == '2':
        manual_entry()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
