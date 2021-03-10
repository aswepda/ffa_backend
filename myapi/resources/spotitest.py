from flask_restful import Resource, abort
from flask import g
import common.spotify_auth as auth

class SpotiTest(Resource):
    @auth.spotify_auth
    def get(self):
        if g.get('spotify') is None:
            return abort(403, message='Unauthorized!')
        sp = g.get('spotify')
        return sp.me()
