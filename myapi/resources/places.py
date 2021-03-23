from flask_restful import Resource, request
from flask import g
import common.google_places as places


class Places(Resource):
    def get(self):
        args = request.args
        search_string = ''
        location = ''
        search_nearby_type=''
        if 'lat' in args and 'lon' in args and 'type' in args:
            lat = args['lat']
            lon = args['lon']
            location = lat + ',' + lon
            search_nearby_type = args['type']
        elif 'search' in args:
            search_string = args['search']
        else: 
            return "argument missing"
        var = places.google_places(location, search_string, search_nearby_type)
        return var