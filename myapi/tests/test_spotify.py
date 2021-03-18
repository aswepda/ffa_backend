import pytest, json
import common.spotify_utility
from myapi import app

@pytest.fixture
def client():
    return app.app.test_client()

def test_playGenre(client):
    response = client.get('/spotify/playGenre?genre=rock')
    assert response.status_code == 200
    assert 'spotify:playlist:' in json.loads(response.data.uri)
    assert 'rock' in json.loads(response.data.name)


def test_playMusicFromYear(client):
    response = client.get('/spotify/playYear?year=2012')
    assert response.status_code == 200
    assert 'spotify:playlist:' in json.loads(response.data.uri)
    assert '2012' in json.loads(response.data.name)
    

def test_getFavoriteArtists(client):
    response = client.get('/spotify/getFavoriteArtists')
    assert response.status_code == 200
    assert 'spotify:artist:' in json.loads(response.data)
    assert type(json.loads(response.data)) == list
    

def test_getFavoriteGenres(client):
    response = client.get('/spotify/getFavoriteGenres')
    assert response.status_code == 200
    assert type(json.loads(response.data)) == list
    

def test_getFavoriteTracks(client):
    response = client.get('/spotify/getFavoriteTracks')
    assert response.status_code == 200
    assert 'spotify:track:' in json.loads(response.data)
    assert type(json.loads(response.data)) == list
    
def test_getPlaylists(client):
    response = client.get('/spotify/getPlaylists?name=workout')
    assert response.status_code == 200
    assert 'spotify:playlist:' in json.loads(response.data)
    assert type(json.loads(response.data)) == list
    

def test_getUserPlaylists(client):
    response = client.get('/spotify/getUserPlaylists')
    assert response.status_code == 200
    assert 'spotify:playlist:' in json.loads(response.data)
    assert type(json.loads(response.data)) == list
    

def test_getArtist(client):
    response = client.get('/spotify/getArtist?name=Queen')
    assert response.status_code == 200
    assert 'spotify:artist:' in json.loads(response.data)
    assert json.loads(response.data.name) == 'Queen'
    assert type(json.loads(response.data)) == list
    

def test_getAlbumFromArtist(client):
    response = client.get('/spotify/getAlbumFromArtist?album=wish you were here&artist=pink floyd')
    assert response.status_code == 200
    assert 'spotify:album:' in json.loads(response.data)
    assert 'Pink Floyd' in json.loads(response.data[0].artist)
    assert type(json.loads(response.data)) == list
