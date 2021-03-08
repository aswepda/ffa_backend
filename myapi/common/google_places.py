
import googlemaps
import pprint
import time

def google_places(location)
    # Define API Key and URL
    API_KEY = 'AIzaSyDJTwbKNbu91ez-Bb20qNSfta6Z8MSD4-M'

    # Define our Client
    gmaps = googlemaps.Client(key = API_KEY)

    # Define our Search
    places_result = gmaps.places_nearby(location= '-33.8670522,151.1957362', radius  = 40000, open_now = False, type = 'cafe')

    return places_result