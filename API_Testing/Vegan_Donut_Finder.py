# Functional; works to find nearby vegan donuts baed on yelp location data. Good for finding cuisines.
# Sorta works. Only finds few places. Also takes coordinates or location name
# Favorite
import requests
import json
import os
import time
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
import re

# Load environment variables from .env file to access API keys securely
load_dotenv()

class VeganDonutFinder:
    def __init__(self):
        # Initialize the finder with API credentials and setup
        self.api_key = os.getenv("YELP_API_KEY")
        if not self.api_key:
            raise ValueError("YELP_API_KEY environment variable not set")
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json"
        }
        # Base URL for all Yelp API endpoints
        self.base_url = "https://api.yelp.com/v3"
        # Initialize geocoder for converting addresses to coordinates
        self.geolocator = Nominatim(user_agent="vegan_donut_finder")
    
    def get_user_location(self):
        """
        Gets the user's location either by address or coordinates
        Returns a dictionary with location data that can be used in API requests
        """
        choice = input("How would you like to specify your location?\n1. Enter an address\n2. Use coordinates\nEnter choice (1 or 2): ")
        
        if choice == "1":
            # Get location by address
            address = input("Enter your address or city: ")
            try:
                # Convert address to coordinates using geocoding
                location = self.geolocator.geocode(address)
                if location:
                    # Return both coordinates and original address if geocoding succeeds
                    return {"latitude": location.latitude, "longitude": location.longitude, "address": address}
                else:
                    # Fall back to just using the address text if geocoding fails
                    print("Couldn't find that location. Using address as text.")
                    return {"address": address}
            except Exception as e:
                # Handle any geocoding errors
                print(f"Error with geocoding: {e}. Using address as text.")
                return {"address": address}
        elif choice == "2":
            # Get location by exact coordinates
            latitude = input("Enter latitude: ")
            longitude = input("Enter longitude: ")
            try:
                # Convert string inputs to floats for the API
                return {"latitude": float(latitude), "longitude": float(longitude)}
            except ValueError:
                # Exit if invalid coordinates are provided
                print("Invalid coordinates. Please run the program again.")
                exit(1)
        else:
            # Default to address input if invalid choice
            print("Invalid choice. Using text input.")
            address = input("Enter your address or city: ")
            return {"address": address}
    
    def search_vegan_donuts(self, location_data, radius=16000, limit=20):
        """
        Searches for donut places that might have vegan options near the given location
        
        Parameters:
        - location_data: Dictionary with either coordinates or address
        - radius: Search radius in meters (default is ~10 miles)
        - limit: Maximum number of results to return
        
        Returns a list of business data from Yelp API
        """
        endpoint = f"{self.base_url}/businesses/search"
        
        # Build query parameters for the search
        params = {
            "term": "vegan donuts",  # Search term combining both requirements
            "limit": limit,
            "radius": radius,  # 16000 meters = about 10 miles
            "categories": "donuts,bakeries,vegan"  # Filter by relevant categories
        }
        
        # Add appropriate location parameter based on what data we have
        if "latitude" in location_data and "longitude" in location_data:
            # Use coordinates if available (more precise)
            params["latitude"] = location_data["latitude"]
            params["longitude"] = location_data["longitude"]
        elif "address" in location_data:
            # Otherwise use text address
            params["location"] = location_data["address"]
        
        # Make the API request
        response = requests.get(endpoint, headers=self.headers, params=params)
        if response.status_code != 200:
            # Handle API errors
            print(f"Error searching for vegan donuts: {response.status_code}")
            print(response.text)
            return []
        
        # Return the list of businesses from the response
        return response.json().get("businesses", [])
    
    def get_business_details(self, business_id):
        """
        Gets detailed information about a specific business
        
        Parameters:
        - business_id: Yelp's business ID
        
        Returns detailed business data or None if request fails
        """
        endpoint = f"{self.base_url}/businesses/{business_id}"
        
        try:
            # Request detailed business information
            response = requests.get(endpoint, headers=self.headers)
            
            if response.status_code == 429:  # Rate limit hit
                print("Rate limit reached. Waiting before retrying...")
                time.sleep(1)  # Wait for 1 second before retry
                response = requests.get(endpoint, headers=self.headers)
                
            if response.status_code == 404:
                print(f"Business {business_id} not found in Yelp database")
                return None
                
            if response.status_code != 200:
                print(f"Error getting business details: {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching business details: {str(e)}")
            return None
    
    def get_reviews(self, business_id, limit=3):
        """
        Gets reviews for a business to analyze for vegan donut mentions
        
        Parameters:
        - business_id: Yelp's business ID
        - limit: Maximum number of reviews to return
        
        Returns a list of review data
        """
        endpoint = f"{self.base_url}/businesses/{business_id}/reviews"
        params = {
            "limit": limit,
            "sort_by": "relevance"  # Get most relevant reviews first
        }
        
        # Add required locale header for reviews endpoint
        headers = self.headers.copy()
        headers["Accept-Language"] = "en_US"
        
        # Request reviews with proper headers
        response = requests.get(endpoint, headers=headers, params=params)
        
        if response.status_code == 429:  # Rate limit hit
            print("Rate limit reached. Waiting before retrying...")
            time.sleep(1)  # Wait for 1 second before retry
            response = requests.get(endpoint, headers=headers, params=params)
            
        if response.status_code != 200:
            print(f"Error getting reviews: {response.status_code}")
            print(f"Response: {response.text}")
            return []
        
        return response.json().get("reviews", [])
    
    def analyze_for_vegan_donuts(self, business, reviews):
        """
        Analyzes business details and reviews to determine likelihood of vegan donut offerings
        
        Parameters:
        - business: Business data dictionary from Yelp API
        - reviews: List of review data dictionaries
        
        Returns analysis results with confidence scores and relevant mentions
        """
        # Initialize scoring system
        vegan_score = 0
        donut_score = 0
        vegan_donut_explicit = False
        vegan_donut_mentions = []
        
        # ANALYSIS 1: Business name analysis
        name = business.get("name", "").lower()
        if "vegan" in name and ("donut" in name or "doughnut" in name):
            # Business name explicitly mentions vegan donuts - strong indicator
            vegan_donut_explicit = True
            vegan_score += 5
            donut_score += 5
        elif "vegan" in name:
            # Business name mentions vegan - moderate indicator
            vegan_score += 3
        elif "donut" in name or "doughnut" in name:
            # Business name mentions donuts - moderate indicator
            donut_score += 3
        
        # ANALYSIS 2: Categories analysis
        for category in business.get("categories", []):
            category_title = category.get("title", "").lower()
            if category_title == "vegan":
                # Business is categorized as vegan - strong indicator
                vegan_score += 3
            elif category_title == "donuts" or category_title == "doughnuts":
                # Business is categorized as donut shop - strong indicator
                donut_score += 3
            elif "bakeries" in category_title:
                # Business is a bakery - weak indicator for donuts
                donut_score += 1
        
        # ANALYSIS 3: Review analysis using regex patterns
        # Define patterns to look for explicit mentions of vegan donuts
        vegan_donut_patterns = [
            r"vegan (donut|doughnut)",
            r"plant.?based (donut|doughnut)",
            r"dairy.?free (donut|doughnut)",
            r"(donut|doughnut).*vegan",
            r"(donut|doughnut).*plant.?based",
            r"(donut|doughnut).*dairy.?free"
        ]
        
        # Analyze each review for relevant mentions
        for review in reviews:
            review_text = review.get("text", "").lower()
            
            # Check for general vegan mentions
            if "vegan" in review_text:
                vegan_score += 1
            
            # Check for general donut mentions
            if "donut" in review_text or "doughnut" in review_text:
                donut_score += 1
            
            # Check for explicit mentions of vegan donuts using regex patterns
            for pattern in vegan_donut_patterns:
                matches = re.findall(pattern, review_text)
                if matches:
                    # Found explicit mention - strongest indicator
                    vegan_donut_explicit = True
                    # Extract context around the match to show user
                    for match in matches:
                        # Find the position of the match in the review
                        match_pos = review_text.find(match)
                        # Extract text before and after the match for context
                        start = max(0, match_pos - 40)
                        end = min(len(review_text), match_pos + len(match) + 40)
                        # Highlight the match within the context
                        context = review_text[start:end].replace(match, f"**{match}**")
                        vegan_donut_mentions.append(f"...{context}...")
        
        # Determine confidence level based on scores and explicit mentions
        return {
            "vegan_score": vegan_score,
            "donut_score": donut_score,
            "vegan_donut_explicit": vegan_donut_explicit,
            "vegan_donut_mentions": vegan_donut_mentions,
            "confidence": "high" if vegan_donut_explicit else ("medium" if vegan_score >= 2 and donut_score >= 2 else "low")
        }
    
    def save_results(self, results, filename="vegan_donut_results.json"):
        """
        Saves the analysis results to a JSON file for later reference
        
        Parameters:
        - results: List of analyzed business data
        - filename: Output file name
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")

def main():
    """Main function that orchestrates the vegan donut finding process"""
    print("===== Vegan Donut Finder =====")
    print("This program helps you find restaurants that offer vegan donuts in your area.")
    
    try:
        # Initialize the finder
        finder = VeganDonutFinder()
        
        # STEP 1: Get the user's location
        location_data = finder.get_user_location()
        
        # STEP 2: Get desired search radius
        radius_input = input("Search radius in miles (default: 10): ")
        # Convert miles to meters for the API
        radius = int(float(radius_input) * 1609.34) if radius_input else 16000
        
        # STEP 3: Search for potential matches
        print("\nSearching for vegan donut options near you...")
        businesses = finder.search_vegan_donuts(location_data, radius)
        
        # Check if any results were found
        if not businesses:
            print("No results found. Try expanding your search radius or using different search terms.")
            return
            
        print(f"Found {len(businesses)} potential places. Analyzing results...")
        
        # STEP 4: Analyze each business for vegan donut indicators
        results = []
        for i, business in enumerate(businesses):
            print(f"Analyzing {i+1}/{len(businesses)}: {business.get('name')}")
            
            # Get additional business details
            business_id = business.get("id")
            if not business_id:
                print(f"Skipping {business.get('name')} - no business ID found")
                continue

            details = finder.get_business_details(business_id)
            if not details:
                print(f"Skipping {business.get('name')} - could not fetch business details")
                continue
                
            # Get reviews to analyze text content
            try:
                reviews = finder.get_reviews(business_id)
                if not reviews:
                    print(f"Note: No reviews found for {business.get('name')}")
            except Exception as e:
                print(f"Warning: Could not fetch reviews for {business.get('name')}: {str(e)}")
                reviews = []  # Continue analysis with empty reviews
            
            # Analyze all data for vegan donut indicators
            analysis = finder.analyze_for_vegan_donuts(business, reviews)
            
            # Add to results if likely to have vegan donuts (filter out low confidence with no explicit mentions)
            if analysis["vegan_donut_explicit"] or analysis["confidence"] != "low":
                results.append({
                    "name": business.get("name"),
                    "rating": business.get("rating"),
                    "price": business.get("price", "unknown"),
                    "address": ", ".join(business.get("location", {}).get("display_address", [])),
                    "phone": business.get("phone"),
                    "url": business.get("url"),
                    "image_url": business.get("image_url"),
                    "is_closed": business.get("is_closed", False),
                    "distance": f"{business.get('distance', 0) / 1609.34:.1f} miles",
                    "analysis": analysis
                })
            
            # Respect API rate limits by adding a delay between requests
            time.sleep(0.5)
        
        # STEP 5: Sort results by confidence level
        # Order: explicit mentions first, then medium confidence, then low confidence
        results.sort(key=lambda x: 0 if x["analysis"]["vegan_donut_explicit"] else 
                                    (1 if x["analysis"]["confidence"] == "medium" else 2))
        
        # STEP 6: Display results to user
        if not results:
            print("\nNo places with vegan donuts found. Try expanding your search.")
        else:
            print(f"\nFound {len(results)} places likely to have vegan donuts!")
            print("\n===== RESULTS =====")
            
            # Format and display each result
            for i, result in enumerate(results):
                # Show confidence level using symbols
                confidence = "✓ Confirmed" if result["analysis"]["vegan_donut_explicit"] else f"⚖ {result['analysis']['confidence'].title()} confidence"
                print(f"\n{i+1}. {result['name']} ({confidence})")
                print(f"   Rating: {result['rating']} stars | Price: {result['price']} | Distance: {result['distance']}")
                print(f"   Address: {result['address']}")
                
                # Show review quotes mentioning vegan donuts if available
                if result["analysis"]["vegan_donut_mentions"]:
                    print("   Review mentions:")
                    for mention in result["analysis"]["vegan_donut_mentions"][:2]:  # Show at most 2 mentions
                        print(f"   \"{mention}\"")
            
            # STEP 7: Save results to file for later reference
            finder.save_results(results)
            print("\nResults saved to vegan_donut_results.json")
            
    except Exception as e:
        # Handle any unexpected errors
        print(f"An error occurred: {str(e)}")

# Program entry point
if __name__ == "__main__":
    main()

"""
Found 1 places likely to have vegan donuts!

===== RESULTS =====

1. Donut Farm (⚖ Medium confidence)
   Rating: 4.0 stars | Price: $ | Distance: 9.4 miles
   Address: 3278 Adeline St, Berkeley, CA 94703
Results saved to vegan_donut_results.json

"""
# Uses Yelp to find restaurants with a dietary specific food
# BARELY-FUNCTIONAL

""" Example output:
===== Vegan Donut Finder =====
This program helps you find restaurants that offer vegan donuts in your area.
How would you like to specify your location?
1. Enter an address
2. Use coordinates
Enter choice (1 or 2): 1
Enter your address or city: Washington DC
Search radius in miles (default: 10): 

Searching for vegan donut options near you...
Found 20 potential places. Analyzing results...
Analyzing 1/20: Donut Run
Error getting reviews: 404
Response: {"error": {"code": "NOT_FOUND", "description": "Resource could not be found."}}
Note: No reviews found for Donut Run
Analyzing 2/20: Astro Doughnuts & Fried Chicken
Error getting reviews: 404
Response: {"error": {"code": "NOT_FOUND", "description": "Resource could not be found."}}
Note: No reviews found for Astro Doughnuts & Fried Chicken
Analyzing 3/20: Just Fine Donuts
"""

# Useful for dietary restaurant finding
# Uses review scores to determine restaurant relevancy
# Relevancy scores: vegan score, donut score, location
