from geopy.geocoders import Nominatim

def get_lat_long(address):
    # Create a geolocator instance with a user agent
    geolocator = Nominatim(user_agent="address_to_latlong_converter")
    
    # Use the geocode method to retrieve location information
    location = geolocator.geocode(address)
    
    if location:
        return location.latitude, location.longitude
    else:
        return None

# Example usage
address = input("Enter an address: ")
coordinates = get_lat_long(address)

if coordinates:
    print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
else:
    print("Could not find coordinates for the given address.")
