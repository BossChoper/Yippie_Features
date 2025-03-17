import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Load API key from .env
load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")

# Yelp API endpoint
BASE_URL = "https://api.yelp.com/v3/businesses"
HEADERS = {"Authorization": f"Bearer {YELP_API_KEY}"}

def fetch_business_id(item_name: str, location: str = "San Francisco, CA") -> str:
    """Fetch a business ID for a restaurant likely to have the menu item."""
    search_url = f"{BASE_URL}/search"
    params = {
        "term": f"{item_name} restaurant",  # e.g., "Burger restaurant"
        "location": location,
        "limit": 1  # Get the top result
    }
    
    try:
        response = requests.get(search_url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch business: Status {response.status_code}")
            return None
        
        data = response.json()
        businesses = data.get("businesses", [])
        if not businesses:
            print(f"No businesses found for {item_name}")
            return None
        
        return businesses[0]["id"]
    except Exception as e:
        print(f"Error fetching business ID: {e}")
        return None

def fetch_reviews(business_id: str) -> list:
    """Fetch reviews for a given business ID from Yelp."""
    reviews_url = f"{BASE_URL}/{business_id}/reviews"
    params = {"limit": 3}  # Yelp API limits to 3 reviews max
    
    try:
        response = requests.get(reviews_url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch reviews: Status {response.status_code}")
            return []
        
        data = response.json()
        return data.get("reviews", [])
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return []

def analyze_reviews(reviews: list) -> str:
    """Simulate AI-generated assumption based on review text."""
    if not reviews:
        return "No assumptions available due to lack of reviews."
    
    # Combine all review text into one string
    all_text = " ".join(review["text"].lower() for review in reviews)
    
    # Count common keywords (simple frequency analysis)
    keywords = ["spicy", "sweet", "salty", "greasy", "delicious"]
    word_counts = Counter(all_text.split())
    
    # Find the most frequent relevant keyword
    relevant_counts = {kw: word_counts.get(kw, 0) for kw in keywords}
    if not any(relevant_counts.values()):
        return "No strong trends detected in reviews."
    
    most_common = max(relevant_counts.items(), key=lambda x: x[1])
    keyword, count = most_common
    
    if count >= 2:  # Arbitrary threshold for "often"
        return f"This item is known to be {keyword}."
    elif count == 1:
        return f"This item might be {keyword}."
    return "No strong trends detected in reviews."

def print_reviews_and_assumption(item_name: str, reviews: list, assumption: str):
    """Print reviews and AI-generated assumption."""
    print(f"\nReviews for '{item_name}':")
    if not reviews:
        print("  No reviews found.")
    else:
        for i, review in enumerate(reviews, 1):
            print(f"  Review {i}:")
            print(f"    Rating: {review['rating']}/5")
            print(f"    Text: {review['text']}")
            print(f"    Source: {review['url']}")
            print()
    
    print(f"AI-Generated Assumption: {assumption}")

def main():
    """Run the Reviews Program."""
    print("Starting Reviews Program...")
    item_name = "Burger"  # Could be made interactive with input()
    
    # Fetch business ID and reviews
    business_id = fetch_business_id(item_name)
    if not business_id:
        return
    
    reviews = fetch_reviews(business_id)
    if not reviews:
        print("No reviews retrieved.")
        return
    
    # Analyze and print
    assumption = analyze_reviews(reviews)
    print_reviews_and_assumption(item_name, reviews, assumption)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Reviews Program...

Reviews for 'Burger':
  Review 1:
    Rating: 4/5
    Text: The burger was delicious and really spicy!
    Source: https://www.yelp.com/biz/xyz/review/123

  Review 2:
    Rating: 5/5
    Text: Best spicy burger in town.
    Source: https://www.yelp.com/biz/xyz/review/456

  Review 3:
    Rating: 3/5
    Text: Decent, but too spicy for me.
    Source: https://www.yelp.com/biz/xyz/review/789

AI-Generated Assumption: This item is known to be spicy.
\\
"""

# Review poolings