from datetime import datetime

# Mock location history data with past occupants
MOCK_HISTORY = [
    {
        "event": "Opening",
        "name": "Burger Bonanza",
        "location": "123 Food St, San Francisco, CA",
        "date": "2023-05-15",
        "details": "New gourmet burger joint opened with vegan options.",
        "past_occupants": [
            {"name": "Pizza Palooza", "period": "2018-2022", "details": "Closed after owner retired."},
            {"name": "Taco Terrace", "period": "2015-2017", "details": "Relocated to downtown."}
        ]
    },
    {
        "event": "Closing",
        "name": "Pizza Palace",
        "location": "456 Slice Ave, San Francisco, CA",
        "date": "2024-01-10",
        "details": "Closed due to lease expiration.",
        "past_occupants": [
            {"name": "Burger Barn", "period": "2010-2023", "details": "Known for cheap eats."}
        ]
    },
    {
        "event": "Opening",
        "name": "Taco Haven",
        "location": "789 Taco Ln, San Francisco, CA",
        "date": "2024-06-20",
        "details": "Street-style tacos now available.",
        "past_occupants": []
    },
    {
        "event": "Closing",
        "name": "Sushi Spot",
        "location": "321 Fish Rd, San Francisco, CA",
        "date": "2025-02-28",
        "details": "Shut down after health inspection issues.",
        "past_occupants": [
            {"name": "Fish Fry Hut", "period": "2019-2024", "details": "Popular seafood shack."}
        ]
    }
]

def print_history(history: list):
    """Print the location history to the console."""
    print("\nLocation History:")
    for entry in history:
        print(f"  Event: {entry['event']}")
        print(f"    Name: {entry['name']}")
        print(f"    Location: {entry['location']}")
        print(f"    Date: {entry['date']}")
        print(f"    Details: {entry['details']}")
        if entry["past_occupants"]:
            print("    Past Occupants:")
            for past in entry["past_occupants"]:
                print(f"      - {past['name']} ({past['period']})")
                print(f"        {past['details']}")
        print()

def save_history(history: list, filename: str = "location_history.txt"):
    """Save the location history to a text file."""
    try:
        with open(filename, "w") as file:
            file.write("Location History\n")
            file.write(f"Saved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for entry in history:
                file.write(f"Event: {entry['event']}\n")
                file.write(f"  Name: {entry['name']}\n")
                file.write(f"  Location: {entry['location']}\n")
                file.write(f"  Date: {entry['date']}\n")
                file.write(f"  Details: {entry['details']}\n")
                if entry["past_occupants"]:
                    file.write("  Past Occupants:\n")
                    for past in entry["past_occupants"]:
                        file.write(f"    - {past['name']} ({past['period']})\n")
                        file.write(f"      {past['details']}\n")
                file.write("\n")
        print(f"History saved to {filename}")
    except Exception as e:
        print(f"Error saving history: {e}")

def main():
    """Run the Location History Program."""
    print("Starting Location History Program...")
    
    # Use mock data
    history = MOCK_HISTORY
    
    # Print and save the history
    print_history(history)
    save_history(history)

if __name__ == "__main__":
    main()

""" Example output:
Starting Menu Pictures Program...

Menu Item: Factory Burger
  Picture 1: https://www.thecheesecakefactory.com/assets/images/Menu-Items/factory-burger.jpg
  Picture 2: No additional image found
  Picture 3: No additional image found

Menu Item: Chicken Parmesan "Pizza Style"
  Picture 1: https://www.thecheesecakefactory.com/assets/images/Menu-Items/chicken-parmesan-pizza-style.jpg
  Picture 2: No additional image found
  Picture 3: No additional image found
"""

# Useful for storing restaurant details
# Stores past restaurants, reason they closed, if/where they moved
