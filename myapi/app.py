from flask import Flask
from flask_restful import Resource, Api
from resouces.speech import Speech

# https://flask-restful.readthedocs.io/en/latest/intermediate-usage.html#project-structure

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

api.add_resource(Speech, '/speech')

if __name__ == '__main__':
    app.run(debug=True)