from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.speech import Speech
from resources.auth import GoogleAuth
from resources.google import Google
from resources.calendar import Calendar
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
api.add_resource(Google, '/google')
api.add_resource(Calendar, '/calendar/<string:time>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, threaded=True, port=port, host='0.0.0.0')
    