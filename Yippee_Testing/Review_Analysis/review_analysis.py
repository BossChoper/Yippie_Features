import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import numpy as np
from collections import Counter
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
        
        # Prepare keyword categories for analysis
        self.keyword_categories = {
            "mac_cheese": ["mac", "macaroni", "cheese", "cheesy", "cheddar", "pasta", "elbow"],
            "spicy": ["spicy", "hot", "heat", "burn", "fiery", "chili", "pepper", "kick"],
            "creamy": ["creamy", "smooth", "rich", "velvety", "silky"],
            "crispy": ["crispy", "crunchy", "crunch", "crisp"],
            "sweet": ["sweet", "sugar", "syrup", "honey"],
            "salty": ["salty", "salt", "briny"],
            "fresh": ["fresh", "light", "refreshing"],
            "savory": ["savory", "umami", "rich", "flavorful"],
            "bland": ["bland", "boring", "plain", "unseasoned"]
        }
        
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
    
    def keyword_match(self, tokens, keyword_list):
        """Check if tokens contain keywords from the specified list"""
        match_score = sum(1 for token in tokens if token in keyword_list)
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
    
    def analyze_reviews(self, reviews):
        """Analyze reviews to extract key characteristics"""
        # Combine all reviews into one text
        all_review_text = " ".join(reviews)
        tokens = self.preprocess_text(all_review_text)
        
        # Check for characteristics
        characteristics = {}
        for category, keywords in self.keyword_categories.items():
            matches = [token for token in tokens if token in keywords]
            if matches:
                count = sum(1 for token in tokens if token in keywords)
                characteristics[category] = {
                    "count": count,
                    "matched_words": list(set(matches))
                }
        
        return characteristics
    
    def generate_assumption_sentence(self, item, characteristics):
        """Generate an assumption sentence based on review analysis"""
        item_name = item["name"]
        
        # If no characteristics found, return None
        if not characteristics:
            return None
        
        # Sort characteristics by count
        sorted_chars = sorted(characteristics.items(), key=lambda x: x[1]["count"], reverse=True)
        
        # Generate assumption sentences based on top characteristics
        sentences = []
        
        # Check for mac and cheese in non-mac dishes
        if "mac_cheese" in characteristics and "mac" not in item_name.lower() and "macaroni" not in item_name.lower():
            words = characteristics["mac_cheese"]["matched_words"]
            if "mac" in words or "macaroni" in words:
                sentences.append(f"This {item_name.lower()} appears to contain mac and cheese based on multiple reviews.")
            elif "cheese" in words or "cheesy" in words:
                sentences.append(f"This {item_name.lower()} is frequently described as cheesy in reviews.")
        
        # Check for spiciness
        if "spicy" in characteristics:
            count = characteristics["spicy"]["count"]
            if count >= 4:
                sentences.append(f"This dish is described as very spicy in multiple reviews.")
            elif count >= 2:
                sentences.append(f"Some customers mention this dish has a spicy kick to it.")
        
        # Check for creaminess
        if "creamy" in characteristics and characteristics["creamy"]["count"] >= 2:
            sentences.append(f"Customers frequently describe this as creamy and smooth.")
        
        # Check for crispiness
        if "crispy" in characteristics and characteristics["crispy"]["count"] >= 2:
            sentences.append(f"This dish is noted for its crispy texture in reviews.")
        
        # Check for blandness
        if "bland" in characteristics and characteristics["bland"]["count"] >= 2:
            sentences.append(f"Some customers find this dish to be somewhat bland.")
        
        # If we have multiple sentences, just return the most significant one
        if sentences:
            return sentences[0]
        
        # Fallback for top characteristic if no specific sentences were generated
        if sorted_chars:
            top_char, details = sorted_chars[0]
            count = details["count"]
            words = ", ".join(details["matched_words"])
            
            if top_char == "mac_cheese":
                return f"This dish is notable for its cheese qualities."
            elif top_char == "spicy":
                return f"This dish has some level of spiciness according to reviews."
            elif top_char == "sweet":
                return f"Customers mention this dish has sweet flavors."
            elif top_char == "salty":
                return f"This dish is described as notably salty in reviews."
            elif top_char == "fresh":
                return f"Customers highlight the freshness of this dish."
            elif top_char == "savory":
                return f"This is described as a particularly savory and flavorful dish."
        
        return None
    
    def filter_results(self, matches, query_tokens):
        """Filter and enhance results based on query intent"""
        # Determine query intent based on keywords
        query_intents = []
        for category, keywords in self.keyword_categories.items():
            if self.keyword_match(query_tokens, keywords):
                query_intents.append(category)
        
        # Filter and enhance results
        results = []
        
        for idx, score in matches:
            item = self.menu_items[idx]
            restaurant_idx = self.restaurant_indices[idx]
            restaurant = self.restaurants[restaurant_idx]
            
            # Analyze reviews for this item
            characteristics = self.analyze_reviews(item["reviews"])
            
            # Generate assumption sentence
            assumption = self.generate_assumption_sentence(item, characteristics)
            
            # For mac and cheese intent, only include actual mac and cheese items
            if "mac_cheese" in query_intents:
                item_text = f"{item['name']} {item['description']}".lower()
                item_tokens = self.preprocess_text(item_text)
                
                has_mac = any(token in ["mac", "macaroni", "elbow"] for token in item_tokens)
                has_cheese = any(token in ["cheese", "cheesy", "cheddar"] for token in item_tokens)
                
                if has_mac and has_cheese:
                    result_item = {
                        "restaurant": restaurant["name"],
                        "item": item["name"],
                        "description": item["description"],
                        "relevance": score,
                        "reviews": item["reviews"],
                        "characteristics": characteristics
                    }
                    
                    if assumption:
                        result_item["assumption"] = assumption
                    
                    results.append(result_item)
            
            # For spicy intent, prioritize spicy items
            elif "spicy" in query_intents:
                is_spicy = "spicy" in characteristics
                
                if is_spicy:
                    result_item = {
                        "restaurant": restaurant["name"],
                        "item": item["name"],
                        "description": item["description"],
                        "relevance": score,
                        "reviews": item["reviews"],
                        "characteristics": characteristics
                    }
                    
                    if assumption:
                        result_item["assumption"] = assumption
                    
                    results.append(result_item)
            
            # For other intents or general queries, include all matches
            else:
                result_item = {
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "description": item["description"],
                    "relevance": score,
                    "reviews": item["reviews"],
                    "characteristics": characteristics
                }
                
                if assumption:
                    result_item["assumption"] = assumption
                
                results.append(result_item)
        
        return results
    
    def search(self, query):
        # Preprocess the query
        query_tokens = self.preprocess_text(query)
        
        # Perform semantic search
        matches = self.semantic_search(query)
        
        # Filter and enhance results
        results = self.filter_results(matches, query_tokens)
        
        return results

# User interface
def main():
    searcher = RestaurantFoodSearch(restaurants)
    
    print("Restaurant Food & Review Analysis Search")
    print("---------------------------------------")
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
                
                # Display assumption if available
                if "assumption" in result and result["assumption"]:
                    print(f"\n   ➤ {result['assumption']}")
                
                # Display relevant reviews
                print("\n   Sample reviews:")
                for review in result["reviews"][:2]:  # Limit to first 2 reviews
                    print(f"   - \"{review}\"")
                        
        else:
            print("\nSorry, I couldn't find any dishes matching your query.")

if __name__ == "__main__":
    main()

""" Example output: 
Restaurant Food & Review Analysis Search
---------------------------------------
Search for dishes by name, description, or what people say in reviews
Try searches like 'mac and cheese', 'spicy', 'creamy', etc.
Type 'exit' to quit


What are you looking for? spicy 

Found 4 matching items:

1. Spicy Jambalaya at Southern Comfort
   Rice dish with sausage, chicken, and spicy seasoning

   ➤ Some customers mention this dish has a spicy kick to it.

   Sample reviews:
   - "Packs a serious punch! Very spicy but flavorful."
   - "One of the spiciest dishes on the menu. Authentic Cajun heat."

""" 
# Review analysis and assumption system
# Use characteristic to find food (spicy foods)
# Useful for food querying and filtering based on reviews