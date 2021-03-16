from flask_restful import Resource
from flask import g
import common.weather_utility

class Weather(Resource):
    def get(self):
        var = common.weather_utility.get_current_weather_by_city('Stuttgart')
        return var