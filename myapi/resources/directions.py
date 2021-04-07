from flask_restful import Resource
from flask import g
import common.google_auth as auth
import common.directions_utility as directions
import json

class Directions(Resource):
    def get(self, origin, mode, destination):
        result = directions.get_direction(origin, mode, destination)
        return result
