from flask_restful import Resource
from flask import g
import common.weather_utility

class Weather(Resource):
    def get(self):
        var = common.weather_utility.get_daily_weather_forecast_next_7days_by_coordinates('48.7667','9.1833')
        return var