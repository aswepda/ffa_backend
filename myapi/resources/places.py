from flask_restful import Resource
from flask import g


class Places(Resource):
    def get_events(self):
        credentials = g.get('googleUser').to_json()
        var = common.speech_utility.google_places('-33.8670522,151.1957362')
        return