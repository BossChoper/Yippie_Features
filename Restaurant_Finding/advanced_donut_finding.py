# NonFunctional
from googleplaces import GooglePlaces, types
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # Replace with your Google Places API key
google_places = GooglePlaces(API_KEY)

# Define search parameters
location = 'New York, USA'  # Replace with your target location
radius = 5000  # Search radius in meters
keywords = ['donut', 'donuts']  # Keywords to search for
place_types = [types.TYPE_BAKERY, types.TYPE_CAFE, types.TYPE_RESTAURANT]  # Relevant place types

# Perform the search
results = []
for place_type in place_types:
    query_result = google_places.nearby_search(
        location=location,
        radius=radius,
        types=[place_type],
        keyword=' OR '.join(keywords)  # Search for any of the keywords
    )
    
    for place in query_result.places:
        place.get_details()  # Fetch additional details
        results.append({
            'Name': place.name,
            'Address': place.formatted_address,
            'Rating': place.rating,
            'Type': place_type,
            'Website': place.website
        })

# Convert results to a DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv('donut_shops.csv', index=False)
print(f"Found {len(df)} donut-serving establishments. Saved to 'donut_shops.csv'.")
