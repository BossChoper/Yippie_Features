import requests
from bs4 import BeautifulSoup

def scrape_jamaican_menu(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        menu_items = []
        
        # Find all menu item containers
        items = soup.find_all('div', class_='menu-item')
        
        for item in items:
            # Extract name from menu-title
            name = item.find('div', class_='menu-title')
            name = name.get_text(strip=True) if name else "N/A"
            
            # Extract description from menu-descr
            desc = item.find('div', class_='menu-descr')
            desc = desc.get_text(strip=True) if desc else "No description available"
            
            menu_items.append({
                'name': name,
                'description': desc
            })
        
        return menu_items if menu_items else None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    menu_url = "https://www.restaurantji.com/md/silver-spring/negril-the-jamaican-eatery-/menu/"
    jamaican_menu = scrape_jamaican_menu(menu_url)
    
    if jamaican_menu:
        print("JAMAICAN MENU ITEMS:\n")
        for idx, item in enumerate(jamaican_menu, 1):
            print(f"{idx}. {item['name']}")
            print(f"   {item['description']}\n")
    else:
        print("Failed to retrieve menu items.")

""" Example output (using Negril on RestaurantJi + perplexity)
Jerk Chicken Dinner
   Jerk chicken made with our signature spices and sauce, on rice & peas and cabbage.

2. Fried Plantain
   Fried yellow sweet plantains. Vegetarian.

3. Oxtail Dinner
   Oxtails stewed in a blend of spices and herbs, carrots, beans, spinners (mini dumplings), on rice & peas and cabbage.

4. Curried Chicken Dinner
   Chicken simmered in our special curry blend, on rice & peas and cabbage. *dark meat
   """