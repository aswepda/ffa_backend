import pytest, json
import common.weather_utility
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()

def test_get_current_weather_by_city(client):
    var = common.weather_utility.get_current_weather_by_city('Stuttgart')
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200

# TBD
def test_get_current_weather_by_coordinates(client):
    var = common.weather_utility.get_current_weather_by_coordinates('48.7667', '9.1833')
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200

# TBD
def test_get_minutely_weather_forecast_next_hour_by_coordinates(client):
    var = common.weather_utility.get_current_weather_by_city('Stuttgart')
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200

# TBD
def test_get_hourly_weather_forecast_next_48hours_by_coordinates(client):
    var = common.weather_utility.get_current_weather_by_city('Stuttgart')
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200


# TBD
def test_get_daily_weather_forecast_next_7days_by_coordinates(client):
    var = common.weather_utility.get_current_weather_by_city('Stuttgart')
    response = client.get('/weather')
    assert response.status_code == 200
    assert 'cod' in json.loads(response.data)
    assert json.loads(response.data)['cod'] == 200


