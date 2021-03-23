
import googlemaps
import pprint
import time

def get_google_places_nearby(location, search_nearby_type):
    # Define API Key
    API_KEY = 'AIzaSyBDF9q6ilWVfRnGcxo_18--kfGVQOEu9_o'

    # Define our Client
    gmaps = googlemaps.Client(key = API_KEY)

    # Define our Search
    places_result = gmaps.places_nearby(location = location, radius = 5000, open_now = True, type = search_nearby_type)

    # Define List
    places_list = []

    # loop through each place in the results
    for place in places_result['results']:

        # define my place id
        my_place_id = place['place_id']

        # define the fields we want sent back to us
        my_fields = ['name', 'formatted_phone_number', 'type', 'rating', 'price_level', 'geometry', 'formatted_address', 'user_ratings_total']

        # make a request for the details
        place_details = gmaps.place(place_id = my_place_id, fields = my_fields)

        # append place details to list
        places_list.append(place_details)

    return places_list

def get_google_places_find_place(location, search_string):
    # Define API Key
    API_KEY = 'AIzaSyBDF9q6ilWVfRnGcxo_18--kfGVQOEu9_o'

    # Define our Client
    gmaps = googlemaps.Client(key = API_KEY)

    # Define our Search
    places_result = gmaps.places(location = location, radius = 5000, open_now = True, query=search_string)
    
    # Define List
    places_list = []

    # loop through each place in the results
    for place in places_result['results']:

        # define my place id
        my_place_id = place['place_id']

        # define the fields we want sent back to us
        my_fields = ['name', 'formatted_phone_number', 'type', 'rating', 'price_level', 'geometry', 'formatted_address', 'user_ratings_total']

        # make a request for the details
        place_details = gmaps.place(place_id = my_place_id, fields = my_fields)

        # append place details to list
        places_list.append(place_details)

    return places_list