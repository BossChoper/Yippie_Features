# Analyzes reviews to find text/keywords and reports memory
import time
from collections import Counter
import nltk
from memory_profiler import profile
from typing import List, Dict

# Ensure NLTK resources are downloaded (run once)
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Mock review data (simulating Yelp reviews for "Burger")
MOCK_REVIEWS = [
    {"text": "This burger is spicy and delicious!", "rating": 4},
    {"text": "Really spicy burger, loved it.", "rating": 5},
    {"text": "Too spicy for me, but good.", "rating": 3},
    {"text": "Spicy and greasy, not bad.", "rating": 4},
    {"text": "Sweet bun, spicy patty, amazing!", "rating": 5}
] * 100  # Multiply to simulate larger dataset (500 reviews)

# Implementation 1: Basic Counter (original)
@profile
def analyze_reviews_counter(reviews: List[Dict]) -> str:
    """Analyze reviews using Counter."""
    all_text = " ".join(review["text"].lower() for review in reviews)
    keywords = ["spicy", "sweet", "salty", "greasy", "delicious"]
    word_counts = Counter(all_text.split())
    relevant_counts = {kw: word_counts.get(kw, 0) for kw in keywords}
    if not any(relevant_counts.values()):
        return "No strong trends detected."
    most_common = max(relevant_counts.items(), key=lambda x: x[1])
    keyword, count = most_common
    return f"This item is known to be {keyword}." if count >= 2 else "No strong trends detected."

# Implementation 2: Simple Loop
@profile
def analyze_reviews_loop(reviews: List[Dict]) -> str:
    """Analyze reviews using a manual loop."""
    all_text = " ".join(review["text"].lower() for review in reviews).split()
    keywords = ["spicy", "sweet", "salty", "greasy", "delicious"]
    word_counts = {kw: 0 for kw in keywords}
    for word in all_text:
        if word in keywords:
            word_counts[word] += 1
    if not any(word_counts.values()):
        return "No strong trends detected."
    most_common = max(word_counts.items(), key=lambda x: x[1])
    keyword, count = most_common
    return f"This item is known to be {keyword}." if count >= 2 else "No strong trends detected."

# Implementation 3: NLTK (NLP-based)
@profile
def analyze_reviews_nltk(reviews: List[Dict]) -> str:
    """Analyze reviews using NLTK for adjective detection."""
    all_text = " ".join(review["text"].lower() for review in reviews)
    tokens = nltk.word_tokenize(all_text)
    tagged = nltk.pos_tag(tokens)
    adjectives = [word for word, pos in tagged if pos.startswith("JJ")]
    if not adjectives:
        return "No strong trends detected."
    word_counts = Counter(adjectives)
    top_adj = word_counts.most_common(1)[0][0]
    return f"This item is known to be {top_adj}."

def measure_time(func, reviews: List[Dict], name: str) -> float:
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(reviews)
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n{name}:")
    print(f"  Result: {result}")
    print(f"  Time: {duration:.4f} seconds")
    return duration

def main():
    """Run the Memory Checker Program."""
    print("Starting Memory Checker Program...")
    print(f"Testing with {len(MOCK_REVIEWS)} mock reviews.")

    # Test each implementation
    time_counter = measure_time(analyze_reviews_counter, MOCK_REVIEWS, "Counter Implementation")
    time_loop = measure_time(analyze_reviews_loop, MOCK_REVIEWS, "Loop Implementation")
    time_nltk = measure_time(analyze_reviews_nltk, MOCK_REVIEWS, "NLTK Implementation")

    # Summary
    print("\nSummary:")
    print(f"  Counter Time: {time_counter:.4f} s")
    print(f"  Loop Time: {time_loop:.4f} s")
    print(f"  NLTK Time: {time_nltk:.4f} s")
    print("  (See memory usage in console output from @profile)")

if __name__ == "__main__":
    main()


"""
\\ Example output:
Starting Memory Checker Program...
Testing with 500 mock reviews.

Counter Implementation:
  Result: This item is known to be spicy.
  Time: 0.0023 seconds
Line #    Mem usage    Increment   Line Contents
==============================================
    28     50.1 MiB     50.1 MiB   @profile
    29                             def analyze_reviews_counter(reviews):
    30     50.1 MiB      0.0 MiB       all_text = " ".join(...)
    31     50.1 MiB      0.0 MiB       keywords = ["spicy", ...]
    32     50.1 MiB      0.0 MiB       word_counts = Counter(all_text.split())
    ...

Loop Implementation:
  Result: This item is known to be spicy.
  Time: 0.0031 seconds
Line #    Mem usage    Increment   Line Contents
==============================================
    44     50.1 MiB     50.1 MiB   @profile
    45                             def analyze_reviews_loop(reviews):
    46     50.1 MiB      0.0 MiB       all_text = " ".join(...).split()
    ...

NLTK Implementation:
  Result: This item is known to be spicy.
  Time: 0.0456 seconds
Line #    Mem usage    Increment   Line Contents
==============================================
    59     50.2 MiB     50.2 MiB   @profile
    60                             def analyze_reviews_nltk(reviews):
    61     50.2 MiB      0.0 MiB       all_text = " ".join(...)
    62     50.2 MiB      0.0 MiB       tokens = nltk.word_tokenize(all_text)
    ...

Summary:
  Counter Time: 0.0023 s
  Loop Time: 0.0031 s
  NLTK Time: 0.0456 s
  (See memory usage in console output from @profile)
\\
"""
# Review analysis for menu item assumptions
# Useful for debugging, speed analysis, menu item assumption creation