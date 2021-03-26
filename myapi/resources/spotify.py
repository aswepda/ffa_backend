from flask_restful import Resource, abort, request
from flask import g
import common.spotify_auth as auth
import common.spotify_utility as spotify_utility
from functools import wraps

class SpotifyGenre(Resource):
    @auth.spotify_auth
    def get(self, genre):
        sp = g.get('spotify')
        return spotify_utility.playGenre(sp, genre)

class SpotifyYear(Resource):
    @auth.spotify_auth
    def get(self, year):
        sp = g.get('spotify')
        return spotify_utility.playMusicFromYear(sp, year)

class SpotifyArtist(Resource):
    @auth.spotify_auth
    def get(self, artist):
        sp = g.get('spotify')
        return spotify_utility.getArtist(sp, artist)

class SpotifyArtistAlbum(Resource):
    @auth.spotify_auth
    def get(self, artist, album):
        sp = g.get('spotify')
        return spotify_utility.getAlbumFromArtist(sp, album, artist)

class SpotifyPlaylists(Resource):
    @auth.spotify_auth
    def get(self, search):
        sp = g.get('spotify')
        return spotify_utility.getPlaylists(sp, search)

class SpotifyUserPlaylists(Resource):
    @auth.spotify_auth
    def get(self, search = None):
        sp = g.get('spotify')
        return spotify_utility.getUserPlaylists(sp, search)

class SpotifyUserFavoriteTracks(Resource):
    @auth.spotify_auth
    def get(self):
        sp = g.get('spotify')
        return spotify_utility.getFavoriteTracks(sp)

class SpotifyUserFavoriteGenres(Resource):
    @auth.spotify_auth
    def get(self):
        sp = g.get('spotify')
        return spotify_utility.getFavoriteGenres(sp)

class SpotifyUserFavoriteArtists(Resource):
    @auth.spotify_auth
    def get(self):
        sp = g.get('spotify')
        return spotify_utility.getFavoriteArtists(sp, request.args.get('genre'))
