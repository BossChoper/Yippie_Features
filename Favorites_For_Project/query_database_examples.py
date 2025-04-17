"""
Example queries for the restaurant database
"""
# Runs and gets queries for a restaurant database
# Functional
import sqlite3
from pprint import pprint

def run_query_examples():
    # Connect to the database
    conn = sqlite3.connect('restaurant_data.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    c = conn.cursor()
    
    print("\n1. Basic restaurant information:")
    c.execute('''
    SELECT name, slogan, average_rating, total_reviews
    FROM restaurant
    ''')
    pprint(dict(c.fetchone()))

    print("\n2. Restaurant location and hours:")
    c.execute('''
    SELECT l.address, l.city, l.state, h.day, h.opening_time, h.closing_time
    FROM location l
    JOIN restaurant r ON r.id = l.restaurant_id
    JOIN hours h ON h.restaurant_id = r.id
    ORDER BY 
        CASE h.day
            WHEN 'monday' THEN 1
            WHEN 'tuesday' THEN 2
            WHEN 'wednesday' THEN 3
            WHEN 'thursday' THEN 4
            WHEN 'friday' THEN 5
            WHEN 'saturday' THEN 6
            WHEN 'sunday' THEN 7
        END
    ''')
    for row in c.fetchall():
        print(f"{row['address']}, {row['city']}, {row['state']} - "
              f"{row['day'].title()}: {row['opening_time']} - {row['closing_time']}")

    print("\n3. Menu items with prices by category:")
    c.execute('''
    SELECT mc.name as category, mi.name, mi.price, mi.description
    FROM menu_categories mc
    JOIN menu_items mi ON mi.category_id = mc.id
    ORDER BY mc.display_order, mi.name
    ''')
    current_category = None
    for row in c.fetchall():
        if current_category != row['category']:
            current_category = row['category']
            print(f"\n{current_category}:")
        print(f"  {row['name']} - ${row['price']:.2f}")
        print(f"    {row['description']}")

    print("\n4. Vegan and gluten-free menu items:")
    c.execute('''
    SELECT DISTINCT mi.name, mi.price
    FROM menu_items mi
    JOIN item_tags it ON it.item_id = mi.id
    WHERE it.tag IN ('vegan', 'gluten-free')
    GROUP BY mi.id
    HAVING COUNT(DISTINCT it.tag) = 2
    ORDER BY mi.price
    ''')
    print("Items that are both vegan and gluten-free:")
    for row in c.fetchall():
        print(f"- {row['name']} (${row['price']:.2f})")

    print("\n5. Nutritional information for menu items:")
    c.execute('''
    SELECT mi.name,
           nf.serving_size,
           nf.calories,
           nf.protein,
           nf.total_carbs,
           nf.total_fat
    FROM menu_items mi
    JOIN nutrition_facts nf ON nf.item_id = mi.id
    ORDER BY nf.calories DESC
    ''')
    print("Nutritional Information (per serving):")
    for row in c.fetchall():
        print(f"\n{row['name']}:")
        print(f"  Serving Size: {row['serving_size']}")
        print(f"  Calories: {row['calories']}")
        print(f"  Protein: {row['protein']}g")
        print(f"  Carbs: {row['total_carbs']}g")
        print(f"  Fat: {row['total_fat']}g")

    print("\n6. Menu items with their ingredients:")
    c.execute('''
    SELECT mi.name, GROUP_CONCAT(i.ingredient, ', ') as ingredients
    FROM menu_items mi
    JOIN ingredients i ON i.item_id = mi.id
    GROUP BY mi.id
    ''')
    print("Ingredients by dish:")
    for row in c.fetchall():
        print(f"\n{row['name']}:")
        print(f"  {row['ingredients']}")

    print("\n7. Review distribution:")
    c.execute('''
    SELECT rating_level, count,
           ROUND(count * 100.0 / SUM(count) OVER (), 1) as percentage
    FROM review_summary
    ORDER BY rating_level DESC
    ''')
    print("Rating distribution:")
    for row in c.fetchall():
        stars = '★' * row['rating_level']
        print(f"{stars:<5} {row['count']} reviews ({row['percentage']}%)")

    print("\n8. Sustainability practices and special diets:")
    c.execute('''
    SELECT 'Sustainability' as category, practice as item
    FROM sustainability_practices
    UNION ALL
    SELECT 'Special Diets' as category,
           diet_name || CASE WHEN available THEN ' (Available)' ELSE ' (Unavailable)' END as item
    FROM special_diets
    ORDER BY category, item
    ''')
    current_category = None
    for row in c.fetchall():
        if current_category != row['category']:
            current_category = row['category']
            print(f"\n{current_category}:")
        print(f"- {row['item']}")

    conn.close()

if __name__ == "__main__":
    run_query_examples()

""" Example output:

1. Basic restaurant information:
{'average_rating': 4.7,
 'name': 'Evergreen Kitchen',
 'slogan': 'Farm to Table, Sustainably Crafted',
 'total_reviews': 342}

2. Restaurant location and hours:
427 Oak Street, Portland, Oregon - Monday: 11:00 AM - 9:00 PM
427 Oak Street, Portland, Oregon - Tuesday: 11:00 AM - 9:00 PM
427 Oak Street, Portland, Oregon - Wednesday: 11:00 AM - 9:00 PM
427 Oak Street, Portland, Oregon - Thursday: 11:00 AM - 10:00 PM
427 Oak Street, Portland, Oregon - Friday: 11:00 AM - 11:00 PM
427 Oak Street, Portland, Oregon - Saturday: 10:00 AM - 11:00 PM
427 Oak Street, Portland, Oregon - Sunday: 10:00 AM - 8:00 PM

3. Menu items with prices by category:

Starters:
  Roasted Beet Hummus - $12.00
    House-made hummus with roasted organic beets, served with fresh vegetables and gluten-free crackers

Main Courses:
  Quinoa Buddha Bowl - $18.00
    Organic quinoa with roasted seasonal vegetables, avocado, sprouts, and tahini dressing

4. Vegan and gluten-free menu items:
Items that are both vegan and gluten-free:
- Roasted Beet Hummus ($12.00)
- Quinoa Buddha Bowl ($18.00)

5. Nutritional information for menu items:
Nutritional Information (per serving):

Quinoa Buddha Bowl:
  Serving Size: 400g
  Calories: 520
  Protein: 18.0g
  Carbs: 68.0g
  Fat: 22.0g

Roasted Beet Hummus:
  Serving Size: 200g
  Calories: 280
  Protein: 10.0g
  Carbs: 32.0g
  Fat: 14.0g

6. Menu items with their ingredients:
Ingredients by dish:

Roasted Beet Hummus:
  chickpeas, beets, tahini, lemon juice, garlic, olive oil

Quinoa Buddha Bowl:
  quinoa, sweet potato, kale, chickpeas, avocado, sprouts, tahini

7. Review distribution:
Rating distribution:
★★★★★ 180 reviews (52.6%)
★★★★  120 reviews (35.1%)
★★★   30 reviews (8.8%)
★★    8 reviews (2.3%)
★     4 reviews (1.2%)

8. Sustainability practices and special diets:

Special Diets:
- dairy-free (Available)
- gluten-free (Available)
- keto (Unavailable)
- paleo (Available)
- vegan (Available)
- vegetarian (Available)

Sustainability:
- composting program
- eco-friendly packaging
- local sourcing
- renewable energy usage
- water conservation
- zero-waste initiatives
"""