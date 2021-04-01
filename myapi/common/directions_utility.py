import googlemaps
from datetime import datetime

def get_direction(origin, mode, destination):
    api_key='AIzaSyBDF9q6ilWVfRnGcxo_18--kfGVQOEu9_o'
    way = mode
    start = origin
    end = destination
    gmaps = googlemaps.Client(key=api_key)
    now = datetime.now()
    # Request directions via public transit
    directions_result = gmaps.directions(origin=start, destination=end, mode=way, departure_time=now)
    data = {"message": 'Dauer',
        "data": directions_result[0]['legs'][0]['duration']['text'],
        "speakMessage": True}
    return data