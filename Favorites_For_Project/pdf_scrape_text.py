# Functional; extracts text from pdf (yelp page)
# perplexity creates scripts for specific web pages
import re
from io import BytesIO
from pdfminer.high_level import extract_text

def extract_menu_items_from_text(text):
    """
    Extracts menu items from a given text, filtering out prices and calorie counts.
    """
    lines = text.splitlines()
    menu_items = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'^\$\d+\.\d{2}$', line):  # Skip lines that are just prices
            continue
        if re.search(r'\((\d+)\s*cal', line, re.IGNORECASE):  # Skip lines with calorie counts
            continue
        if re.search(r'Contains:', line, re.IGNORECASE):  # Skip "Contains" lines
            continue
        if line.lower() in ['menu', 'what\'s popular here?', 'yelp for business', 'write a review',
                         'restaurants', 'home services', 'auto services', 'more', 'beverages',
                         'tartines & sandwiches', 'shaks & plates', 'salads & soups', 'breakfast all day',
                         'tatte bakery & cafe - menu - washington', 'menu may not be up to date. submit corrections.',
                         'iced ginger date oatmilk latte 16 oz', 'orange coriander matcha soda 16oz', 'sparkling matcha lemonade 16 oz',
                         'iced black sesame latte - 16 oz', 'iced pistachio latte - 16 oz', 'iced honey halva latte - 12 oz',
                         'double espresso', 'cappuccino', 'macchiato', 'cortado', 'flat white - 8 oz', 'decaf black sesame latte - 12 oz',
                         'decaf pistachio latte - 12 oz', 'decaf honey halva latte - 12 oz', 'decaf cappuccino', 'decaf cortado',
                         'decaf macchiato', 'decaf flat white - 8 oz', 'iced decaf black sesame latte - 16 oz', 'iced decaf pistachio latte - 16 oz',
                         'blood orange hibiscus tea', 'apple berry tea' ]: # Skip titles and Yelp-related text
            continue
        if re.search(r'\d+\s+of\s+\d+', line):  # Skip page numbers
            continue
        if re.search(r'https?://', line):  # Skip URLs
            continue
        menu_items.append(line)
    return '\n'.join(menu_items)

def extract_menu_from_pdf_path(pdf_path):
    """
    Extracts the menu items from a PDF file given its file path.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            text = extract_text(pdf_file)
            menu_items = extract_menu_items_from_text(text)
            return menu_items
    except FileNotFoundError:
        return f"Error: File not found at path: {pdf_path}"
    except Exception as e:
        return f"Error processing PDF: {e}"

# Main execution
pdf_path = "/Users/mkonteh88/Desktop/Yippee_Dev/Yippee_Testing/Menu_Scraping/Tatte Bakery & Cafe - Menu - Washington.pdf"  # Replace with the actual path to your PDF file
menu = extract_menu_from_pdf_path(pdf_path)

if "Error" in menu:
    # If there was an error, print the error message
    print(menu)
else:
    # Otherwise, print the extracted menu
    print(menu)

""" Works: Perplexity AI
Bread & Butter
Toasted housemade bread served with butter and housemade jam.
Potato, Mushroom, & Bacon Shakshuka
Potato sauce, baby spinach, shiitake, and button mushrooms,
poached egg topped with bacon, parsley relish, garlic Aleppo
oil, grated parmesan, and fresh parsley served with housemade
1 photo
Traditional Shakshuka
Traditional North African dish of eggs poached in a tomato sauce
with chili, bell peppers, and onions spiced with cumin and topped
with feta and parsley. Served with housemade challah
7 reviews
4 photos
Lamb Meatball & Labneh Shakshuka
Tomato and bell pepper sauce, eggs, lamb meatballs, and
peppadew peppers topped with spicy labneh and parsley. Served
1 photo
Maple Aleppo Chicken
Aleppo pepper and maple spiced chicken served with jasmine rice,
chickpeas, dried apricots, roasted pearl onions, and
1 review
"""
