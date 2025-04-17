# NON FUNCTIONAL
import os
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_database():
    """Create SQLite database and tables if they don't exist"""
    conn = sqlite3.connect('restaurant_menu.db')
    cursor = conn.cursor()
    
    # Create menu items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        category TEXT,
        date_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    return conn, cursor

def clear_existing_data(cursor, conn):
    """Clear existing menu data before adding new data"""
    cursor.execute("DELETE FROM menu_items")
    conn.commit()
    print("Cleared existing menu data")

def scrape_menu(url):
    """Scrape menu items and prices from the Google restaurant listing"""
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Setup WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"Accessing {url}")
        driver.get(url)
        time.sleep(5)  # Give time for page to load
        
        # Try to find and click on the menu button
        try:
            # Wait for the menu button to be clickable
            menu_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Menu') or contains(., 'menu')]"))
            )
            menu_button.click()
            print("Clicked on menu button")
            time.sleep(3)  # Wait for menu to load
        except Exception as e:
            print(f"Could not find menu button: {e}")
            print("Attempting to find menu items directly...")
        
        # Initialize results
        menu_items = []
        
        # Look for menu items
        # This selector may need adjustment based on the actual structure
        sections = driver.find_elements(By.CSS_SELECTOR, "div[role='tabpanel']")
        
        if not sections:
            sections = driver.find_elements(By.CSS_SELECTOR, "div.m6QErb")
            
        for section in sections:
            try:
                category_elem = section.find_element(By.CSS_SELECTOR, "h2, h3")
                category = category_elem.text
            except:
                category = "Uncategorized"
            
            # Look for menu items in this section
            items = section.find_elements(By.CSS_SELECTOR, "div.GHmjSc, div.FLiGse")
            
            for item in items:
                try:
                    name_elem = item.find_element(By.CSS_SELECTOR, "div.PflGfe, div.O7guHb")
                    name = name_elem.text
                    
                    try:
                        price_elem = item.find_element(By.CSS_SELECTOR, "div.e7Rrle, div.NIL5qe")
                        price_text = price_elem.text.strip().replace('$', '')
                        price = float(price_text) if price_text else None
                    except:
                        price = None
                    
                    menu_items.append({
                        'name': name,
                        'price': price,
                        'category': category
                    })
                    
                except Exception as e:
                    print(f"Error parsing menu item: {e}")
        
        print(f"Found {len(menu_items)} menu items")
        return menu_items
    
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []
    
    finally:
        driver.quit()

def save_to_database(menu_items, cursor, conn):
    """Save the scraped menu items to the database"""
    for item in menu_items:
        cursor.execute(
            "INSERT INTO menu_items (name, price, category) VALUES (?, ?, ?)",
            (item['name'], item['price'], item['category'])
        )
    
    conn.commit()
    print(f"Saved {len(menu_items)} menu items to database")

def main():
    # Restaurant URL
    url = "https://g.co/kgs/k9HcRo9"
    
    # Setup database
    conn, cursor = setup_database()
    
    try:
        # Clear existing data
        clear_existing_data(cursor, conn)
        
        # Scrape menu
        menu_items = scrape_menu(url)
        
        if menu_items:
            # Save to database
            save_to_database(menu_items, cursor, conn)
            
            # Display results
            print("\nMenu items saved to database:")
            cursor.execute("SELECT name, price, category FROM menu_items")
            for name, price, category in cursor.fetchall():
                price_display = f"${price:.2f}" if price is not None else "Price not available"
                print(f"{name} - {price_display} - Category: {category}")
        else:
            print("No menu items were found")
    
    finally:
        # Close database connection
        conn.close()

if __name__ == "__main__":
    main()