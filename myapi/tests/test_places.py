import pytest, json
import common.google_places
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()

def test_get_google_places_nearby(client):
    response = client.get('/places?lat=48.7823&lon=9.177&type=book_store')
    assert response.status_code == 200

def test_get_google_places_find_place(client):
    response = client.get('/places?search=dhbw%20stuttgart')
    assert response.status_code == 200