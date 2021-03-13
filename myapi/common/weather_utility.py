import configparser
import requests
import sys

def get_weather_by_city(location):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, API_KEY)
    r = requests.get(url)
    return r.json()

def get_weather_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude, longitude, API_KEY)
    r = requests.get(url)
    return r.json()

def get_weather_forecast_by_city(location):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, API_KEY)
    r = requests.get(url)
    return r.json()

def get_weather_forecast_by_coordinates(latitude, longitude):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(latitude, longitude, API_KEY)
    r = requests.get(url)
    return r.json()