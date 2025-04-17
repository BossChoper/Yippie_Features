import requests
from bs4 import BeautifulSoup
import re

def scrape_yelp_menu(url):
    """ 
    Scrapes menu data from a Yelp restaurant page.

    Args:
        url (str): URL of the Yelp menu page

    Returns:
        dict: Structured menu data with sections as keys and items as values
        """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        menu = {}

        # Find all sections of the menu as h2 headings
        sections = soup.find_all('h2', class_=lambda x: x!= 'hidden')

        for section in sections:
            section_title = section.get_text(strip=True)
            menu[section_title] = []

            next_section = section.find_next('h2')
            current_element = section.next_sibling

            while current_element and current_element != next_section:
                if current_element.name == 'h4':
                    item = {'name': '', 'description': '', 'price': ''}
                    item['name'] = current_element.get_text(strip=True)

                    # Process siblings until next item
                    desc_element = []
                    price_found = False

                    sibling = current_element.next_sibling
                    while sibling == sibling.name not in ['h2', 'h4']:
                        text = sibling.get_text(strip=True)

                        # Price detection pattern
                        if re.match(r'^-?\$?\d+\.\d{2}$', text.replace(' ', '')):
                            item['price'] = text.replace('- ', '').strip()
                            price_found = True
                            break

                        if text:
                            desc_elements.append(text)
                        sibling = sibling.next_sibling
                    
                    # Handle descriptions
                    if desc_elements:
                        item['description'] = ' '.join(desc_elements)

                        # Extract calories and allergens from description
                        calories = re.search(r'\((\d+ cal)', item['description'])
                        allergens = re.findall(r'Contains: ([\w\s,\(\)]+)', item['description'])

                        if calories:
                            item['calories'] = calories.group(1)
                        if allergens:
                            items['allergens'] = [a.strip() for a in allergens[0].split(',')]
                    
                    menu[section_title].append(item)
                current_element = current_element.next_sibling if current_element else None
        
        return menu

    except Exception as e:
        print(f"Error scraping menu: {e}")
        return None

# Usage example
url = "https://www.yelp.com/menu/tatte-bakery-and-cafe-washington-2"
menu_data = scrape_yelp_menu(url)

if menu_data:
    for section, items in menu_data.items():
        print(f"\n## {section}")
        for item in items:
            print(f"\nItem: {item['name']}")
            if item.get('description'):
                print(f"Description: {item['description']}")
            if item.get('calories'):
                print(f"Calories: {item['calories']}")
            if item.get('allergens'):
                print(f"Allergens: {', '.join(item['allergens'])}")
            print(f"Price: {item['price']}")
else:
    print("Failed to retrieve menu data")

""" Example output:
Enter: python GetMenuDataYelp.py
## Breakfast All Day
## Shaks & Plates
## Tartines & Sandwiches
## Salads & Soups
## Beverages
## Bakery
## Desserts, Cookies, & Nuts
## Tatte Pantry
## Gluten Friendly
## What's Popular Here?
