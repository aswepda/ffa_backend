from flask_restful import Resource
from flask import g
import common.google_auth as auth

class Google(Resource):
    @auth.google_auth
    def get(self):
        return g.get('googleUser').to_json()