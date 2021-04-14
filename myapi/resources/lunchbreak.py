from flask_restful import Resource, abort
from flask import g
import common.google_auth as auth
import common.calendar_utility as calendar
import json

class Lunchbreak(Resource):
    @auth.google_auth
    def get(self):
        credentials = g.get('googleUser')
        if credentials:
            events = calendar.calendar_events(credentials, 'lunch')
            lunchtime = calendar.get_lunchtime(events)
        else:
            return abort(403, message="No Access granted")
        
        return lunchtime
