# Functional
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK components
try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('wordnet')
    nltk.download('stopwords')

# Mock restaurant data with menu items and reviews
restaurants = [
    {
        "name": "Cheesy Corner",
        "menu": [
            {
                "id": "cc1",
                "name": "Homestyle Mac and Cheese", 
                "description": "Creamy blend of cheddar and Monterey Jack with elbow macaroni",
                "reviews": [
                    "Best mac and cheese I've ever had! So creamy and cheesy.",
                    "Love this classic mac and cheese. Perfect comfort food.",
                    "A bit bland for my taste, could use more seasoning.",
                    "The mac and cheese is their specialty for a reason, so good!"
                ]
            },
            {
                "id": "cc2",
                "name": "Truffle Mac", 
                "description": "Macaroni with aged white cheddar and truffle oil",
                "reviews": [
                    "The truffle mac is absolutely divine! Worth every penny.",
                    "Elegant take on mac and cheese, very rich and aromatic.",
                    "Too strong on the truffle flavor, overpowered the cheese.",
                    "Best truffle mac in town, perfect for a fancy night out."
                ]
            },
            {
                "id": "cc3",
                "name": "Cheeseburger", 
                "description": "Beef patty with American cheese on a brioche bun",
                "reviews": [
                    "Standard cheeseburger, nothing special but good.",
                    "Their burgers are okay, but come for the mac and cheese.",
                    "Juicy burger but the cheese wasn't melted properly.",
                    "Decent burger, but not as good as their mac and cheese options."
                ]
            }
        ]
    },
    {
        "name": "Spice Kingdom",
        "menu": [
            {
                "id": "sk1",
                "name": "Spicy Curry Mac", 
                "description": "Mac and cheese with a spicy curry twist",
                "reviews": [
                    "Wow! So spicy but delicious. Have water ready!",
                    "The spicy mac was way too hot for me to finish.",
                    "Perfect level of heat. The cheese balances the spice nicely.",
                    "Unique fusion dish - the curry flavor with creamy mac is amazing!"
                ]
            },
            {
                "id": "sk2",
                "name": "Devil's Pasta", 
                "description": "Fiery red sauce with ghost pepper and pasta",
                "reviews": [
                    "EXTREMELY SPICY! Not for beginners.",
                    "Couldn't feel my tongue after eating this. Insanely hot!",
                    "The spiciest pasta I've ever had. Great flavor beneath the heat.",
                    "They don't call it Devil's Pasta for nothing. Too spicy to enjoy."
                ]
            },
            {
                "id": "sk3",
                "name": "Mild Tikka Masala", 
                "description": "Creamy tomato sauce with mild spices and tender chicken",
                "reviews": [
                    "Perfect for those who can't handle spice. Very flavorful.",
                    "Don't let the 'mild' fool you - it's still got a kick!",
                    "Nice flavor but very mild compared to their other dishes.",
                    "Good balance of spices without being overwhelming."
                ]
            }
        ]
    },
    {
        "name": "Comfort Food Haven",
        "menu": [
            {
                "id": "cfh1",
                "name": "Gourmet Macaroni and Cheese", 
                "description": "House specialty with three cheese blend and bread crumbs",
                "reviews": [
                    "The cheese blend is perfect - sharp, creamy, and rich!",
                    "Best mac and cheese in the city, hands down.",
                    "The breadcrumbs add a nice crunch to the creamy pasta.",
                    "A bit overpriced for mac and cheese, but it's really good."
                ]
            },
            {
                "id": "cfh2",
                "name": "Fried Chicken", 
                "description": "Crispy chicken with secret spices",
                "reviews": [
                    "Crispy outside, juicy inside. Perfect fried chicken!",
                    "The chicken is good but their mac and cheese is better.",
                    "Not too spicy, just the right amount of seasoning.",
                    "The best fried chicken I've had in years. So crispy!"
                ]
            },
            {
                "id": "cfh3",
                "name": "Loaded Cheese Fries", 
                "description": "Fries topped with cheddar cheese sauce and bacon",
                "reviews": [
                    "The cheese sauce is basically liquid gold.",
                    "So indulgent! The cheese is similar to their mac and cheese.",
                    "Good but too salty for my taste.",
                    "These fries are addictive - the cheese sauce is amazing!"
                ]
            }
        ]
    },
    {
        "name": "Burger Shack",
        "menu": [
            {
                "id": "bs1",
                "name": "Classic Burger", 
                "description": "Beef patty with lettuce, tomato, and our special sauce",
                "reviews": [
                    "Simple but delicious burger. The special sauce makes it.",
                    "Nothing fancy but perfectly executed.",
                    "Juicy patty and fresh vegetables. Solid burger.",
                    "Their classic burger is my go-to every time."
                ]
            },
            {
                "id": "bs2",
                "name": "Cheesy Bacon Burger", 
                "description": "Burger topped with American cheese and bacon",
                "reviews": [
                    "The cheese is perfectly melted and the bacon is crispy.",
                    "Heart attack on a plate but worth it!",
                    "Good burger but nothing revolutionary.",
                    "Cheese lovers will enjoy this one."
                ]
            },
            {
                "id": "bs3",
                "name": "Mac Attack Burger", 
                "description": "Burger topped with mac and cheese and bacon bits",
                "reviews": [
                    "Innovative burger! The mac and cheese topping is delicious.",
                    "Messy to eat but so worth it. Best of both worlds.",
                    "Their mac and cheese makes this burger special.",
                    "It sounds weird but it works! The mac and cheese is creamy and complements the burger perfectly."
                ]
            }
        ]
    },
    {
        "name": "Southern Comfort",
        "menu": [
            {
                "id": "sc1",
                "name": "Baked Macaroni Casserole", 
                "description": "Traditional Southern style baked macaroni with cheese",
                "reviews": [
                    "Just like my grandma used to make. Perfect southern mac and cheese.",
                    "The crispy top layer is amazing. Not too spicy, just right.",
                    "Authentic southern style with that baked cheese crust.",
                    "A bit dry compared to creamier versions, but still delicious."
                ]
            },
            {
                "id": "sc2",
                "name": "Spicy Jambalaya", 
                "description": "Rice dish with sausage, chicken, and spicy seasoning",
                "reviews": [
                    "Packs a serious punch! Very spicy but flavorful.",
                    "One of the spiciest dishes on the menu. Authentic Cajun heat.",
                    "Too spicy for me to finish, but my husband loved it.",
                    "Great flavor and the spice builds as you eat. Have some water ready!"
                ]
            },
            {
                "id": "sc3",
                "name": "Cheese Grits", 
                "description": "Creamy grits with cheddar cheese",
                "reviews": [
                    "Smooth, creamy, cheesy goodness. Perfect comfort food.",
                    "The cheese flavor is perfect. Not too sharp, not too mild.",
                    "Best cheese grits I've ever had outside of my mom's.",
                    "A simple dish done perfectly. The cheese really makes it."
                ]
            }
        ]
    }
]

class RestaurantFoodSearch:
    def __init__(self, restaurant_data):
        self.restaurants = restaurant_data
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Prepare relevant keywords
        self.mac_cheese_keywords = [
            "mac", "macaroni", "cheese", "cheesy", "cheddar", "pasta", "elbow"
        ]
        
        self.spicy_keywords = [
            "spicy", "hot", "heat", "burn", "fiery", "chili", "pepper", "kick"
        ]
        
        # Prepare corpus for TF-IDF
        self.corpus = []
        self.menu_items = []
        self.restaurant_indices = []
        
        for restaurant_idx, restaurant in enumerate(self.restaurants):
            for item in restaurant["menu"]:
                # Combine menu description with all reviews
                all_reviews = " ".join(item["reviews"])
                text = f"{item['name']} {item['description']} {all_reviews}".lower()
                self.corpus.append(text)
                self.menu_items.append(item)
                self.restaurant_indices.append(restaurant_idx)
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
    
    def preprocess_text(self, text):
        # Convert to lowercase and remove non-alphanumeric characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
        
        # Tokenize
        tokens = text.split()
        
        # Remove stopwords and lemmatize
        processed_tokens = [
            self.lemmatizer.lemmatize(token) for token in tokens 
            if token not in self.stop_words
        ]
        
        return processed_tokens
    
    def keyword_match(self, query_tokens, keyword_list):
        """Check if the query contains keywords from the specified list"""
        match_score = sum(1 for token in query_tokens if token in keyword_list)
        return match_score > 0
    
    def semantic_search(self, query):
        """Search using TF-IDF and cosine similarity"""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get matches above a threshold
        threshold = 0.1
        matches = [(i, score) for i, score in enumerate(similarities) if score > threshold]
        
        # Sort by similarity score
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches
    
    def filter_mac_cheese_results(self, matches):
        """Filter to ensure we're only returning mac and cheese items"""
        filtered_results = []
        
        for idx, score in matches:
            item = self.menu_items[idx]
            restaurant_idx = self.restaurant_indices[idx]
            restaurant = self.restaurants[restaurant_idx]
            
            item_text = f"{item['name']} {item['description']}".lower()
            item_tokens = self.preprocess_text(item_text)
            
            # Check if the item is actually mac and cheese related
            # Must contain both mac/macaroni AND cheese concepts
            has_mac = any(token in ["mac", "macaroni", "elbow"] for token in item_tokens)
            has_cheese = any(token in ["cheese", "cheesy", "cheddar"] for token in item_tokens)
            
            if has_mac and has_cheese:
                filtered_results.append({
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "description": item["description"],
                    "relevance": score,
                    "reviews": item["reviews"]
                })
        
        return filtered_results
    
    def filter_spicy_results(self, matches):
        """Filter to ensure we're returning items mentioned as spicy in reviews"""
        filtered_results = []
        
        for idx, score in matches:
            item = self.menu_items[idx]
            restaurant_idx = self.restaurant_indices[idx]
            restaurant = self.restaurants[restaurant_idx]
            
            # Check both description and reviews for mentions of spiciness
            spicy_reviews = []
            for review in item["reviews"]:
                review_tokens = self.preprocess_text(review)
                if self.keyword_match(review_tokens, self.spicy_keywords):
                    spicy_reviews.append(review)
            
            description_tokens = self.preprocess_text(item["description"])
            is_spicy_in_description = self.keyword_match(description_tokens, self.spicy_keywords)
            
            # Include if spicy is mentioned in description or in any reviews
            if is_spicy_in_description or spicy_reviews:
                filtered_results.append({
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "description": item["description"],
                    "relevance": score,
                    "spicy_reviews": spicy_reviews,
                    "all_reviews": item["reviews"]
                })
        
        return filtered_results
    
    def filter_results(self, matches, query_tokens):
        """Filter results based on query intent"""
        # Check for specific intents
        is_mac_cheese_query = self.keyword_match(query_tokens, self.mac_cheese_keywords)
        is_spicy_query = self.keyword_match(query_tokens, self.spicy_keywords)
        
        # Apply appropriate filters
        if is_mac_cheese_query:
            return self.filter_mac_cheese_results(matches)
        elif is_spicy_query:
            return self.filter_spicy_results(matches)
        else:
            # For general queries, include all matches with their reviews
            general_results = []
            for idx, score in matches:
                item = self.menu_items[idx]
                restaurant_idx = self.restaurant_indices[idx]
                restaurant = self.restaurants[restaurant_idx]
                
                general_results.append({
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "description": item["description"],
                    "relevance": score,
                    "reviews": item["reviews"]
                })
            return general_results
    
    def search(self, query):
        # Preprocess the query
        query_tokens = self.preprocess_text(query)
        
        # Perform semantic search
        matches = self.semantic_search(query)
        
        # Filter and return results
        results = self.filter_results(matches, query_tokens)
        
        return results

# User interface
def main():
    searcher = RestaurantFoodSearch(restaurants)
    
    print("Restaurant Food & Review Search")
    print("-------------------------------")
    print("Search for dishes by name, description, or what people say in reviews")
    print("Try searches like 'mac and cheese', 'spicy', 'creamy', etc.")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("\nWhat are you looking for? ")
        if query.lower() == 'exit':
            break
        
        results = searcher.search(query)
        
        if results:
            print(f"\nFound {len(results)} matching items:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['item']} at {result['restaurant']}")
                print(f"   {result['description']}")
                
                # Display relevant reviews
                if "spicy_reviews" in result and result["spicy_reviews"]:
                    print("\n   What people say about the spiciness:")
                    for review in result["spicy_reviews"][:2]:  # Limit to first 2 reviews
                        print(f"   - \"{review}\"")
                else:
                    print("\n   Sample reviews:")
                    for review in result["reviews"][:2]:  # Limit to first 2 reviews
                        print(f"   - \"{review}\"")
                        
        else:
            print("\nSorry, I couldn't find any dishes matching your query.")

if __name__ == "__main__":
    main()

""" Example output:
Restaurant Food & Review Search
-------------------------------
Search for dishes by name, description, or what people say in reviews
Try searches like 'mac and cheese', 'spicy', 'creamy', etc.
Type 'exit' to quit


What are you looking for? cheese

Found 6 matching items:

1. Gourmet Macaroni and Cheese at Comfort Food Haven
   House specialty with three cheese blend and bread crumbs

   Sample reviews:
   - "The cheese blend is perfect - sharp, creamy, and rich!"
   - "Best mac and cheese in the city, hands down."

2. Homestyle Mac and Cheese at Cheesy Corner
   Creamy blend of cheddar and Monterey Jack with elbow macaroni

   Sample reviews:
   - "Best mac and cheese I've ever had! So creamy and cheesy."
   - "Love this classic mac and cheese. Perfect comfort food."

3. Mac Attack Burger at Burger Shack
   Burger topped with mac and cheese and bacon bits

   Sample reviews:
   - "Innovative burger! The mac and cheese topping is delicious."
   - "Messy to eat but so worth it. Best of both worlds."

4. Baked Macaroni Casserole at Southern Comfort
   Traditional Southern style baked macaroni with cheese

   Sample reviews:
   - "Just like my grandma used to make. Perfect southern mac and cheese."
   - "The crispy top layer is amazing. Not too spicy, just right."
"""

# Find foods based on foods and characteristics
# Provide list of foods from different restaurants
# Useful for review analysis testing, food finding