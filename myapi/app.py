from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.speech import Speech
from resources.auth import GoogleAuth, SpotifyAuth
from resources.google import Google
from resources.calendar import Calendar
from resources.places import Places
from resources.lunchbreak import Lunchbreak
from resources.weather import Weather
from resources.spotitest import SpotiTest
import os

# https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html#project-structure

app = Flask(__name__)
app.secret_key = 'pda_backend'
CORS(app, supports_credentials=True)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

api.add_resource(Speech, '/speech')
api.add_resource(GoogleAuth, '/auth/google')
api.add_resource(SpotifyAuth, '/auth/spotify')
api.add_resource(Google, '/google')
api.add_resource(Calendar, '/calendar/<string:time>')
api.add_resource(Places, '/places')
api.add_resource(Lunchbreak, '/lunchbreak')
api.add_resource(Weather, '/weather')
api.add_resource(SpotiTest, '/spotitest')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000)) # pragma: no cover
    app.run(debug=True, threaded=True, port=port, host='0.0.0.0') # pragma: no cover
