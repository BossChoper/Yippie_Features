# Functional Javascript console script; gets images on webpage (RestaurantJi)
from bs4 import BeautifulSoup
import requests

url = "https://www.restaurantji.com/ny/new-york/mcdonalds-57/menu/"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all gallery links first
    gallery_links = soup.find_all('a', class_='gallery_item')
    
    # Extract image URLs from matching img tags
    for link in gallery_links:
        img_tag = link.find('img')
        if img_tag and img_tag.get('src'):
            print(img_tag['src'])
else:
    print(f"Request failed with status {response.status_code}")

""" SCRIPT DOESN'T WORK. Was able to get images from webpage through javascript console. 
Restaurant: McDonald's

Example output:
[ "https://cdn5.localdatacdn.com/ny/new-york/1593808/original/YbB397mkp4.jpg", "https://cdn5.localdatacdn.com/ny/new-york/1593808/original/VmXvEEMXII.jpg", "https://cdn3.localdatacdn.com/ny/new-york/1593808/original/3E9VdyMS6N.jpg", "https://cdn3.localdatacdn.com/ny/new-york/1593808/original/uoeJXMxbGi.jpg", "https://cdn3.localdatacdn.com/ny/new-york/1593808/original/FCfdU46LYd.jpg", "https://cdn.localdatacdn.com/ny/new-york/1593808/original/uKksoFed6n.jpg", "https://cdn9.localdatacdn.com/ny/new-york/1593808/original/gVtMdauSf3.jpg", "https://cdn9.localdatacdn.com/ny/new-york/1593808/original/14C3bSyQbQ.jpg", "https://cdn9.localdatacdn.com/ny/new-york/1593808/original/CxqhHGIDs8.jpg" ]

Script:
// Get all gallery items
const galleryItems = document.querySelectorAll('a.gallery_item');

// Extract image URLs
const imageUrls = Array.from(galleryItems).map(item => {
    const img = item.querySelector('img');
    return img ? img.src : null;
}).filter(url => url);

console.log(imageUrls);
"""

""" Example result:
[
    "https://cdn5.localdatacdn.com/ny/new-york/3827136/original/BioZExbYDO.jpg",
    "https://cdn5.localdatacdn.com/ny/new-york/3827136/original/y7CrW06vnJ.jpg",
    "https://cdn3.localdatacdn.com/ny/new-york/3827136/original/df5roKGhUf.jpg",
    "https://cdn3.localdatacdn.com/ny/new-york/3827136/original/cfEdvGKMLX.jpg"
]

As JSON literal:
"https://cdn5.localdatacdn.com/ny/new-york/3827136/original/BioZExbYDO.jpg"
"""