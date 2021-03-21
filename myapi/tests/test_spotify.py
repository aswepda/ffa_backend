import pytest
import json
import common.spotify_utility
from myapi import app


@pytest.fixture
def client():
    return app.app.test_client()


@pytest.fixture
def token():
    token = {
        # Insert your Spotify TOKEN Here:
        "Authorization": ""
    }
    return token


def test_getAlbumFromArtist(client, token):
    response = client.get(
        '/spotify/getAlbumFromArtist?album=wish you were here&artist=pink floyd', headers=token)
    assert response.status_code == 200
    assert 'spotify:album:' in str(json.loads(response.data))
    assert 'Pink Floyd' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_playGenre(client, token):
    response = client.get('/spotify/playGenre?genre=rock', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert 'rock' in str(json.loads(response.data))


def test_playMusicFromYear(client, token):
    response = client.get('/spotify/playYear?year=2012', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert '2012' in str(json.loads(response.data))


def test_getFavoriteArtists(client, token):
    response = client.get('/spotify/getFavoriteArtists', headers=token)
    assert response.status_code == 200
    assert 'spotify:artist:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getFavoriteGenres(client, token):
    response = client.get('/spotify/getFavoriteGenres', headers=token)
    assert response.status_code == 200
    assert type(json.loads(response.data)) == dict


def test_getFavoriteTracks(client, token):
    response = client.get('/spotify/getFavoriteTracks', headers=token)
    assert response.status_code == 200
    assert 'spotify:track:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getPlaylists(client, token):
    response = client.get('/spotify/getPlaylists?name=workout', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert 'workout' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getUserPlaylists(client, token):
    response = client.get('/spotify/getUserPlaylists', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getArtist(client, token):
    response = client.get('/spotify/getArtist?name=Queen', headers=token)
    assert response.status_code == 200
    assert 'spotify:artist:' in str(json.loads(response.data))
    assert 'Queen' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict
