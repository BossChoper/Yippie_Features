# Good map; can create a world map
import folium

def create_world_map():
    """
    Create an interactive world map with multiple markers and features.
    
    Returns:
        folium.Map: An interactive geographical map
    """
    # Create a world map centered on the coordinates of (0, 0)
    world_map = folium.Map(
        location=[0, 0],  # Centered at the equator and prime meridian
        zoom_start=2,     # Initial zoom level to show most of the world
        tiles='CartoDB positron'  # A clean, minimalist map style
    )
    
    # Add some interesting location markers
    locations = [
        {"name": "New York", "coords": [40.7128, -74.0060], "popup": "The Big Apple"},
        {"name": "Paris", "coords": [48.8566, 2.3522], "popup": "City of Lights"},
        {"name": "Tokyo", "coords": [35.6762, 139.6503], "popup": "Technology Hub"},
        {"name": "Sydney", "coords": [-33.8688, 151.2093], "popup": "Opera House"},
        {"name": "Cairo", "coords": [30.0444, 31.2357], "popup": "Pyramids of Giza"}
    ]
    
    # Add markers for each location
    for location in locations:
        folium.Marker(
            location=location["coords"],
            popup=location["popup"],
            tooltip=location["name"],
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(world_map)
    
    # Add some circle markers to show population or significance
    circle_locations = [
        {"name": "Moscow", "coords": [55.7558, 37.6173], "radius": 100000, "color": "red"},
        {"name": "Beijing", "coords": [39.9042, 116.4074], "radius": 150000, "color": "green"}
    ]
    
    for circle in circle_locations:
        folium.CircleMarker(
            location=circle["coords"],
            radius=circle["radius"] / 10000,  # Scaling down for visibility
            popup=circle["name"],
            color=circle["color"],
            fill=True,
            fillColor=circle["color"]
        ).add_to(world_map)
    
    return world_map

def save_map(map_object, filename='world_map.html'):
    """
    Save the map to an HTML file.
    
    Args:
        map_object (folium.Map): The map to save
        filename (str): Name of the file to save
    """
    map_object.save(filename)
    print(f"Map saved as {filename}")

def main():
    # Create the world map
    world_map = create_world_map()
    
    # Save the map
    save_map(world_map)
    
    print("Interactive map created successfully!")
    print("Open the HTML file in a web browser to explore the map.")

if __name__ == "__main__":
    main()