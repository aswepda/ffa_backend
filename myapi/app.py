from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from resources.speech import Speech
from resources.auth import GoogleAuth, SpotifyAuth
from resources.calendar import Calendar
from resources.places import Places
from resources.lunchbreak import Lunchbreak
from resources.weather import Weather
from resources.directions import Directions
from resources.spotify import SpotifyGenre, SpotifyYear, SpotifyArtist, SpotifyArtistAlbum, SpotifyPlaylists, SpotifyUserPlaylists, SpotifyUserFavoriteTracks, SpotifyUserFavoriteGenres, SpotifyUserFavoriteArtists
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
api.add_resource(Calendar, '/calendar/<string:time>')
api.add_resource(Places, '/places')
api.add_resource(Lunchbreak, '/lunchbreak')
api.add_resource(Weather, '/weather/<string:time>')
api.add_resource(Directions, '/directions/<string:origin>/<string:mode>/<string:destination>')

## SPOTIFY
api.add_resource(SpotifyGenre, '/spotify/genre/<string:genre>')
api.add_resource(SpotifyYear, '/spotify/year/<string:year>')
api.add_resource(SpotifyArtistAlbum, '/spotify/artist/<string:artist>/<string:album>')
api.add_resource(SpotifyArtist, '/spotify/artist/<string:artist>')
api.add_resource(SpotifyPlaylists, '/spotify/playlists/<string:search>')
api.add_resource(SpotifyUserPlaylists, '/spotify/user/playlists', '/spotify/user/playlists/<string:search>')
api.add_resource(SpotifyUserFavoriteTracks, '/spotify/user/favorite/tracks')
api.add_resource(SpotifyUserFavoriteGenres, '/spotify/user/favorite/genres')
api.add_resource(SpotifyUserFavoriteArtists, '/spotify/user/favorite/artists')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # pragma: no cover
    app.run(debug=True, threaded=True, port=port,
            host='0.0.0.0')  # pragma: no cover
