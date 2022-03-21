import googlemaps
from datetime import datetime
import os

def get_direction(origin, mode, destination):
    api_key = os.getenv("GOOGLE_API_KEY")
    way = mode
    start = origin
    end = destination
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    # Request directions via public transit
    directions_result = gmaps.directions(origin=start, destination=end, mode=way, departure_time=now)
    data = {"message": 'Dauer',
        "data": directions_result[0]['legs'][0]['duration'],
        "speakMessage": True}
    return data