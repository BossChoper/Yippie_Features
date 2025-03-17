import requests
from bs4 import BeautifulSoup
import os
import re
import time
from urllib.parse import urljoin, urlparse
import argparse
import json

class RestaurantScraper:
    def __init__(self, base_url, output_folder="scraped_data"):
        """Initialize the scraper with the restaurant website URL."""
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        self.output_folder = output_folder
        self.food_items = []
        
        # Create output directories if they don't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if not os.path.exists(os.path.join(output_folder, "images")):
            os.makedirs(os.path.join(output_folder, "images"))
    
    def get_soup(self, url):
        """Fetch a web page and return its BeautifulSoup object."""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def find_menu_page(self):
        """Attempt to locate the menu page if we're starting from the homepage."""
        soup = self.get_soup(self.base_url)
        if not soup:
            return None
        
        # Common menu page link patterns
        menu_keywords = ["menu", "food", "dishes", "cuisine", "order"]
        
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            link_text = link.text.lower()
            
            # Check if any keywords are in the link text or href
            if any(keyword in link_text or keyword in href.lower() for keyword in menu_keywords):
                full_url = urljoin(self.base_url, href)
                print(f"Found potential menu page: {full_url}")
                return full_url
        
        # If no specific menu page is found, just use the base URL
        return self.base_url
    
    def scrape_food_items(self, url=None):
        """Scrape food items (names, descriptions, prices) from the menu page."""
        if url is None:
            url = self.find_menu_page()
            if not url:
                print("Couldn't find a menu page. Using the base URL.")
                url = self.base_url
        
        soup = self.get_soup(url)
        if not soup:
            return []
        
        # Common patterns for menu items
        # This is challenging without knowing the specific restaurant website structure
        # We'll look for common patterns
        
        # Method 1: Look for structured menu items
        menu_items = soup.find_all(["div", "article", "section"], class_=re.compile(r"(menu-item|dish|food|product)"))
        
        # Method 2: Look for list items that might contain food
        if not menu_items:
            menu_items = soup.find_all("li", class_=re.compile(r"(menu-item|dish|food|product)"))
        
        # Method 3: Look for headings with nearby prices
        if not menu_items:
            headings = soup.find_all(["h2", "h3", "h4", "strong"], string=re.compile(r"[A-Za-z\s]{3,}"))
            menu_items = []
            for heading in headings:
                # Look for nearby price patterns
                price_text = None
                for sibling in heading.find_next_siblings():
                    price_match = re.search(r'(\$\d+\.?\d*|\d+\.?\d*\$|\d+\.?\d*\s(USD|dollars))', sibling.text)
                    if price_match:
                        price_text = price_match.group(0)
                        break
                
                if price_text:
                    menu_items.append({
                        "name": heading.text.strip(),
                        "price": price_text,
                        "description": heading.find_next("p").text.strip() if heading.find_next("p") else ""
                    })
        
        # Process and store the food items
        for item in menu_items:
            food_item = {}
            
            # Extract name, price, and description based on the item structure
            if isinstance(item, dict):
                food_item = item
            else:
                # Try to extract name, price, description from HTML elements
                name_elem = item.find(["h2", "h3", "h4", "strong", "span", "div"], class_=re.compile(r"(name|title)"))
                price_elem = item.find(["span", "div", "p"], class_=re.compile(r"(price|cost)"))
                desc_elem = item.find(["p", "div", "span"], class_=re.compile(r"(desc|description|info)"))
                
                food_item["name"] = name_elem.text.strip() if name_elem else item.text.strip()
                food_item["price"] = price_elem.text.strip() if price_elem else ""
                food_item["description"] = desc_elem.text.strip() if desc_elem else ""
                
                # Try to extract price using regex if not found through class
                if not food_item["price"]:
                    price_match = re.search(r'(\$\d+\.?\d*|\d+\.?\d*\$|\d+\.?\d*\s(USD|dollars))', item.text)
                    if price_match:
                        food_item["price"] = price_match.group(0)
            
            # Clean up the data
            food_item["name"] = re.sub(r'\s+', ' ', food_item.get("name", "")).strip()
            food_item["price"] = re.sub(r'\s+', ' ', food_item.get("price", "")).strip()
            food_item["description"] = re.sub(r'\s+', ' ', food_item.get("description", "")).strip()
            
            if food_item["name"] and not food_item["name"].isspace():
                self.food_items.append(food_item)
        
        return self.food_items
    
    def scrape_food_images(self, url=None):
        """Scrape images that are likely to be food photos."""
        if url is None:
            url = self.find_menu_page()
            if not url:
                url = self.base_url
        
        soup = self.get_soup(url)
        if not soup:
            return []
        
        # Find all images
        images = soup.find_all("img")
        downloaded_images = []
        
        # Keywords likely to appear in food image filenames or alt text
        food_keywords = ["food", "dish", "menu", "meal", "plate", "cuisine", "burger", "pizza", "pasta", 
                        "salad", "appetizer", "dessert", "breakfast", "lunch", "dinner"]
        
        for img in images:
            src = img.get("src")
            if not src:
                continue
                
            # Make the URL absolute
            img_url = urljoin(url, src)
            
            # Skip tiny images, icons, or logos
            if img.get("width") and int(img.get("width")) < 100:
                continue
            if img.get("height") and int(img.get("height")) < 100:
                continue
            
            # Check if this is likely a food image based on alt text or filename
            alt_text = img.get("alt", "").lower()
            filename = os.path.basename(urlparse(img_url).path).lower()
            
            is_likely_food = False
            # Check alt text for food keywords
            if any(keyword in alt_text for keyword in food_keywords):
                is_likely_food = True
            # Check filename for food keywords
            elif any(keyword in filename for keyword in food_keywords):
                is_likely_food = True
            # If image is in a container with menu-related class
            elif img.parent and any(keyword in " ".join(img.parent.get("class", [])).lower() for keyword in ["menu", "food", "dish"]):
                is_likely_food = True
                
            # Skip if not likely a food image and we have some images already
            if not is_likely_food and len(downloaded_images) >= 5:
                continue
                
            # Download the image
            try:
                img_response = self.session.get(img_url, timeout=10)
                img_response.raise_for_status()
                
                # Determine image type from content
                content_type = img_response.headers.get("Content-Type", "")
                if "image" not in content_type:
                    continue
                    
                # Get file extension from URL or content type
                if "jpeg" in content_type or "jpg" in content_type:
                    ext = "jpg"
                elif "png" in content_type:
                    ext = "png"
                elif "gif" in content_type:
                    ext = "gif"
                elif "webp" in content_type:
                    ext = "webp"
                else:
                    # Try to get extension from URL
                    url_ext = os.path.splitext(urlparse(img_url).path)[1]
                    ext = url_ext[1:] if url_ext else "jpg"
                
                # Create a filename
                img_filename = f"food_{len(downloaded_images) + 1}.{ext}"
                img_path = os.path.join(self.output_folder, "images", img_filename)
                
                # Save the image
                with open(img_path, "wb") as f:
                    f.write(img_response.content)
                
                downloaded_images.append({
                    "url": img_url,
                    "local_path": img_path,
                    "alt_text": alt_text
                })
                
                print(f"Downloaded image: {img_filename}")
                
                # Add a small delay to be respectful to the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")
        
        return downloaded_images
    
    def save_food_items_to_file(self):
        """Save the scraped food items to a text file."""
        if not self.food_items:
            print("No food items to save.")
            return
            
        output_path = os.path.join(self.output_folder, "menu_items.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"Restaurant: {self.domain}\n")
            f.write("=" * 50 + "\n\n")
            
            for item in self.food_items:
                f.write(f"Name: {item.get('name', 'N/A')}\n")
                f.write(f"Price: {item.get('price', 'N/A')}\n")
                if item.get('description'):
                    f.write(f"Description: {item.get('description')}\n")
                f.write("\n" + "-" * 30 + "\n\n")
        
        print(f"Food items saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Scrape food images and menu items from a restaurant website")
    parser.add_argument("url", help="The URL of the restaurant website")
    parser.add_argument("--output", "-o", default="scraped_data", help="Output folder for scraped data")
    parser.add_argument("--images-only", action="store_true", help="Only scrape images, not menu items")
    parser.add_argument("--menu-only", action="store_true", help="Only scrape menu items, not images")
    
    args = parser.parse_args()
    
    scraper = RestaurantScraper(args.url, args.output)
    
    if not args.menu_only:
        print(f"Scraping food images from {args.url}...")
        scraper.scrape_food_images()
        
    if not args.images_only:
        print(f"Scraping menu items from {args.url}...")
        scraper.scrape_food_items()
        scraper.save_food_items_to_file()
    
    print("Scraping completed!")

if __name__ == "__main__":
    main()

""" Example Output:
Downloaded image: food_5.jpg
Scraping menu items from https://www.negrileats.com/menu/...
Found potential menu page: https://www.negrileats.com/menu/
Food items saved to scraped_data/menu_items.txt
Scraping completed!
"""

# Scrape menu items and images from entered websites
# Useful for scraping practice