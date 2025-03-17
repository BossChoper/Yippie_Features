import asyncio
import random
import signal
import sys
from dataclasses import dataclass
from typing import Optional

try:
    from plyer import notification
except ImportError:
    print("Error: plyer package not found. Please install it using: pip install plyer")
    sys.exit(1)

@dataclass
class Restaurant:
    name: str
    description: str
    distance: float  # Distance in miles
    rating: Optional[float] = None
    price_level: Optional[str] = None

MOCK_RESTAURANTS = [
    Restaurant("Donut Run DC", "High quality vegan donuts", 0.91, 4.8, "$$"),
    Restaurant("Pizza Palace", "Freshly baked artisan pizza", 1.3, 4.5, "$$"),
    Restaurant("Taco Haven", "Spicy street-style tacos", 0.75, 4.7, "$"),
    Restaurant("Burger Bonanza", "Juicy gourmet burgers", 1.8, 4.2, "$$"),
    Restaurant("Sushi Spot", "Fresh sushi rolls", 2.5, 4.6, "$$$"),  # Outside threshold
]

# Static user location (could be expanded with real coords later)
USER_LOCATION = {"lat": 38.8977, "lon": -77.0365}  # Example: Washington, DC
DISTANCE_THRESHOLD_MIN = 1.0  # Minimum distance in miles
DISTANCE_THRESHOLD_MAX = 2.0  # Maximum distance in miles

def signal_handler(sig, frame):
    """Handle graceful shutdown on Ctrl+C"""
    print("\nShutting down notification system...")
    sys.exit(0)

async def send_notification(restaurant: Restaurant) -> bool:
    """Send a desktop notification about a restaurant.
    
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    try:
        message = (
            f"{restaurant.name}: {restaurant.description}\n"
            f"Distance: {restaurant.distance:.1f} mi | Rating: {restaurant.rating}★ | Price: {restaurant.price_level}"
        )
        
        notification.notify(
            title="Food Finder Alert",
            message=message,
            app_name="Food Finder",
            timeout=10  # Notification lasts 10 seconds
        )
        return True
    except Exception as e:
        print(f"Failed to send notification: {e}")
        return False

async def check_nearby_restaurants():
    """Simulate checking for nearby restaurants and send notifications."""
    notifications_sent = 0
    
    while True:
        # Randomly select a restaurant to simulate real-time alerts
        restaurant = random.choice(MOCK_RESTAURANTS)
        
        # Check if within threshold
        if DISTANCE_THRESHOLD_MIN <= restaurant.distance <= DISTANCE_THRESHOLD_MAX:
            print(f"\nFound restaurant within range: {restaurant.name}")
            if await send_notification(restaurant):
                notifications_sent += 1
                print(f"Successfully sent notification #{notifications_sent}")
        
        # Wait randomly between 15-30 seconds between notifications
        await asyncio.sleep(random.uniform(15, 30))

async def main():
    """Run the notification system."""
    print("Starting Food Finder Notifications System...")
    print(f"Monitoring restaurants within {DISTANCE_THRESHOLD_MIN}-{DISTANCE_THRESHOLD_MAX} miles")
    print("Press Ctrl+C to stop the notifications")
    
    try:
        await check_nearby_restaurants()
    except asyncio.CancelledError:
        print("\nNotification system stopped")

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run the asyncio event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully

# Notification system for location
# Useful for location-based alert practice and testing