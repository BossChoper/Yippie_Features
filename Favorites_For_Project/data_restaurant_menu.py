"""
Restaurant Mock Data Template
This script generates mock data for a fictional restaurant including basic information,
location details, tags, and a detailed menu with nutritional information.
"""
# Functional; provides a template database framework and dataset for restaurant business information

import json
from datetime import datetime

# Mock Restaurant Data
restaurant_data = {
    "name": "Evergreen Kitchen",
    "slogan": "Farm to Table, Sustainably Crafted",
    "description": "Evergreen Kitchen offers a seasonal menu using locally-sourced ingredients with an emphasis on sustainable practices. Our chef-driven dishes balance flavor and nutrition in a cozy, modern atmosphere.",
    "year_established": 2019,
    "location": {
        "address": "427 Oak Street",
        "city": "Portland",
        "state": "Oregon",
        "zip_code": "97205",
        "country": "USA",
        "coordinates": {
            "latitude": 45.523064,
            "longitude": -122.675674
        }
    },
    "contact": {
        "phone": "(503) 555-7890",
        "email": "info@evergreenkitchen.com",
        "website": "www.evergreenkitchen.com",
        "social_media": {
            "instagram": "@evergreenkitchen",
            "facebook": "EverGreenKitchenPDX",
            "twitter": "@EvergreenKitchn"
        }
    },
    "hours": {
        "monday": "11:00 AM - 9:00 PM",
        "tuesday": "11:00 AM - 9:00 PM",
        "wednesday": "11:00 AM - 9:00 PM",
        "thursday": "11:00 AM - 10:00 PM",
        "friday": "11:00 AM - 11:00 PM",
        "saturday": "10:00 AM - 11:00 PM",
        "sunday": "10:00 AM - 8:00 PM"
    },
    "tags": [
        "farm-to-table",
        "sustainable",
        "seasonal",
        "organic",
        "eco-friendly",
        "local ingredients",
        "health-conscious",
        "allergen-friendly"
    ],
    "amenities": [
        "outdoor seating",
        "wheelchair accessible",
        "parking available",
        "wifi",
        "reservations accepted",
        "full bar",
        "private dining available"
    ],
    "menu": {
        "starters": [
            {
                "name": "Roasted Beet Salad",
                "price": 12.95,
                "description": "Locally sourced roasted beets with arugula, goat cheese, candied walnuts, and citrus vinaigrette",
                "tags": [
                    "vegetarian", 
                    "gluten-free", 
                    "low sodium", 
                    "antioxidant-rich"
                ],
                "ingredients": [
                    "organic red beets",
                    "organic golden beets",
                    "organic arugula",
                    "goat cheese",
                    "candied walnuts",
                    "organic orange",
                    "organic lemon juice",
                    "olive oil",
                    "dijon mustard",
                    "local honey",
                    "black pepper"
                ],
                "nutrition": {
                    "serving_size": "1 salad (220g)",
                    "calories": 320,
                    "total_fat": 21,
                    "saturated_fat": 6,
                    "trans_fat": 0,
                    "cholesterol": 15,
                    "sodium": 210,
                    "total_carbs": 24,
                    "dietary_fiber": 5,
                    "sugars": 16,
                    "protein": 9,
                    "vitamin_d": 0,
                    "calcium": 12,
                    "iron": 8,
                    "potassium": 15,
                    "allergens": ["dairy", "nuts"]
                },
                "image": "beet_salad.jpg"
            }
        ],
        "entrees": [
            {
                "name": "Plant-Based Buddha Bowl",
                "price": 16.95,
                "description": "Seasonal roasted vegetables, quinoa, chickpeas, avocado, and tahini dressing on a bed of kale",
                "tags": [
                    "vegan", 
                    "gluten-free", 
                    "high protein", 
                    "low cholesterol", 
                    "heart healthy"
                ],
                "ingredients": [
                    "organic kale",
                    "organic quinoa",
                    "organic chickpeas",
                    "organic sweet potato",
                    "organic broccoli",
                    "organic red bell pepper",
                    "organic avocado",
                    "tahini",
                    "lemon juice",
                    "garlic",
                    "olive oil",
                    "sesame seeds",
                    "sea salt",
                    "black pepper"
                ],
                "nutrition": {
                    "serving_size": "1 bowl (410g)",
                    "calories": 580,
                    "total_fat": 26,
                    "saturated_fat": 3.5,
                    "trans_fat": 0,
                    "cholesterol": 0,
                    "sodium": 380,
                    "total_carbs": 72,
                    "dietary_fiber": 18,
                    "sugars": 10,
                    "protein": 22,
                    "vitamin_d": 0,
                    "calcium": 15,
                    "iron": 30,
                    "potassium": 25,
                    "allergens": ["sesame"]
                },
                "image": "buddha_bowl.jpg"
            },
            {
                "name": "Wild Salmon with Herb Crust",
                "price": 24.95,
                "description": "Pacific wild-caught salmon with herb crust, lemon-caper sauce, roasted fingerling potatoes and seasonal vegetables",
                "tags": [
                    "high protein", 
                    "omega-3 rich", 
                    "gluten-free", 
                    "low carb",
                    "pescatarian"
                ],
                "ingredients": [
                    "wild-caught Pacific salmon",
                    "fresh parsley",
                    "fresh dill",
                    "fresh chives",
                    "lemon zest",
                    "garlic",
                    "olive oil",
                    "capers",
                    "organic fingerling potatoes",
                    "organic seasonal vegetables",
                    "butter",
                    "white wine",
                    "sea salt",
                    "black pepper"
                ],
                "nutrition": {
                    "serving_size": "1 entree (380g)",
                    "calories": 490,
                    "total_fat": 22,
                    "saturated_fat": 5,
                    "trans_fat": 0,
                    "cholesterol": 95,
                    "sodium": 420,
                    "total_carbs": 28,
                    "dietary_fiber": 4,
                    "sugars": 3,
                    "protein": 42,
                    "vitamin_d": 120,
                    "calcium": 8,
                    "iron": 15,
                    "potassium": 24,
                    "allergens": ["fish", "dairy"]
                },
                "image": "salmon_herb_crust.jpg"
            },
            {
                "name": "Grass-Fed Beef Tenderloin",
                "price": 32.95,
                "description": "Locally sourced grass-fed beef with red wine reduction, truffle mashed potatoes, and roasted seasonal vegetables",
                "tags": [
                    "high protein",

                    "locally sourced",
                    "iron-rich"
                ],
                "ingredients": [
                    "grass-fed beef tenderloin",
                    "organic russet potatoes",
                    "organic butter",
                    "organic cream",
                    "truffle oil",
                    "organic garlic",
                    "organic seasonal vegetables",
                    "red wine",
                    "beef stock",
                    "shallots",
                    "fresh thyme",
                    "olive oil",
                    "sea salt",
                    "black pepper"
                ],
                "nutrition": {
                    "serving_size": "1 entree (400g)",
                    "calories": 720,
                    "total_fat": 38,
                    "saturated_fat": 18,
                    "trans_fat": 0.5,
                    "cholesterol": 140,
                    "sodium": 580,
                    "total_carbs": 42,
                    "dietary_fiber": 6,
                    "sugars": 5,
                    "protein": 48,
                    "vitamin_d": 4,
                    "calcium": 10,
                    "iron": 35,
                    "potassium": 28,
                    "allergens": ["dairy"]
                },
                "image": "beef_tenderloin.jpg"
            }
        ],
        "desserts": [
            {
                "name": "Berry Compote Panna Cotta",
                "price": 9.95,
                "description": "House-made coconut milk panna cotta topped with seasonal berry compote and mint",
                "tags": [
                    "vegan", 
                    "gluten-free", 
                    "dairy-free",
                    "low sodium"
                ],
                "ingredients": [
                    "coconut milk",
                    "agar-agar",
                    "organic cane sugar",
                    "vanilla bean",
                    "seasonal organic berries",
                    "organic lemon juice",
                    "fresh mint"
                ],
                "nutrition": {
                    "serving_size": "1 dessert (150g)",
                    "calories": 280,
                    "total_fat": 18,
                    "saturated_fat": 16,
                    "trans_fat": 0,
                    "cholesterol": 0,
                    "sodium": 30,
                    "total_carbs": 30,
                    "dietary_fiber": 3,
                    "sugars": 24,
                    "protein": 2,
                    "vitamin_d": 0,
                    "calcium": 6,
                    "iron": 8,
                    "potassium": 6,
                    "allergens": ["coconut"]
                },
                "image": "panna_cotta.jpg"
            }
        ]
    },
    "special_diets": {
        "vegetarian": True,
        "vegan": True,
        "gluten_free": True,
        "dairy_free": True,
        "nut_free_options": True,
        "keto_friendly": True,
        "paleo_friendly": True
    },
    "sustainability_practices": [
        "Locally sourced ingredients (within 100 miles when possible)",
        "Composting food waste",
        "Energy-efficient appliances and lighting",
        "Reusable/biodegradable to-go containers",
        "Water conservation practices",
        "Supporting regenerative agriculture"
    ],
    "reviews": {
        "average_rating": 4.7,
        "total_reviews": 342,
        "rating_distribution": {
            "5_star": 268,
            "4_star": 52,
            "3_star": 12,
            "2_star": 6,
            "1_star": 4
        }
    },
    "metadata": {
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0",
        "is_mock_data": True
    }
}

# Print sample of the data structure to console
print(json.dumps(restaurant_data, indent=2))

# Save to file
with open('restaurant_mock_data.json', 'w') as file:
    json.dump(restaurant_data, file, indent=2)

print("\nMock restaurant data has been generated and saved to 'restaurant_mock_data.json'")