from flask_restful import Resource
from flask import g
import common.weather_utility

class Weather(Resource):
    def get(self):
        var = common.weather_utility.get_weather('Stuttgart')
        return var