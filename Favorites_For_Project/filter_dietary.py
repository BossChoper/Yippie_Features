# Functional; creates a "vegan" score to help find vegan food in a series of reviews
import json
import re
import pandas as pd
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
SEARCH_TERMS = ["vegan", "plant-based", "dairy-free", "egg-free", "plant based"]
MIN_VEGAN_SCORE = 1  # Minimum vegan mentions to be included in results

# Mock Data Generation
def generate_mock_reviews(bakery_name, num_reviews=15, vegan_probability=0.3):
    """Generate mock reviews for a bakery"""
    reviews = []
    
    # Sample review templates
    general_templates = [
        "The {item} at {bakery} was {quality}. {additional}",
        "Visited {bakery} yesterday and tried their {item}. {quality} experience overall.",
        "I've been to {bakery} multiple times, and their {item} is always {quality}.",
        "If you're in the area, {bakery} is {recommendation}. {additional}",
        "{bakery} has a {atmosphere} atmosphere and the {item} is {quality}."
    ]
    
    vegan_templates = [
        "As a vegan, I was delighted to find that {bakery} offers {vegan_item}.",
        "The {vegan_item} at {bakery} is perfect for those looking for plant-based options.",
        "Finally a bakery with good dairy-free options! Their {vegan_item} is {quality}.",
        "Great egg-free {vegan_item} at {bakery}. Perfect for my dietary restrictions.",
        "Love that {bakery} has plant based options. The {vegan_item} was {quality}.",
        "I'm always looking for vegan treats and {bakery} did not disappoint with their {vegan_item}.",
        "Their {vegan_item} is vegan and tastes {quality} - even my non-vegan friends enjoyed it!"
    ]
    
    items = ["croissant", "bread", "pastry", "cake", "cookie", "muffin", "donut", "sandwich"]
    vegan_items = ["vegan croissant", "plant-based cookies", "dairy-free cake", 
                   "egg-free pastry", "vegan bread", "plant based muffin"]
    
    qualities = ["amazing", "delicious", "excellent", "fantastic", "outstanding", "decent", 
                "good", "average", "mediocre", "disappointing"]
    
    atmospheres = ["cozy", "warm", "friendly", "modern", "rustic", "sophisticated", "relaxed"]
    
    recommendations = ["definitely worth a visit", "a must-try", "worth checking out", 
                      "great for breakfast", "perfect for lunch", "a hidden gem"]
    
    additionals = ["Will come back for sure!", "Highly recommend.", "The staff was friendly too.",
                  "Prices are reasonable.", "A bit pricey but worth it.", ""]
    
    # Generate random dates over the past year
    current_date = datetime.now()
    
    for i in range(num_reviews):
        # Randomly decide if this review will mention vegan options
        is_vegan_review = random.random() < vegan_probability
        
        if is_vegan_review:
            template = random.choice(vegan_templates)
            vegan_item = random.choice(vegan_items)
            text = template.format(
                bakery=bakery_name,
                vegan_item=vegan_item,
                quality=random.choice(qualities)
            )
        else:
            template = random.choice(general_templates)
            text = template.format(
                bakery=bakery_name,
                item=random.choice(items),
                quality=random.choice(qualities),
                atmosphere=random.choice(atmospheres),
                recommendation=random.choice(recommendations),
                additional=random.choice(additionals)
            )
        
        # Generate a random date within the last year
        days_ago = random.randint(0, 365)
        review_date = current_date - timedelta(days=days_ago)
        
        # Generate a random rating, biased toward higher ratings
        rating_weights = [0.05, 0.10, 0.15, 0.30, 0.40]  # Probabilities for ratings 1-5
        rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
        
        review = {
            "author_name": f"User{i+1}",
            "rating": rating,
            "text": text,
            "time": int(review_date.timestamp())
        }
        
        reviews.append(review)
    
    return reviews

def generate_mock_bakeries(num_bakeries=20):
    """Generate mock bakery data"""
    bakery_name_parts = {
        "prefix": ["Golden", "Sweet", "Rising", "Fresh", "Hometown", "Artisan", "Morning", "Sunshine", 
                  "Bountiful", "Classic", "Urban", "Rustic", "Heritage", "Daily", "Local"],
        "middle": ["Harvest", "Flour", "Grain", "Loaf", "Crumb", "Dough", "Sugar", "Butter", 
                  "Whisk", "Spoon", "Oven", "Hearth", "Table", "Mill", ""],
        "suffix": ["Bakery", "Bake House", "Bread Co", "Patisserie", "Cakery", "Confections", 
                  "Kitchen", "Cafe", "Boulangerie", "Pastries", "Treats"]
    }
    
    addresses = [
        "123 Main St, San Francisco, CA 94105",
        "456 Market St, San Francisco, CA 94111",
        "789 Valencia St, San Francisco, CA 94110",
        "321 Divisadero St, San Francisco, CA 94117",
        "555 Hayes St, San Francisco, CA 94102",
        "987 Irving St, San Francisco, CA 94122",
        "654 Union St, San Francisco, CA 94133",
        "852 Clement St, San Francisco, CA 94118",
        "753 Polk St, San Francisco, CA 94109",
        "159 9th Ave, San Francisco, CA 94118",
        "357 Castro St, San Francisco, CA 94114",
        "246 Fillmore St, San Francisco, CA 94117",
        "135 Chestnut St, San Francisco, CA 94111",
        "864 Cole St, San Francisco, CA 94117",
        "975 Columbus Ave, San Francisco, CA 94133",
        "468 Geary St, San Francisco, CA 94102",
        "279 Bryant St, San Francisco, CA 94107",
        "486 Brannan St, San Francisco, CA 94107",
        "395 Grant Ave, San Francisco, CA 94108",
        "628 Cortland Ave, San Francisco, CA 94110"
    ]
    
    bakeries = []
    
    for i in range(min(num_bakeries, len(addresses))):
        # Generate random bakery name
        name_parts = [random.choice(bakery_name_parts["prefix"])]
        if random.random() > 0.5:  # 50% chance of including middle part
            name_parts.append(random.choice(bakery_name_parts["middle"]))
        name_parts.append(random.choice(bakery_name_parts["suffix"]))
        
        bakery_name = " ".join(name_parts)
        
        # Higher chance of vegan mentions for bakeries with certain keywords
        vegan_probability = 0.3
        if any(word in bakery_name.lower() for word in ["artisan", "urban", "sunshine", "harvest"]):
            vegan_probability = 0.5
        
        # Generate random reviews
        reviews = generate_mock_reviews(bakery_name, 
                                       num_reviews=random.randint(5, 20),
                                       vegan_probability=vegan_probability)
        
        bakery = {
            "place_id": f"mock_place_id_{i}",
            "name": bakery_name,
            "formatted_address": addresses[i],
            "rating": round(random.uniform(3.2, 4.8), 1),
            "url": f"https://maps.example.com/{bakery_name.replace(' ', '-').lower()}",
            "website": f"https://{bakery_name.replace(' ', '-').lower()}.example.com",
            "reviews": reviews
        }
        
        bakeries.append(bakery)
    
    return bakeries

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

def find_vegan_bakeries_mock(num_bakeries=20):
    """Main function to find and score bakeries for vegan options using mock data"""
    print(f"Generating mock data for {num_bakeries} bakeries...")
    
    # Generate mock bakeries with reviews
    bakeries = generate_mock_bakeries(num_bakeries)
    print(f"Generated {len(bakeries)} mock bakeries. Analyzing reviews...")
    
    # Store results
    results = []
    
    # Process each bakery
    for bakery in bakeries:
        # Analyze reviews for vegan mentions
        analysis = analyze_reviews(bakery["reviews"], SEARCH_TERMS)
        
        # Only include bakeries with vegan mentions
        if analysis["vegan_score"] >= MIN_VEGAN_SCORE:
            results.append({
                "name": bakery["name"],
                "address": bakery["formatted_address"],
                "rating": bakery["rating"],
                "google_maps_url": bakery["url"],
                "website": bakery["website"],
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
        "Website": r["website"],
        "Vegan Mentions": len(r["vegan_mentions"])
    } for r in results])
    
    csv_filename = filename.replace(".json", ".csv")
    df.to_csv(csv_filename, index=False)
    print(f"Summary saved to {csv_filename}")

def main():
    """Main function to run the script"""
    # Get user input for number of mock bakeries
    num_input = input("Enter number of mock bakeries to generate (default: 20): ")
    num_bakeries = int(num_input) if num_input.isdigit() else 20
    
    # Run the search with mock data
    results = find_vegan_bakeries_mock(num_bakeries)
    
    # Display summary
    print(f"\nFound {len(results)} bakeries with vegan options:")
    for i, bakery in enumerate(results[:10], 1):  # Show top 10
        print(f"{i}. {bakery['name']} - Vegan Score: {bakery['vegan_score']} - {bakery['address']}")
    
    if len(results) > 10:
        print(f"...and {len(results) - 10} more.")
    
    # Save results
    save_results(results, "mock_vegan_bakeries_results.json")
    
    # Ask if user wants to see sample reviews
    show_reviews = input("\nShow sample vegan reviews from top bakery? (y/n): ")
    if show_reviews.lower() == 'y' and results:
        top_bakery = results[0]
        print(f"\nSample vegan reviews from {top_bakery['name']}:")
        for i, mention in enumerate(top_bakery['vegan_mentions'][:5], 1):
            print(f"\n{i}. Rating: {mention['rating']} stars - Date: {mention['time']}")
            print(f"   {mention['review_text']}")
            print(f"   Terms mentioned: {', '.join(mention['matches'])}")

if __name__ == "__main__":
    main()

""" Example output:

Enter number of mock bakeries to generate (default: 20): 2
Generating mock data for 2 bakeries...
Generated 2 mock bakeries. Analyzing reviews...

Found 2 bakeries with vegan options:
1. Local Spoon Bakery - Vegan Score: 15 - 456 Market St, San Francisco, CA 94111
2. Bountiful Boulangerie - Vegan Score: 8 - 123 Main St, San Francisco, CA 94105
Results saved to mock_vegan_bakeries_results.json
Summary saved to mock_vegan_bakeries_results.csv

Show sample vegan reviews from top bakery? (y/n): 
"""