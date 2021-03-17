from flask_restful import Resource, abort, request
from flask import g
import common.spotify_auth as auth
import common.spotify_utility as spotify_utility

class Spotify(Resource):
        @auth.spotify_auth
        def get(self,function):
                sp = g.get('spotify')
                args = request.args
                if sp is None:
                        return abort(403, message='Unauthorized!')
                if function == 'playGenre' and args['genre']:
                        return spotify_utility.playGenre(sp, args['genre'])
                if function == 'playYear' and args['year']:
                        return spotify_utility.playMusicFromYear(sp, args['year'])
                if function == 'getFavoriteArtists':
                        if "genre" in args:
                                return spotify_utility.getFavoriteArtists(sp, args['genre'])
                        else:
                                return spotify_utility.getFavoriteArtists(sp)
                if function == 'getFavoriteGenres':
                        return spotify_utility.getFavoriteGenres(sp)
                if function == 'getFavoriteTracks':
                        return spotify_utility.getFavoriteTracks(sp)
                if function == 'getPlaylists' and args['name']:
                        return spotify_utility.getPlaylists(sp, args['name'])
                if function == 'getUserPlaylists':
                        if "name" in args:
                                return spotify_utility.getUserPlaylists(sp, args['name'])
                        else:
                                return spotify_utility.getUserPlaylists(sp)
                if function == 'getArtist' and args['name']:
                        return spotify_utility.getArtist(sp, args['name'])
                if function == 'getAlbumFromArtist' and args['album'] and args['artist']:
                        return spotify_utility.getAlbumFromArtist(sp, args['album'], args['artist'])
                

