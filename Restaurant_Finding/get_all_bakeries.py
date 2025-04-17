# Functional; retrieves all restaurants that are listed as bakeries on google
import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def find_bakeries_in_state(api_key, state_name):
    # Define the base URL for the Google Places Text Search API
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # Define the query to search for bakeries in the given state
    query = f"bakeries in {state_name}"
    
    # Set up parameters for the API request
    params = {
        "query": query,
        "key": api_key,
    }
    
    # Initialize variables for pagination
    bakeries = []
    next_page_token = None
    
    while True:
        if next_page_token:
            params["pagetoken"] = next_page_token
        
        # Make the API request
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Check if the request was successful
        if data.get("status") != "OK":
            print(f"Error: {data.get('status')}")
            break
        
        # Extract bakery names and add them to the list
        for result in data.get("results", []):
            bakeries.append(result.get("name"))
        
        # Check if there's a next page of results
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break
    
    return bakeries

# Replace 'YOUR_API_KEY' with your actual Google Cloud API key
api_key = os.getenv('GOOGLE_MAPS_API_KEY')
state_name = input("Enter the state name: ")

# Call the function and list all bakeries
bakeries = find_bakeries_in_state(api_key, state_name)
print(f"\nBakeries in {state_name}:")
for bakery in bakeries:
    print(f"- {bakery}")


""" Example output:
python get_all_bakeries.py 
Enter the state name: Maryland
Error: INVALID_REQUEST

Bakeries in Maryland:
- B. Sweet Cakes, LLC
- Mouth Full of Crumbs
- Black Market Bakers Edgewater
- Annie Bakery
- Icing On The Cake Maryland
- Dulce vida bakery
- Love & Flour Bakery Panaderia
- Sweet Tooth Cafe & Cakes
- Sugar Butter Love
- Angyono Custom Cakes
- Casa Blanca Bakery
- EdniscoCreamyCreations
- Pure Sweet Indulgence Bakery and Cafe
- Sunday Morning Bakehouse
- San Carlos Bakery
- The Dessert Junkie
- Mi Pueblito Bakery
- Heavens Bakery Inc
- Mirabeau
- Sugar Vault Desserts & Bakery
(base) mkonteh88@8042388ntehsAir Restaurant_Finding % python get_all_bakeries.py 
Enter the state name: Washington DC
Error: INVALID_REQUEST

Bakeries in Washington DC:
- Baked & Wired
- Levain Bakery – Georgetown, D.C.
- Bread Furst
- Un je ne sais Quoi...
- Sharbat Bakery&Cafe
- Boulangerie Christophe
- The CakeRoom
- SEYLOU LLC
- DC Sweet Potato Cake Bakery & Cafe
- Rise Bakery
- Pluma by Bluebird Bakery
- Tatte Bakery & Cafe | Dupont Circle
- Bake Peace with Timmy
- A Baked Joint
- Fresh Baguette Georgetown
- Souk
- Tatte Bakery & Cafe | West End
- Sticky Fingers Sweets & Eats
- Baked by Yael
- Bread Alley
"""