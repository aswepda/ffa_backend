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
        "Authorization": "AQDQgsBAiszxDDX-UZ4ltaTIAhwUwrWsChU_iD-AUBm7qCtmm3T9_fHzzXFtC3ywDOPH0ZSE1NE3YvAbZChEp5Rpjzb_MdgVdKnCSCz5DnD7Svm9SoXuNFkUxfvAvI4ewp4"
    }
    return token


def test_getAlbumFromArtist(client, token):
    response = client.get('/spotify/artist/pink floyd/wish you were here', headers=token)
    assert response.status_code == 200
    assert 'spotify:album:' in str(json.loads(response.data))
    assert 'Pink Floyd' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_playGenre(client, token):
    response = client.get('/spotify/genre/rock', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert 'rock' in str(json.loads(response.data))


def test_playMusicFromYear(client, token):
    response = client.get('/spotify/year/2012', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert '2012' in str(json.loads(response.data))


def test_getFavoriteArtists(client, token):
    response = client.get('/spotify/user/favorite/artists', headers=token)
    assert response.status_code == 200
    assert 'spotify:artist:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getFavoriteGenres(client, token):
    response = client.get('/spotify/user/favorite/genres', headers=token)
    assert response.status_code == 200
    assert type(json.loads(response.data)) == dict


def test_getFavoriteTracks(client, token):
    response = client.get('/spotify/user/favorite/tracks', headers=token)
    assert response.status_code == 200
    assert 'spotify:track:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getPlaylists(client, token):
    response = client.get('/spotify/playlists/workout', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert 'workout' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getUserPlaylists(client, token):
    response = client.get('/spotify/user/playlists', headers=token)
    assert response.status_code == 200
    assert 'spotify:playlist:' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict


def test_getArtist(client, token):
    response = client.get('/spotify/artist/Queen', headers=token)
    assert response.status_code == 200
    assert 'spotify:artist:' in str(json.loads(response.data))
    assert 'Queen' in str(json.loads(response.data))
    assert type(json.loads(response.data)) == dict
