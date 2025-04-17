# NonFunctional; uses Google API to search for restaurants using specific terms within google reviews
import os
import json
import re
import pandas as pd
import requests
from collections import defaultdict
from datetime import datetime

# Configuration
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your actual API key
SEARCH_TERMS = ["vegan", "plant-based", "dairy-free", "egg-free", "plant based"]
LOCATION = "37.7749,-122.4194"  # Default location (San Francisco)
RADIUS = 5000  # Search radius in meters
MIN_VEGAN_SCORE = 1  # Minimum vegan mentions to be included in results

def search_bakeries(location, radius):
    """Search for bakeries in the given location and radius"""
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": location,
        "radius": radius,
        "type": "bakery",
        "key": API_KEY
    }
    
    bakeries = []
    next_page_token = None
    
    # Google Maps API paginates results, so we need to make multiple requests
    while True:
        if next_page_token:
            params["pagetoken"] = next_page_token
            
        response = requests.get(endpoint_url, params=params)
        results = response.json()
        
        if "results" in results:
            bakeries.extend(results["results"])
            
        next_page_token = results.get("next_page_token")
        
        if not next_page_token:
            break
            
        # Google requires a delay between pagetoken requests
        import time
        time.sleep(2)
    
    return bakeries

def get_place_details(place_id):
    """Get detailed information about a place, including reviews"""
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        "place_id": place_id,
        "fields": "name,rating,formatted_address,review,website,url",
        "key": API_KEY
    }
    
    response = requests.get(endpoint_url, params=params)
    return response.json()["result"]

def analyze_reviews(reviews, search_terms):
    """Analyze reviews for mentions of vegan-related terms"""
    vegan_mentions = []
    vegan_score = 0
    
    for review in reviews:
        review_text = review.get("text", "").lower()
        
        # Find all matches of search terms
        matches = []
        for term in search_terms:
            # Use word boundaries to find whole words only
            pattern = r'\b{}\b'.format(re.escape(term))
            term_matches = re.findall(pattern, review_text)
            matches.extend(term_matches)
        
        if matches:
            vegan_score += len(matches)
            vegan_mentions.append({
                "review_text": review.get("text"),
                "author": review.get("author_name"),
                "rating": review.get("rating"),
                "time": datetime.fromtimestamp(review.get("time")).strftime('%Y-%m-%d'),
                "matches": matches
            })
    
    return {
        "vegan_score": vegan_score,
        "mentions": vegan_mentions
    }

def find_vegan_bakeries(location=LOCATION, radius=RADIUS):
    """Main function to find and score bakeries for vegan options"""
    print(f"Searching for bakeries within {radius}m of {location}...")
    
    # Search for bakeries
    bakeries = search_bakeries(location, radius)
    print(f"Found {len(bakeries)} bakeries. Analyzing reviews...")
    
    # Store results
    results = []
    
    # Process each bakery
    for bakery in bakeries:
        place_id = bakery["place_id"]
        
        # Get detailed information including reviews
        details = get_place_details(place_id)
        reviews = details.get("reviews", [])
        
        if not reviews:
            continue
        
        # Analyze reviews for vegan mentions
        analysis = analyze_reviews(reviews, SEARCH_TERMS)
        
        # Only include bakeries with vegan mentions
        if analysis["vegan_score"] >= MIN_VEGAN_SCORE:
            results.append({
                "name": details.get("name", "Unknown"),
                "address": details.get("formatted_address", "Unknown"),
                "rating": details.get("rating", "N/A"),
                "google_maps_url": details.get("url", ""),
                "website": details.get("website", ""),
                "vegan_score": analysis["vegan_score"],
                "vegan_mentions": analysis["mentions"]
            })
    
    # Sort results by vegan score (highest first)
    results.sort(key=lambda x: x["vegan_score"], reverse=True)
    
    return results

def save_results(results, filename="vegan_bakeries_results.json"):
    """Save results to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"Results saved to {filename}")
    
    # Also create a CSV with basic info
    df = pd.DataFrame([{
        "Name": r["name"],
        "Address": r["address"],
        "Rating": r["rating"],
        "Vegan Score": r["vegan_score"],
        "Google Maps URL": r["google_maps_url"],
        "Website": r["website"]
    } for r in results])
    
    csv_filename = filename.replace(".json", ".csv")
    df.to_csv(csv_filename, index=False)
    print(f"Summary saved to {csv_filename}")

def main():
    """Main function to run the script"""
    # Get user input for location
    use_default = input(f"Use default location (San Francisco)? (y/n): ")
    
    if use_default.lower() != 'y':
        city = input("Enter city name or coordinates (lat,lng): ")
        if ',' in city and all(c.replace('.', '', 1).replace('-', '', 1).isdigit() for c in city.split(',')):
            location = city  # User entered coordinates
        else:
            # Convert city name to coordinates using geocoding API
            geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={API_KEY}"
            response = requests.get(geocode_url)
            result = response.json()
            
            if result["status"] == "OK":
                lat = result["results"][0]["geometry"]["location"]["lat"]
                lng = result["results"][0]["geometry"]["location"]["lng"]
                location = f"{lat},{lng}"
            else:
                print("Could not geocode the city. Using default location.")
                location = LOCATION
    else:
        location = LOCATION
    
    # Get radius
    radius_input = input(f"Enter search radius in meters (default: {RADIUS}): ")
    radius = int(radius_input) if radius_input.isdigit() else RADIUS
    
    # Run the search
    results = find_vegan_bakeries(location, radius)
    
    # Display summary
    print(f"\nFound {len(results)} bakeries with vegan options:")
    for i, bakery in enumerate(results[:10], 1):  # Show top 10
        print(f"{i}. {bakery['name']} - Vegan Score: {bakery['vegan_score']} - {bakery['address']}")
    
    if len(results) > 10:
        print(f"...and {len(results) - 10} more.")
    
    # Save results
    save_results(results)

if __name__ == "__main__":
    main()