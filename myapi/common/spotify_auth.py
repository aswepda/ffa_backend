from functools import wraps
from spotipy.oauth2 import SpotifyOAuth
from common.spotify_cache_void import CacheVoid
import spotipy
from flask import request, g
from flask_restful import abort

def spotify_auth(f):
    @wraps(f)
    def spotifyAuthFunction(*args, **kwargs):
        if request.headers.get('Authorization') is not None:
            refresh_code = request.headers.get('Authorization')
            authObj = SpotifyOAuth(client_id='d5550bed36f64690a6d2ae32d26023bd', client_secret='7bb9fade755943888c8e27522498b2ed', redirect_uri='https://ffagent.eu.org/#/', open_browser=False, cache_handler=CacheVoid())
            accessDict = authObj.refresh_access_token(refresh_code)
            g.spotify = spotipy.Spotify(auth=accessDict['access_token'])
        if g.get('spotify') is None:
            return abort(403, message='Unauthorized!')
        return f(*args, **kwargs)
    return spotifyAuthFunction
