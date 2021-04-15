from flask_restful import Resource, request, abort
from flask import g
import common.weather_utility

class Weather(Resource):
    def get(self, time):
        args = request.args
        if 'lat' in args and 'lon' in args:
            lat = args['lat']
            lon = args['lon']
        else: 
            return abort(400, message="Latitude and/or longitude missing")
        var = common.weather_utility.get_weather(lat, lon, time)
        return var