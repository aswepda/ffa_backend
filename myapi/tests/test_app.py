from myapi import app
import pytest, json

@pytest.fixture
def client():
    return app.app.test_client()

def test_hello_world(client):
    result = client.get('/')
    assert 'hello' in json.loads(result.data)
    assert json.loads(result.data)['hello'] == 'world'
    