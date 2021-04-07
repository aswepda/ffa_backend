import pytest, json
import common.directions_utility
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()

def test_get_direction(client):
    response = client.get('/directions/schorndorf/driving/Stuttgart')
    assert response.status_code == 200
    assert 'data' in json.loads(response.data)
