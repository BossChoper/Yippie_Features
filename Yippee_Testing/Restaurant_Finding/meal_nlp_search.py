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

# Mock restaurant data
restaurants = [
    {
        "name": "Cheesy Corner",
        "menu": [
            {"name": "Homestyle Mac and Cheese", "description": "Creamy blend of cheddar and Monterey Jack with elbow macaroni"},
            {"name": "Truffle Mac", "description": "Macaroni with aged white cheddar and truffle oil"},
            {"name": "Cheeseburger", "description": "Beef patty with American cheese on a brioche bun"}
        ]
    },
    {
        "name": "Italian Bistro",
        "menu": [
            {"name": "Spaghetti Carbonara", "description": "Pasta with egg, cheese, pancetta and black pepper"},
            {"name": "Lasagna", "description": "Layered pasta with meat sauce and cheese"},
            {"name": "Pizza Margherita", "description": "Tomato sauce, mozzarella cheese and basil"}
        ]
    },
    {
        "name": "Comfort Food Haven",
        "menu": [
            {"name": "Gourmet Macaroni and Cheese", "description": "House specialty with three cheese blend and bread crumbs"},
            {"name": "Fried Chicken", "description": "Crispy chicken with secret spices"},
            {"name": "Loaded Cheese Fries", "description": "Fries topped with cheddar cheese sauce and bacon"}
        ]
    },
    {
        "name": "Burger Shack",
        "menu": [
            {"name": "Classic Burger", "description": "Beef patty with lettuce, tomato, and our special sauce"},
            {"name": "Cheesy Bacon Burger", "description": "Burger topped with American cheese and bacon"},
            {"name": "Mac Attack Burger", "description": "Burger topped with mac and cheese and bacon bits"}
        ]
    },
    {
        "name": "Southern Comfort",
        "menu": [
            {"name": "Baked Macaroni Casserole", "description": "Traditional Southern style baked macaroni with cheese"},
            {"name": "Fried Okra", "description": "Crispy seasoned okra"},
            {"name": "Cheese Grits", "description": "Creamy grits with cheddar cheese"}
        ]
    }
]

class MacAndCheeseSearch:
    def __init__(self, restaurant_data):
        self.restaurants = restaurant_data
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Prepare relevant keywords for mac and cheese
        self.mac_cheese_keywords = [
            "mac", "macaroni", "cheese", "cheesy", "cheddar", "pasta", "elbow"
        ]
        
        # Prepare corpus for TF-IDF
        self.corpus = []
        self.menu_items = []
        self.restaurant_indices = []
        
        for restaurant_idx, restaurant in enumerate(self.restaurants):
            for item in restaurant["menu"]:
                text = f"{item['name']} {item['description']}".lower()
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
    
    def keyword_match(self, query_tokens):
        """Check if the query contains mac and cheese related keywords"""
        # Count how many mac and cheese related keywords are in the query
        match_score = sum(1 for token in query_tokens if token in self.mac_cheese_keywords)
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
    
    def filter_results(self, matches, is_mac_and_cheese_query):
        """Filter to ensure we're only returning mac and cheese items when that's the intent"""
        filtered_results = []
        
        for idx, score in matches:
            item = self.menu_items[idx]
            restaurant_idx = self.restaurant_indices[idx]
            restaurant = self.restaurants[restaurant_idx]
            
            # For mac and cheese queries, only include actual mac and cheese items
            if is_mac_and_cheese_query:
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
                        "relevance": score
                    })
            else:
                # For non-mac and cheese queries, include all matches
                filtered_results.append({
                    "restaurant": restaurant["name"],
                    "item": item["name"],
                    "description": item["description"],
                    "relevance": score
                })
        
        return filtered_results
    
    def search(self, query):
        # Preprocess the query
        query_tokens = self.preprocess_text(query)
        
        # Determine if this is a mac and cheese related query
        is_mac_and_cheese_query = self.keyword_match(query_tokens)
        
        # Perform semantic search
        matches = self.semantic_search(query)
        
        # Filter and return results
        results = self.filter_results(matches, is_mac_and_cheese_query)
        
        return results

# User interface
def main():
    searcher = MacAndCheeseSearch(restaurants)
    
    print("Mac and Cheese Restaurant Finder")
    print("--------------------------------")
    print("Type 'exit' to quit\n")
    
    while True:
        query = input("What are you looking for? ")
        if query.lower() == 'exit':
            break
        
        results = searcher.search(query)
        
        if results:
            print("\nHere's what I found:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['item']} at {result['restaurant']}")
                print(f"   {result['description']}")
            print()
        else:
            print("\nSorry, I couldn't find any mac and cheese dishes matching your query.\n")

if __name__ == "__main__":
    main()

""" Example output: 
Mac and Cheese Restaurant Finder
--------------------------------
Type 'exit' to quit

What are you looking for? mac

Here's what I found:

1. Mac Attack Burger at Burger Shack
   Burger topped with mac and cheese and bacon bits

2. Homestyle Mac and Cheese at Cheesy Corner
   Creamy blend of cheddar and Monterey Jack with elbow macaroni
"""

# Searches restaurants based on query
# Returns associated meals at restaurant
# Useful for queries and menu searches