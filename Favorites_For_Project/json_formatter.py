# Functional (sorta): analyzes json data from image scrape to categorize items
import json
import re
import unicodedata

def clean_text(text):
    """
    Clean and normalize text by removing extra whitespace, 
    normalizing unicode characters, and stripping non-printable characters.
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove non-printable characters and extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_menu_items(raw_text):
    """
    Extract menu items and their prices from the raw text.
    """
    # Remove newline characters and extra spaces
    cleaned_text = raw_text.replace('\n', ' ')
    
    # Regex pattern to match menu items and prices
    # This pattern looks for:
    # 1. Item name (capturing words until a price or end of line)
    # 2. Optional price (with or without decimal, including market price 'MKT')
    menu_items = []
    
    # Split the text into lines and process each line
    lines = cleaned_text.split(' ')
    current_item = []
    current_price = None
    
    for word in lines:
        # Check if word is a price
        price_match = re.match(r'^(\d+(?:\.\d+)?|MKT)$', word)
        
        if price_match:
            # If we were building an item, finalize it
            if current_item:
                item_name = ' '.join(current_item).strip()
                menu_items.append({
                    'name': clean_text(item_name),
                    'price': word
                })
                current_item = []
                current_price = word
        else:
            # Not a price, so add to current item
            current_item.append(word)
    
    # Handle any remaining item
    if current_item:
        item_name = ' '.join(current_item).strip()
        menu_items.append({
            'name': clean_text(item_name),
            'price': current_price
        })
    
    return menu_items

def categorize_menu_items(menu_items):
    """
    Categorize menu items into sections.
    """
    sections = {
        'Appetizers': [],
        'Salads': [],
        'Sandwiches': [],
        'Mains': [],
        'Sides': [],
        'Desserts': [],
        'Other': []
    }
    
    # Keywords to identify sections
    section_keywords = {
        'Appetizers': ['appetizers', 'wings', 'eggs', 'cakes'],
        'Salads': ['salad', 'kale'],
        'Sandwiches': ['sandwich', 'toast'],
        'Mains': ['hash', 'waffle', 'scramble', 'gumbo', 'pasta', 'steak'],
        'Sides': ['sides', 'tots', 'potatoes', 'grits'],
        'Desserts': ['desserts', 'pudding', 'cake', 'pie', 'cheesecake']
    }
    
    for item in menu_items:
        categorized = False
        for section, keywords in section_keywords.items():
            if any(keyword in item['name'].lower() for keyword in keywords):
                sections[section].append(item)
                categorized = True
                break
        
        if not categorized:
            sections['Other'].append(item)
    
    return {k: v for k, v in sections.items() if v}

def analyze_menu(file_path):
    """
    Main function to analyze the menu JSON file.
    """
    # Read the JSON file
    with open(file_path, 'r') as f:
        menu_data = json.load(f)
    
    # Extract raw text
    raw_text = menu_data.get('raw_text', '')
    
    # Extract menu items
    menu_items = extract_menu_items(raw_text)
    
    # Categorize menu items
    categorized_menu = categorize_menu_items(menu_items)
    
    # Update the JSON with extracted data
    menu_data['menu_items'] = menu_items
    menu_data['menu_sections'] = categorized_menu
    menu_data['total_items'] = len(menu_items)
    
    # Write back to the file
    with open(file_path, 'w') as f:
        json.dump(menu_data, f, indent=4)
    
    # Print summary
    print("Menu Analysis Summary:")
    print(f"Total Menu Items: {len(menu_items)}")
    for section, items in categorized_menu.items():
        print(f"{section}: {len(items)} items")
    
    return menu_data

# Usage
if __name__ == "__main__":
    analyze_menu('menu_analysis.json')