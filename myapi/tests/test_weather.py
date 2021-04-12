import pytest, json
import common.weather_utility
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()

def test_get_current_weather_by_coordinates(client):
    response = client.get('/weather/now?lat=48.7823&lon=9.177')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200

def test_get_minutely_weather_forecast_next_hour_by_coordinates(client):
    response = client.get('/weather/later?lat=48.7823&lon=9.177')
    assert response.status_code == 200
    assert 'minutely' in json.loads(response.data)

def test_get_hourly_weather_forecast_next_48hours_by_coordinates(client):
    response = client.get('/weather/today?lat=48.7823&lon=9.177')
    assert response.status_code == 200
    assert 'hourly' in json.loads(response.data)

def test_get_daily_weather_forecast_next_7days_by_coordinates(client):
    response = client.get('/weather/tomorrow?lat=48.7823&lon=9.177')
    assert response.status_code == 200
    assert 'daily' in json.loads(response.data)

def test_get_weather(client):
    response = client.get('/weather/noow?lat=48.7823&lon=9.177')
    assert response.status_code == 200
    assert b"Not a valid time parameter (use 'now', 'later', 'today' or 'tomorrow')" in response.data

def test_get_current_weather_by_coordinates_missing_arguments(client):
    response = client.get('/weather/now?lat=48.7823')
    assert response.status_code == 200
    assert b"Latitude and/or longitude missing" in response.data
