import math


def circle_coordinates(latitude, longitude, radius):
    """
    Circle around a point with a given latitude, longitude, and radius.
    Returns a generator that continuously produces coordinates.
    """
    # Convert latitude and longitude to radians
    lat_r = math.radians(latitude)
    long_r = math.radians(longitude)
    # Generate coordinates
    theta = 0
    while True:
        # Calculate new latitude and longitude
        lat_new = math.asin(math.sin(lat_r) * math.cos(radius / 6371) + math.cos(lat_r) * math.sin(radius / 6371) * math.cos(theta))
        long_new = long_r + math.atan2(math.sin(theta) * math.sin(radius / 6371) * math.cos(lat_r), math.cos(radius / 6371) - math.sin(lat_r) * math.sin(lat_new))
        # Convert back to degrees
        lat_new = math.degrees(lat_new)
        long_new = math.degrees(long_new)
        # Yield the new coordinates
        yield (lat_new, long_new)
        # Increase the angle
        theta += 0.1


if __name__ == "__main__":

    coords = circle_coordinates(37.7749, -122.4194, 1) # Circle 1 km around San Francisco
    for i in range(10):
        print(next(coords))