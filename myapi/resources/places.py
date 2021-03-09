from flask_restful import Resource
from flask import g
import common.google_places as places


class Places(Resource):
    def get(self):
        var = places.google_places('48.7667,9.1833')
        return var