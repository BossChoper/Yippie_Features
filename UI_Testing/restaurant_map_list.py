# Functional; creates a UI for generation of restaurants, filter, etc.
import tkinter as tk
from tkinter import ttk
import math
import random

class RestaurantProximityApp:
    def __init__(self, master):
        self.master = master
        master.title("Restaurant Proximity Finder")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        # Central point coordinates (example: New York City center)
        self.central_lat = 40.7128
        self.central_lon = -74.0060

        # Styles
        self.style = ttk.Style()
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12))

        # Create and setup UI components
        self.create_ui()

        # Generate initial restaurant list
        self.restaurants = self.generate_restaurants()
        self.update_restaurant_list()

    def create_ui(self):
        """Create the user interface components"""
        # Frame for central point info
        central_frame = ttk.Frame(self.master, style='TFrame')
        central_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(central_frame, text="Central Point: New York City", style='TLabel').pack(side='left')

        # Search and filter frame
        search_frame = ttk.Frame(self.master)
        search_frame.pack(pady=10, padx=10, fill='x')

        # Cuisine type filter
        ttk.Label(search_frame, text="Filter by Cuisine:", style='TLabel').pack(side='left', padx=(0,10))
        self.cuisine_var = tk.StringVar()
        cuisine_options = ['All', 'Pizza', 'Sushi', 'Burger', 'Cafe', 'Steakhouse', 'Vegetarian', 'Seafood']
        cuisine_dropdown = ttk.Combobox(search_frame, textvariable=self.cuisine_var, values=cuisine_options, width=15)
        cuisine_dropdown.pack(side='left', padx=(0,10))
        cuisine_dropdown.set('All')
        cuisine_dropdown.bind('<<ComboboxSelected>>', self.filter_restaurants)

        # Max distance filter
        ttk.Label(search_frame, text="Max Distance (miles):", style='TLabel').pack(side='left', padx=(10,10))
        self.distance_var = tk.StringVar(value='10')
        distance_entry = ttk.Entry(search_frame, textvariable=self.distance_var, width=10)
        distance_entry.pack(side='left', padx=(0,10))

        # Filter button
        filter_button = ttk.Button(search_frame, text="Apply Filter", command=self.filter_restaurants)
        filter_button.pack(side='left')

        # Restaurants Treeview
        self.tree = ttk.Treeview(self.master, columns=('Name', 'Cuisine', 'Distance', 'Latitude', 'Longitude'), show='headings')
        self.tree.pack(pady=10, padx=10, expand=True, fill='both')

        # Define column headings
        self.tree.heading('Name', text='Restaurant Name')
        self.tree.heading('Cuisine', text='Cuisine Type')
        self.tree.heading('Distance', text='Distance (miles)')
        self.tree.heading('Latitude', text='Latitude')
        self.tree.heading('Longitude', text='Longitude')

        # Set column widths
        self.tree.column('Name', width=200)
        self.tree.column('Cuisine', width=100)
        self.tree.column('Distance', width=100)
        self.tree.column('Latitude', width=100)
        self.tree.column('Longitude', width=100)

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 3956  # Radius of earth in miles
        return c * r

    def generate_restaurants(self, num_restaurants=50):
        """Generate a list of random restaurants near the central point"""
        cuisines = ['Pizza', 'Sushi', 'Burger', 'Cafe', 'Steakhouse', 'Vegetarian', 'Seafood']
        restaurants = []

        for i in range(num_restaurants):
            # Generate coordinates within ~10 miles of central point
            lat_variation = random.uniform(-0.1, 0.1)
            lon_variation = random.uniform(-0.1, 0.1)
            
            restaurant_lat = self.central_lat + lat_variation
            restaurant_lon = self.central_lon + lon_variation

            restaurant = {
                'name': f"{random.choice(cuisines)} Restaurant {i+1}",
                'cuisine': random.choice(cuisines),
                'latitude': restaurant_lat,
                'longitude': restaurant_lon,
                'distance': self.haversine_distance(
                    self.central_lat, self.central_lon, 
                    restaurant_lat, restaurant_lon
                )
            }
            restaurants.append(restaurant)

        return sorted(restaurants, key=lambda x: x['distance'])

    def update_restaurant_list(self, filtered_restaurants=None):
        """Update the treeview with restaurant data"""
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Use filtered list or full list
        restaurants_to_show = filtered_restaurants or self.restaurants

        # Populate treeview
        for restaurant in restaurants_to_show:
            self.tree.insert('', 'end', values=(
                restaurant['name'], 
                restaurant['cuisine'], 
                f"{restaurant['distance']:.2f}", 
                f"{restaurant['latitude']:.4f}", 
                f"{restaurant['longitude']:.4f}"
            ))

    def filter_restaurants(self, event=None):
        """Filter restaurants based on cuisine and max distance"""
        # Get filter values
        selected_cuisine = self.cuisine_var.get()
        max_distance = float(self.distance_var.get())

        # Filter restaurants
        filtered = [
            r for r in self.restaurants 
            if (selected_cuisine == 'All' or r['cuisine'] == selected_cuisine) 
            and r['distance'] <= max_distance
        ]

        # Update list
        self.update_restaurant_list(filtered)

def main():
    root = tk.Tk()
    app = RestaurantProximityApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

