from datetime import datetime

# Mock trip plan data
MOCK_TRIP_PLAN = {
    "destination": "San Francisco, CA",
    "duration": "Weekend (March 8-9, 2025)",
    "days": [
        {
            "date": "2025-03-08",
            "restaurants": [
                {
                    "name": "Burger Bonanza",
                    "cuisine": "American",
                    "food": "Classic Burger",
                    "address": "123 Food St",
                    "time": "12:00 PM"
                },
                {
                    "name": "Taco Haven",
                    "cuisine": "Mexican",
                    "food": "Street Tacos",
                    "address": "789 Taco Ln",
                    "time": "6:00 PM"
                }
            ]
        },
        {
            "date": "2025-03-09",
            "restaurants": [
                {
                    "name": "Sushi Spot",
                    "cuisine": "Japanese",
                    "food": "Sushi Rolls",
                    "address": "321 Fish Rd",
                    "time": "1:00 PM"
                },
                {
                    "name": "Pizza Palace",
                    "cuisine": "Italian",
                    "food": "Margherita Pizza",
                    "address": "456 Slice Ave",
                    "time": "7:00 PM"
                }
            ]
        }
    ]
}

def print_trip_plan(plan: dict):
    """Print the trip plan kit to the console."""
    print("\nTrip Plan Kit:")
    print(f"  Destination: {plan['destination']}")
    print(f"  Duration: {plan['duration']}")
    for day in plan["days"]:
        print(f"\n  Date: {day['date']}")
        print("    Restaurants:")
        for restaurant in day["restaurants"]:
            print(f"      - {restaurant['name']} ({restaurant['cuisine']})")
            print(f"        Food: {restaurant['food']}")
            print(f"        Address: {restaurant['address']}")
            print(f"        Time: {restaurant['time']}")

def save_trip_plan(plan: dict, filename: str = "trip_plan.txt"):
    """Save the trip plan kit to a text file."""
    try:
        with open(filename, "w") as file:
            file.write("Trip Plan Kit\n")
            file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Destination: {plan['destination']}\n")
            file.write(f"Duration: {plan['duration']}\n")
            for day in plan["days"]:
                file.write(f"\nDate: {day['date']}\n")
                file.write("  Restaurants:\n")
                for restaurant in day["restaurants"]:
                    file.write(f"    - {restaurant['name']} ({restaurant['cuisine']})\n")
                    file.write(f"      Food: {restaurant['food']}\n")
                    file.write(f"      Address: {restaurant['address']}\n")
                    file.write(f"      Time: {restaurant['time']}\n")
        print(f"Trip plan saved to {filename}")
    except Exception as e:
        print(f"Error saving trip plan: {e}")

def main():
    """Run the Trip Plan Program."""
    print("Starting Trip Plan Program...")
    
    # Use mock data
    trip_plan = MOCK_TRIP_PLAN
    
    # Print and save the plan
    print_trip_plan(trip_plan)
    save_trip_plan(trip_plan)

if __name__ == "__main__":
    main()

"""
\\ Example output:
Starting Trip Plan Program...

Trip Plan Kit:
  Destination: San Francisco, CA
  Duration: Weekend (March 8-9, 2025)

  Date: 2025-03-08
    Restaurants:
      - Burger Bonanza (American)
        Food: Classic Burger
        Address: 123 Food St
        Time: 12:00 PM
      - Taco Haven (Mexican)
        Food: Street Tacos
        Address: 789 Taco Ln
        Time: 6:00 PM

  Date: 2025-03-09
    Restaurants:
      - Sushi Spot (Japanese)
        Food: Sushi Rolls
        Address: 321 Fish Rd
        Time: 1:00 PM
      - Pizza Palace (Italian)
        Food: Margherita Pizza
        Address: 456 Slice Ave
        Time: 7:00 PM
Trip plan saved to trip_plan.txt
\\
"""

# Trip planning
# Find restaurants, retrieve basic information including open time and location

