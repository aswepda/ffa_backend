import pytest, json
import common.directions_utility
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()


@pytest.fixture
def token():
    token = {
        "Authorization": "eyJ0b2tlbiI6ICJ5YTI5LmEwQWZINlNNQ1hjS0JWejFENTlhck53ZXZlUXR6X090RExwN052OXJkaGdEVDBPWmJBcTROTnR2ZjVZWm03M2h1RVlHTDRrTi1lRUlJSDlDQzl1TkJBOVAxSVNTSFNKUG5FSUQ1YllDVUZsOXdFY2JfZVc4bjByQWZxd2R3SFhMcEtMZVRVcTZQZlU3Si00aGc4Rzc1V3l2c2hVVWFKIiwgInJlZnJlc2hfdG9rZW4iOiAiMS8vMDM4T1lWOS1xUzhSRkNnWUlBUkFBR0FNU053Ri1MOUlyWjhFMzYtNVg2ODJKRHZaSmZsMlUyempYSjdWUkpITUo3QW1WMlNxeXpnQktZM2JYY2tya1gzQzlOUnc2NDdDM0drbyIsICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLCAiY2xpZW50X2lkIjogIjU5OTQxOTQ3ODgxLWJrZW1pYmk3Y2Nwc2VhNTk0NTYxdjBpNW43ZWlsczloLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwgImNsaWVudF9zZWNyZXQiOiAiN2dtaWFlZnpDNTQ4NmpUOUtlRnZVZzhXIiwgInNjb3BlcyI6IFsib3BlbmlkIiwgImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvdXNlcmluZm8ucHJvZmlsZSIsICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9hdXRoL3VzZXJpbmZvLmVtYWlsIiwgImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL2F1dGgvY2FsZW5kYXIuZXZlbnRzLnJlYWRvbmx5Il0sICJleHBpcnkiOiAiMjAyMS0wNC0xMlQxNDo1MDowMy45NjQ5ODRaIn0="
    }
    return token

def test_lunch(client):
    response = client.get('/lunchbreak')
    assert response.status_code == 200
    assert 'No' in json.loads(response.data)

def test_calendar(client, token):
    response = client.get('/calendar/today', headers = token)
    assert response.status_code == 200
    assert 'data' in json.loads(response.data)

def test_calendar(client, token):
    response = client.get('/calendar/lunch', headers = token)
    assert response.status_code == 200
    assert 'data' in json.loads(response.data)