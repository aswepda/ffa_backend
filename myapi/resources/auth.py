from flask_restful import Resource, abort
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from flask import request, session, g
import os
import json
import common.google_auth as auth

dirname = os.path.dirname(__file__)

class GoogleAuth(Resource):
    #method_decorators = {'get': [google_auth]}

    def post(self):
        json = request.get_json()
        filename = os.path.join(dirname, '../common/client_secret.json')
        flow = Flow.from_client_secrets_file(
            filename, scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/calendar.events.readonly'],
            redirect_uri='postmessage')
        flow.fetch_token(code=json['code'])
        session['googleSession'] = flow.credentials.to_json()
        return {'message': 'Logged In!'}

    @auth.google_auth
    def get(self):
        if g.get('googleUser') is None:
            return abort(403, message='Unauthorized!')
        service = build('oauth2', 'v2', credentials=g.get('googleUser'))
        return service.userinfo().get().execute()
