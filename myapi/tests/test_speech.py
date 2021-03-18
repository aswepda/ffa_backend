import common.speech_utility 
from myapi import app
import base64
import pytest
from urllib.parse import urlencode

@pytest.fixture
def client():
    return app.app.test_client()

@pytest.mark.skip()
def test_connection():
    var = str(base64.b64encode(common.speech_utility.text_to_speech("test")), 'ascii', 'ignore')
    assert var.startswith("SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//")

@pytest.mark.skip()
def test_right_query_string(client):
    qstr = urlencode([("text", "Sample text to be spoken")])
    response = client.get('/speech?' + qstr)
    assert response.status_code == 200

@pytest.mark.skip()
def test_wrong_query_string(client):
    qstr = urlencode([("var", "Other value")])
    response = client.get('/speech?' + qstr)     
    assert response.status_code == 400

