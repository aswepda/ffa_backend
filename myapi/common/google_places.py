
import googlemaps
import pprint
import time

def google_places(location):
    # Define API Key
    API_KEY = 'AIzaSyBDF9q6ilWVfRnGcxo_18--kfGVQOEu9_o'

    # Define our Client
    gmaps = googlemaps.Client(key = API_KEY)

    # Define our Search
    places_result = gmaps.places_nearby(location = location, radius = 1000, open_now = True, type = 'restaurant')

    # Define List
    places_list = []

    # loop through each place in the results
    for place in places_result['results']:

        # define my place id
        my_place_id = place['place_id']

        # define the fields we want sent back to us
        my_fields = ['name', 'formatted_phone_number', 'type', 'rating']

        # make a request for the details
        place_details = gmaps.place(place_id = my_place_id, fields = my_fields)

        # append place details to list
        places_list.append(place_details)

    return places_list