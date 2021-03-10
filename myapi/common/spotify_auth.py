from functools import wraps
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from flask import request, g

def spotify_auth(f):
    @wraps(f)
    def spotifyAuthFunction(*args, **kwargs):
        if request.headers.get('Authorization') is not None:
            refresh_code = request.headers.get('Authorization')
            authObj = SpotifyOAuth(client_id='d5550bed36f64690a6d2ae32d26023bd', client_secret='317ee1ad087448bbb8316ad86a9f39a1', redirect_uri='https://aswepda.surge.sh/#/', open_browser=False)
            accessDict = authObj.refresh_access_token(refresh_code)
            g.spotify = spotipy.Spotify(auth=accessDict['access_token'])
        return f(*args, **kwargs)
    return spotifyAuthFunction
