from flask_restful import Resource, abort
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask import g, request
import os
import json
import common.google_auth as auth
import common.spotify_auth as spauth
from common.spotify_cache_void import CacheVoid
import base64

dirname = os.path.dirname(__file__)

class GoogleAuth(Resource):
    #method_decorators = {'get': [google_auth]}

    def post(self):
        req_json = request.get_json()
        filename = os.path.join(dirname, '../common/client_secret.json')
        with open(filename, 'r') as secret_file:
            data=secret_file.read()
        obj = json.loads(data)
        google_secret = os.getenv('GOOGLE_SECRET')
        obj['web']['client_secret'] = google_secret
        flow = Flow.from_client_config(
            obj, scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri='postmessage')
        flow.fetch_token(code=req_json['code'])
        google_credentials = flow.credentials.to_json()
        encoded_credentials = str(base64.b64encode(google_credentials.encode('ascii')), 'ascii', 'ignore')
        return {'message': 'Logged In!', 'credentials': encoded_credentials}

    @auth.google_auth
    def get(self):
        if g.get('googleUser') is None:
            return abort(403, message='Unauthorized!')
        service = build('oauth2', 'v2', credentials=g.get('googleUser'))
        return service.userinfo().get().execute()

class SpotifyAuth(Resource):
    def post(self):
        json = request.get_json()
        secret = os.getenv('SPOTIFY_SECRET')
        authObject = SpotifyOAuth(client_id='d5550bed36f64690a6d2ae32d26023bd', client_secret=secret, redirect_uri='https://ffagent.eu.org/#/', open_browser=False, cache_handler=CacheVoid())
        accessDict = authObject.get_access_token(code=json['code'])
        return {'message': 'Logged In!', 'credentials': accessDict['refresh_token']}

    @spauth.spotify_auth
    def get(self):
        if g.get('spotify') is None:
            return abort(403, message='Unauthorized!')
        sp = g.get('spotify')
        return sp.me()

