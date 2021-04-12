import configparser
import requests
import sys
from flask_restful import abort

# Choose fitting function according to time parameter
def get_weather(latitude, longitude, time):
    if time == 'now':
        return get_current_weather_by_coordinates(latitude, longitude)
    elif time == 'later':
        return get_minutely_weather_forecast_next_hour_by_coordinates(latitude, longitude)
    elif time == 'today':
        return get_hourly_weather_forecast_next_48hours_by_coordinates(latitude, longitude)
    elif time == 'tomorrow':
        return get_daily_weather_forecast_next_7days_by_coordinates(latitude, longitude)
    else:
        return abort(400, message="Not a valid time parameter (use 'now', 'later', 'today' or 'tomorrow')")

# https://openweathermap.org/current
# Current weather
def get_current_weather_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&lang={}&appid={}".format(latitude, longitude, "de", API_KEY)
    r = requests.get(url)
    return r.json()

# https://openweathermap.org/api/one-call-api
# Minutely forecast for 1 hour 
def get_minutely_weather_forecast_next_hour_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&lang={}&appid={}".format(latitude, longitude, "alerts,current,hourly,daily", "de", API_KEY)
    r = requests.get(url)
    return r.json()

# Hourly forecast for 48 hours
def get_hourly_weather_forecast_next_48hours_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&lang={}&appid={}".format(latitude, longitude, "alerts,current,minutely,daily", "de", API_KEY)
    r = requests.get(url)
    return r.json()

# Daily forecast for 7 days
def get_daily_weather_forecast_next_7days_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&lang={}&appid={}".format(latitude, longitude, "alerts,current,minutely,hourly", "de", API_KEY)
    r = requests.get(url)
    return r.json()