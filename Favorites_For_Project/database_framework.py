# Should be functional; acting weird
import sqlite3
import os
from datetime import datetime

def create_tables(cursor):
    """Create the necessary tables for the restaurant database"""
    
    # Restaurant information table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slogan TEXT,
        description TEXT,
        year_established INTEGER,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        country TEXT,
        latitude REAL,
        longitude REAL,
        phone TEXT,
        email TEXT,
        website TEXT,
        average_rating REAL,
        total_reviews INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Hours of operation table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        day_of_week TEXT,
        opening_time TEXT,
        closing_time TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Tags table (restaurant tags like farm-to-table, sustainable, etc.)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurant_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        tag TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Amenities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS amenities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        amenity TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Social media table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS social_media (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        platform TEXT,
        handle TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Menu categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        name TEXT,
        display_order INTEGER,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Menu items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        name TEXT NOT NULL,
        price REAL,
        description TEXT,
        image_path TEXT,
        FOREIGN KEY (category_id) REFERENCES menu_categories (id)
    )
    ''')
    
    # Item tags table (vegetarian, vegan, etc.)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        tag TEXT,
        FOREIGN KEY (item_id) REFERENCES menu_items (id)
    )
    ''')
    
    # Ingredients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        name TEXT,
        FOREIGN KEY (item_id) REFERENCES menu_items (id)
    )
    ''')
    
    # Nutritional information table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nutrition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        serving_size TEXT,
        calories INTEGER,
        total_fat REAL,
        saturated_fat REAL,
        trans_fat REAL,
        cholesterol REAL,
        sodium REAL,
        total_carbs REAL,
        dietary_fiber REAL,
        sugars REAL,
        protein REAL,
        vitamin_d REAL,
        calcium REAL,
        iron REAL,
        potassium REAL,
        FOREIGN KEY (item_id) REFERENCES menu_items (id)
    )
    ''')
    
    # Allergens table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        allergen TEXT,
        FOREIGN KEY (item_id) REFERENCES menu_items (id)
    )
    ''')
    
    # Sustainability practices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sustainability_practices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        practice TEXT,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')
    
    # Special diets accommodated table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS special_diets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurant_id INTEGER,
        diet_name TEXT,
        is_accommodated BOOLEAN,
        FOREIGN KEY (restaurant_id) REFERENCES restaurant (id)
    )
    ''')

def insert_restaurant_data(conn, cursor):
    """Insert mock restaurant data into the database"""
    
    # Insert restaurant information
    cursor.execute('''
    INSERT INTO restaurant (
        name, slogan, description, year_established, 
        address, city, state, zip_code, country, 
        latitude, longitude, phone, email, website,
        average_rating, total_reviews
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        "Evergreen Kitchen",
        "Farm to Table, Sustainably Crafted",
        "Evergreen Kitchen offers a seasonal menu using locally-sourced ingredients with an emphasis on sustainable practices. Our chef-driven dishes balance flavor and nutrition in a cozy, modern atmosphere.",
        2019,
        "427 Oak Street",
        "Portland",
        "Oregon",
        "97205",
        "USA",
        45.523064,
        -122.675674,
        "(503) 555-7890",
        "info@evergreenkitchen.com",
        "www.evergreenkitchen.com",
        4.7,
        342
    ))
    
    restaurant_id = cursor.lastrowid
    
    # Insert hours of operation
    hours_data = [
        ("monday", "11:00 AM", "9:00 PM"),
        ("tuesday", "11:00 AM", "9:00 PM"),
        ("wednesday", "11:00 AM", "9:00 PM"),
        ("thursday", "11:00 AM", "10:00 PM"),
        ("friday", "11:00 AM", "11:00 PM"),
        ("saturday", "10:00 AM", "11:00 PM"),
        ("sunday", "10:00 AM", "8:00 PM")
    ]
    
    for day, opening, closing in hours_data:
        cursor.execute(
            "INSERT INTO hours (restaurant_id, day_of_week, opening_time, closing_time) VALUES (?, ?, ?, ?)",
            (restaurant_id, day, opening, closing)
        )
    
    # Insert restaurant tags
    tags = [
        "farm-to-table",
        "sustainable",
        "seasonal",
        "organic",
        "eco-friendly",
        "local ingredients",
        "health-conscious",
        "allergen-friendly"
    ]
    
    for tag in tags:
        cursor.execute(
            "INSERT INTO restaurant_tags (restaurant_id, tag) VALUES (?, ?)",
            (restaurant_id, tag)
        )
    
    # Insert amenities
    amenities = [
        "outdoor seating",
        "wheelchair accessible",
        "parking available",
        "wifi",
        "reservations accepted",
        "full bar",
        "private dining available"
    ]
    
    for amenity in amenities:
        cursor.execute(
            "INSERT INTO amenities (restaurant_id, amenity) VALUES (?, ?)",
            (restaurant_id, amenity)
        )
    
    # Insert social media
    social_media = [
        ("instagram", "@evergreenkitchen"),
        ("facebook", "EverGreenKitchenPDX"),
        ("twitter", "@EvergreenKitchn")
    ]
    
    for platform, handle in social_media:
        cursor.execute(
            "INSERT INTO social_media (restaurant_id, platform, handle) VALUES (?, ?, ?)",
            (restaurant_id, platform, handle)
        )
    
    # Insert sustainability practices
    practices = [
        "Locally sourced ingredients (within 100 miles when possible)",
        "Composting food waste",
        "Energy-efficient appliances and lighting",
        "Reusable/biodegradable to-go containers",
        "Water conservation practices",
        "Supporting regenerative agriculture"
    ]
    
    for practice in practices:
        cursor.execute(
            "INSERT INTO sustainability_practices (restaurant_id, practice) VALUES (?, ?)",
            (restaurant_id, practice)
        )
    
    # Insert special diets
    special_diets = [
        ("vegetarian", True),
        ("vegan", True),
        ("gluten_free", True),
        ("dairy_free", True),
        ("nut_free_options", True),
        ("keto_friendly", True),
        ("paleo_friendly", True)
    ]
    
    for diet, accommodated in special_diets:
        cursor.execute(
            "INSERT INTO special_diets (restaurant_id, diet_name, is_accommodated) VALUES (?, ?, ?)",
            (restaurant_id, diet, accommodated)
        )
    
    conn.commit()
    return restaurant_id

def insert_menu_data(conn, cursor, restaurant_id):
    """Insert mock menu data into the database"""
    
    # Insert menu categories
    categories = [
        ("Starters", 1),
        ("Entrees", 2),
        ("Desserts", 3)
    ]
    
    category_ids = {}
    
    for name, order in categories:
        cursor.execute(
            "INSERT INTO menu_categories (restaurant_id, name, display_order) VALUES (?, ?, ?)",
            (restaurant_id, name, order)
        )
        category_ids[name] = cursor.lastrowid
    
    # Insert menu items
    
    # Starters
    cursor.execute(
        "INSERT INTO menu_items (category_id, name, price, description, image_path) VALUES (?, ?, ?, ?, ?)",
        (
            category_ids["Starters"],
            "Roasted Beet Salad",
            12.95,
            "Locally sourced roasted beets with arugula, goat cheese, candied walnuts, and citrus vinaigrette",
            "beet_salad.jpg"
        )
    )
    beet_salad_id = cursor.lastrowid
    
    # Entrees
    cursor.execute(
        "INSERT INTO menu_items (category_id, name, price, description, image_path) VALUES (?, ?, ?, ?, ?)",
        (
            category_ids["Entrees"],
            "Plant-Based Buddha Bowl",
            16.95,
            "Seasonal roasted vegetables, quinoa, chickpeas, avocado, and tahini dressing on a bed of kale",
            "buddha_bowl.jpg"
        )
    )
    buddha_bowl_id = cursor.lastrowid
    
    cursor.execute(
        "INSERT INTO menu_items (category_id, name, price, description, image_path) VALUES (?, ?, ?, ?, ?)",
        (
            category_ids["Entrees"],
            "Wild Salmon with Herb Crust",
            24.95,
            "Pacific wild-caught salmon with herb crust, lemon-caper sauce, roasted fingerling potatoes and seasonal vegetables",
            "salmon_herb_crust.jpg"
        )
    )
    salmon_id = cursor.lastrowid
    
    cursor.execute(
        "INSERT INTO menu_items (category_id, name, price, description, image_path) VALUES (?, ?, ?, ?, ?)",
        (
            category_ids["Entrees"],
            "Grass-Fed Beef Tenderloin",
            32.95,
            "Locally sourced grass-fed beef with red wine reduction, truffle mashed potatoes, and roasted seasonal vegetables",
            "beef_tenderloin.jpg"
        )
    )
    beef_id = cursor.lastrowid
    
    # Desserts
    cursor.execute(
        "INSERT INTO menu_items (category_id, name, price, description, image_path) VALUES (?, ?, ?, ?, ?)",
        (
            category_ids["Desserts"],
            "Berry Compote Panna Cotta",
            9.95,
            "House-made coconut milk panna cotta topped with seasonal berry compote and mint",
            "panna_cotta.jpg"
        )
    )
    panna_cotta_id = cursor.lastrowid
    
    # Insert tags for each item
    item_tags = {
        beet_salad_id: ["vegetarian", "gluten-free", "low sodium", "antioxidant-rich"],
        buddha_bowl_id: ["vegan", "gluten-free", "high protein", "low cholesterol", "heart healthy"],
        salmon_id: ["high protein", "omega-3 rich", "gluten-free", "low carb", "pescatarian"],
        beef_id: ["high protein", "locally sourced", "iron-rich"],
        panna_cotta_id: ["vegan", "gluten-free", "dairy-free", "low sodium"]
    }
    
    for item_id, tags in item_tags.items():
        for tag in tags:
            cursor.execute(
                "INSERT INTO item_tags (item_id, tag) VALUES (?, ?)",
                (item_id, tag)
            )
    
    # Insert ingredients for each item
    ingredients = {
        beet_salad_id: [
            "organic red beets", "organic golden beets", "organic arugula", "goat cheese",
            "candied walnuts", "organic orange", "organic lemon juice", "olive oil",
            "dijon mustard", "local honey", "black pepper"
        ],
        buddha_bowl_id: [
            "organic kale", "organic quinoa", "organic chickpeas", "organic sweet potato",
            "organic broccoli", "organic red bell pepper", "organic avocado", "tahini",
            "lemon juice", "garlic", "olive oil", "sesame seeds", "sea salt", "black pepper"
        ],
        salmon_id: [
            "wild-caught Pacific salmon", "fresh parsley", "fresh dill", "fresh chives",
            "lemon zest", "garlic", "olive oil", "capers", "organic fingerling potatoes",
            "organic seasonal vegetables", "butter", "white wine", "sea salt", "black pepper"
        ],
        beef_id: [
            "grass-fed beef tenderloin", "organic russet potatoes", "organic butter", "organic cream",
            "truffle oil", "organic garlic", "organic seasonal vegetables", "red wine",
            "beef stock", "shallots", "fresh thyme", "olive oil", "sea salt", "black pepper"
        ],
        panna_cotta_id: [
            "coconut milk", "agar-agar", "organic cane sugar", "vanilla bean",
            "seasonal organic berries", "organic lemon juice", "fresh mint"
        ]
    }
    
    for item_id, item_ingredients in ingredients.items():
        for ingredient in item_ingredients:
            cursor.execute(
                "INSERT INTO ingredients (item_id, name) VALUES (?, ?)",
                (item_id, ingredient)
            )
    
    # Insert nutritional information for each item
    nutrition_data = [
        (
            beet_salad_id, "1 salad (220g)", 320, 21, 6, 0, 15, 210, 24, 5, 16, 9, 0, 12, 8, 15,
            ["dairy", "nuts"]
        ),
        (
            buddha_bowl_id, "1 bowl (410g)", 580, 26, 3.5, 0, 0, 380, 72, 18, 10, 22, 0, 15, 30, 25,
            ["sesame"]
        ),
        (
            salmon_id, "1 entree (380g)", 490, 22, 5, 0, 95, 420, 28, 4, 3, 42, 120, 8, 15, 24,
            ["fish", "dairy"]
        ),
        (
            beef_id, "1 entree (400g)", 720, 38, 18, 0.5, 140, 580, 42, 6, 5, 48, 4, 10, 35, 28,
            ["dairy"]
        ),
        (
            panna_cotta_id, "1 dessert (150g)", 280, 18, 16, 0, 0, 30, 30, 3, 24, 2, 0, 6, 8, 6,
            ["coconut"]
        )
    ]
    
    for (
        item_id, serving_size, calories, total_fat, saturated_fat, trans_fat, 
        cholesterol, sodium, total_carbs, dietary_fiber, sugars, protein,
        vitamin_d, calcium, iron, potassium, allergens
    ) in nutrition_data:
        cursor.execute(
            """
            INSERT INTO nutrition (
                item_id, serving_size, calories, total_fat, saturated_fat, trans_fat,
                cholesterol, sodium, total_carbs, dietary_fiber, sugars, protein,
                vitamin_d, calcium, iron, potassium
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_id, serving_size, calories, total_fat, saturated_fat, trans_fat,
                cholesterol, sodium, total_carbs, dietary_fiber, sugars, protein,
                vitamin_d, calcium, iron, potassium
            )
        )
        
        for allergen in allergens:
            cursor.execute(
                "INSERT INTO allergens (item_id, allergen) VALUES (?, ?)",
                (item_id, allergen)
            )
    
    conn.commit()

def query_and_display_data(cursor):
    """Query and display data from the database"""
    
    print("\n=== RESTAURANT INFORMATION ===")
    cursor.execute("""
    SELECT name, slogan, description, address, city, state, country, phone, email, website
    FROM restaurant
    """)
    restaurant = cursor.fetchone()
    print(f"Name: {restaurant[0]}")
    print(f"Slogan: {restaurant[1]}")
    print(f"Description: {restaurant[2]}")
    print(f"Address: {restaurant[3]}, {restaurant[4]}, {restaurant[5]}, {restaurant[6]}")
    print(f"Contact: {restaurant[7]} | {restaurant[8]} | {restaurant[9]}")
    
    print("\n=== HOURS OF OPERATION ===")
    cursor.execute("""
    SELECT day_of_week, opening_time, closing_time
    FROM hours
    ORDER BY CASE 
        WHEN day_of_week = 'monday' THEN 1
        WHEN day_of_week = 'tuesday' THEN 2
        WHEN day_of_week = 'wednesday' THEN 3
        WHEN day_of_week = 'thursday' THEN 4
        WHEN day_of_week = 'friday' THEN 5
        WHEN day_of_week = 'saturday' THEN 6
        WHEN day_of_week = 'sunday' THEN 7
    END
    """)
    hours = cursor.fetchall()
    for day, opening, closing in hours:
        print(f"{day.capitalize()}: {opening} - {closing}")
    
    print("\n=== MENU ===")
    cursor.execute("""
    SELECT mc.name as category, mi.name, mi.price, mi.description
    FROM menu_categories mc
    JOIN menu_items mi ON mc.id = mi.category_id
    ORDER BY mc.display_order, mi.name
    """)
    menu_items = cursor.fetchall()
    current_category = ""
    for category, name, price, description in menu_items:
        if category != current_category:
            print(f"\n--- {category} ---")
            current_category = category
        print(f"{name} - ${price:.2f}")
        print(f"  {description}")
        
        # Get tags for this item
        cursor.execute("""
        SELECT it.tag 
        FROM item_tags it
        JOIN menu_items mi ON it.item_id = mi.id
        WHERE mi.name = ?
        """, (name,))
        tags = cursor.fetchall()
        tag_list = ", ".join([tag[0] for tag in tags])
        print(f"  Tags: {tag_list}")
        
        # Get ingredients for this item
        cursor.execute("""
        SELECT i.name 
        FROM ingredients i
        JOIN menu_items mi ON i.item_id = mi.id
        WHERE mi.name = ?
        """, (name,))
        ingredients = cursor.fetchall()
        print(f"  Ingredients: {', '.join([ing[0] for ing in ingredients])}")
        
        # Get nutrition information for this item
        cursor.execute("""
        SELECT serving_size, calories, total_fat, saturated_fat, trans_fat,
               cholesterol, sodium, total_carbs, dietary_fiber, sugars, protein
        FROM nutrition n
        JOIN menu_items mi ON n.item_id = mi.id
        WHERE mi.name = ?
        """, (name,))
        nutrition = cursor.fetchone()
        if nutrition:
            print(f"  Nutrition (per {nutrition[0]}):")
            print(f"    Calories: {nutrition[1]}, Fat: {nutrition[2]}g (Sat: {nutrition[3]}g, Trans: {nutrition[4]}g)")
            print(f"    Cholesterol: {nutrition[5]}mg, Sodium: {nutrition[6]}mg")
            print(f"    Carbs: {nutrition[7]}g (Fiber: {nutrition[8]}g, Sugars: {nutrition[9]}g)")
            print(f"    Protein: {nutrition[10]}g")
        
        # Get allergens for this item
        cursor.execute("""
        SELECT a.allergen 
        FROM allergens a
        JOIN menu_items mi ON a.item_id = mi.id
        WHERE mi.name = ?
        """, (name,))
        allergens = cursor.fetchall()
        if allergens:
            print(f"  Allergens: {', '.join([alg[0] for alg in allergens])}")
        
        print()

def main():
    # Check if database exists, if so delete it for fresh start
    db_path = 'restaurant.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create database schema
        create_tables(cursor)
        print("Created database tables")
        
        # Insert restaurant data
        restaurant_id = insert_restaurant_data(conn, cursor)
        print(f"Inserted restaurant data with ID: {restaurant_id}")
        
        # Insert menu data
        insert_menu_data(conn, cursor, restaurant_id)
        print("Inserted menu data")
        
        # Display the data
        query_and_display_data(cursor)
        
        print(f"\nDatabase created successfully at {db_path}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()