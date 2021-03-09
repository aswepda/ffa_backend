import configparser
import requests
import sys



def get_weather(location):
    API_KEY = 'bdde23a2384b8b49a5c47d36cbab8780'
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(location, API_KEY)
    r = requests.get(url)
    return r.json()
