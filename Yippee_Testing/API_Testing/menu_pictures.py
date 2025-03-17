# NON FUNCTIONAL
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
YELP_API_KEY = os.getenv("YELP_API_KEY")  # Not used here, but included for future compatibility

# Target URL: Panera Bread menu page
BASE_URL = "https://www.panerabread.com/en-us/menu.html"

def setup_driver():
    """Set up headless Chrome driver for Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_menu_pictures():
    """Scrape menu items and at least 3 pictures per item from Panera Bread's website."""
    driver = setup_driver()
    driver.get(BASE_URL)
    
    # Wait and scroll incrementally to load all content
    driver.implicitly_wait(20)
    for _ in range(3):  # Scroll 3 times to ensure full load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait 2 seconds between scrolls
    
    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Broaden search: any div with an img and a title-like tag
    potential_items = soup.find_all("div", recursive=True)
    menu_items = [item for item in potential_items if item.find("img") and (item.find("h3") or item.find("h4") or item.find("span"))]
    
    if not menu_items:
        print("No menu items found. The site structure may have changed.")
        print("Here's a larger snippet of the HTML for debugging:")
        print(soup.prettify()[:5000])  # Increased to 5000 chars
        return

    # Store results in a dictionary: {item_name: [image_urls]}
    menu_data = {}
    
    for item in menu_items:
        # Extract item name
        name_tag = item.find("h3") or item.find("h4") or item.find("span")
        if not name_tag:
            continue
        item_name = name_tag.get_text(strip=True)
        
        # Extract images
        image_tag = item.find("img")
        image_urls = []
        
        if image_tag and image_tag.get("src"):
            src = image_tag["src"]
            # Ensure full URL
            if not src.startswith("http"):
                src = "https://www.panerabread.com" + src
            image_urls.append(src)
        
        # If fewer than 3 images, add placeholders
        while len(image_urls) < 3:
            image_urls.append("No additional image found")
        
        menu_data[item_name] = image_urls[:3]

    # Print results
    for item_name, images in menu_data.items():
        print(f"\nMenu Item: {item_name}")
        for i, url in enumerate(images, 1):
            print(f"  Picture {i}: {url}")

if __name__ == "__main__":
    print("Starting Menu Pictures Program...")
    scrape_menu_pictures()

"""
\\ Example output:
Starting Menu Pictures Program...

Menu Item: Big Mac
  Picture 1: https://www.mcdonalds.com/is/image/content/dam/usa/nfl/food/BigMac.jpg
  Picture 2: No additional image found
  Picture 3: No additional image found

Menu Item: McChicken
  Picture 1: https://www.mcdonalds.com/is/image/content/dam/usa/nfl/food/McChicken.jpg
  Picture 2: No additional image found
  Picture 3: No additional image found
  \\
"""

# Picture and menu item web scraper
# Useful for retrieving basic items in menus at restaurants
