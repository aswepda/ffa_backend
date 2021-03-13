import configparser
import requests
import sys

# Current weather
def get_current_weather_by_city(location):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, API_KEY)
    r = requests.get(url)
    return r.json()

# Current weather
def get_current_weather_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude, longitude, API_KEY)
    r = requests.get(url)
    return r.json()

# Minutely forecast for 1 hour
def get_minutely_weather_forecast_next_hour_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(latitude, longitude, "alerts,current,hourly,daily", API_KEY)
    r = requests.get(url)
    return r.json()

# Hourly forecast for 48 hours
def get_hourly_weather_forecast_next_48hours_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(latitude, longitude, "alerts,current,minutely,daily", API_KEY)
    r = requests.get(url)
    return r.json()

# Daily forecast for 7 days
def get_daily_weather_forecast_next_7days_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}".format(latitude, longitude, "alerts,current,minutely,hourly", API_KEY)
    r = requests.get(url)
    return r.json()