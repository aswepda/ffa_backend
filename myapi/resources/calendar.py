from flask_restful import Resource
from flask import g
import common.google_auth as auth
import common.calendar_utility as calendar
import json

class Calendar(Resource):
    @auth.google_auth
    def get(self, time):
        credentials = g.get('googleUser')
        if credentials:
            events = calendar.calendar_events(credentials, time)
        else:
            events = "No Access granted"
        
        return events
