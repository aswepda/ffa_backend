from flask_restful import Resource, abort, request
from flask import g
import common.spotify_auth as auth
import common.spotify_utility as spotify_utility


class Spotify(Resource):
    @auth.spotify_auth
    def get(self, function):
        sp = g.get('spotify')
        args = request.args
        # calls corresponding function based on GET request
        if sp is None:
            return abort(403, message='Unauthorized!')
        elif function == 'playGenre' and args['genre']:
            return spotify_utility.playGenre(sp, args['genre'])
        elif function == 'playYear' and args['year']:
            return spotify_utility.playMusicFromYear(sp, args['year'])
        elif function == 'getFavoriteArtists':
            if "genre" in args:
                return spotify_utility.getFavoriteArtists(sp, args['genre'])
            else:
                return spotify_utility.getFavoriteArtists(sp)
        elif function == 'getFavoriteGenres':
            return spotify_utility.getFavoriteGenres(sp)
        elif function == 'getFavoriteTracks':
            return spotify_utility.getFavoriteTracks(sp)
        elif function == 'getPlaylists' and args['name']:
            return spotify_utility.getPlaylists(sp, args['name'])
        elif function == 'getUserPlaylists':
            if "name" in args:
                return spotify_utility.getUserPlaylists(sp, args['name'])
            else:
                return spotify_utility.getUserPlaylists(sp)
        elif function == 'getArtist' and args['name']:
            return spotify_utility.getArtist(sp, args['name'])
        elif function == 'getAlbumFromArtist' and args['album'] and args['artist']:
            return spotify_utility.getAlbumFromArtist(sp, args['album'], args['artist'])