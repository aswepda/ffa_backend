from flask_restful import Resource, request, abort
from flask import g
import common.google_places as places


class Places(Resource):
    def get(self):
        args = request.args
        search_string = ''
        location = ''
        search_nearby_type=''
        if 'lat' in args and 'lon' in args:
            lat = args['lat']
            lon = args['lon']
            location = lat + ',' + lon
        if 'type' in args:
            search_nearby_type = args['type']
            return places.get_google_places_nearby(location, search_nearby_type)
        elif 'search' in args:
            search_string = args['search']
            return places.get_google_places_find_place(location, search_string)
        else: 
            return abort(400, message="argument missing")