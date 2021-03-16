from myapi import app
import pytest, json
from urllib.parse import urlencode

@pytest.fixture
def client():
    return app.app.test_client()

@pytest.fixture
def param():
    params = {
        "text": "Sample text to be spoken",
        "var": "Wrong query string"
    }
    return params

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'hello' in json.loads(response.data)
    assert json.loads(response.data)['hello'] == 'world'

  
def test_post_error(client):
    response = client.post('/')
    assert response.status_code == 405
    assert 'hello' not in json.loads(response.data)

