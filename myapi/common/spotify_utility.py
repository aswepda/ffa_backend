import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import common.spotify_auth as auth
from flask_restful import Resource, abort, request
from flask import g
from collections import Counter
from datetime import datetime

class Spotify(Resource):
        @auth.spotify_auth
        def get(self,function):
                sp = g.get('spotify')
                args = request.args
                # TODO requests mit blank funktionieren nicht
                if sp is None:
                        return abort(403, message='Unauthorized!')
                if function == 'playGenre' and args['genre']:
                        return playGenre(sp, args['genre'])
                if function == 'getFavoriteArtists':
                        if args['genre']:
                                return getFavoriteArtists(sp, args['genre'])
                        else:
                                # TODO das tut noch nicht
                                return getFavoriteArtists(sp)
                if function == 'getFavoriteGenres':
                        return getFavoriteGenres(sp)
                if function == 'getFavoriteTracks':
                        return getFavoriteTracks(sp)
                if function == 'getUserPlaylists':
                        if args['name']:
                                return getUserPlaylists(sp, args['name'])
                        else:
                                # TODO das tut noch nicht
                                return getUserPlaylists(sp)
                if function == 'getArtist' and args['name']:
                        return getArtist(sp, args['name'])

'''
#get album
album_result = sp.album('spotify:album:7cX5qEjIAFq8iL5JW2jedw')
print(album_result)

#recently played
recently_played = sp.current_user_recently_played()
recently_played_uri_list = []
#print result
for idx, track in enumerate(recently_played['items']['track]):
        print(idx, track['artists'][0]['name'], " – ", track['name'] , " (",track['uri'], ")")
        recently_played_uri_list.append(track['uri'])

# spotify best tracks of certain years
artist_name = []
track_name = []
popularity = []
track_id = []
print("2012:")
print("#######################################################")
for j in range(0,10,50):
track_results = sp.search(q='year:2012', type='track', limit=50,offset=j, market='from_token')
for i, t in enumerate(track_results['tracks']['items']):
        print(j + i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")
'''
# Return json:
# {'message': 'Dies ist eine Nachricht.', 'data': {}, 'speakMessage': true}

def getArtist(sp, name):
        #search artist
        artistsUriList = []
        artists = sp.search(q='artist:'+ name , type='artist')
        #return Artist only if name matches exactly
        for artist in artists['artists']['items']:
                if str.lower(artist['name']) == str.lower(name):
                        artistsUriList.append(artist['uri'])
        return artistsUriList

def getUserPlaylists(sp, name=None):
        #get playlists of current user
        playlistsUriList = []
        playlists = sp.current_user_playlists()
        for i, playlist in enumerate(playlists['items']):
                if name is None or str.lower(name) in str.lower(playlist['name']):
                        #print(i, playlist['name'], ": ", playlist['description'], " , uri: ", playlist['uri'])
                        playlistsUriList.append(playlist['uri'])
        return playlistsUriList

def getFavoriteTracks(sp):
        # get favorite tracks from user
        favoriteTracksUriList = []
        for j in range(0,100,49):
                favoriteTracks = sp.current_user_top_tracks(limit=49, offset=j, time_range='medium_term')
                for i, track in enumerate(favoriteTracks['items']):
                        #print(j + i, track['artists'][0]['name'], " : ", track['name'], " (",track['uri'], ")")
                        favoriteTracksUriList.append(track['uri'])
        return favoriteTracksUriList

def getFavoriteArtists(sp, genre=None):
        '''
        desc:
         - get favorite artists from user
        param:
         - genre: optional, if set, artists need to have music of that genre
        return:
         - list of Spotify-URI of favorite artists
        '''
        favoriteArtistsUriList = []
        for j in range(0,100,49):
                favoriteArtists = sp.current_user_top_artists(limit=49, offset=j, time_range='medium_term')
                for i, artist in enumerate(favoriteArtists['items']):
                        if genre is None or str.lower(genre) in artist['genres']:
                                #print(j + i, artist['name'], " (",artist['uri'], "): ", artist['genres'])
                                favoriteArtistsUriList.append(artist['uri'])
        return favoriteArtistsUriList

def getFavoriteGenres(sp):
        # get favorite genres from user (based on top 98 Artists genres)
        genres = []
        favoriteArtists = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
        for i, artist in enumerate(favoriteArtists['items']):
                for element in artist['genres']:
                        genres.append(element)
        genresList = [key for key, _ in Counter(genres).most_common(50)]
        return genresList

def getRecommendations(sp, artistList=None, genreList=None, trackList=None):
        #get recommendations based on track list
        recommendedTracksUriList = []
        recommendedTracks = sp.recommendations(seed_artists=artistList, seed_genres=genreList, seed_tracks=trackList, limit=50, country='from_token')
        for i, track in enumerate(recommendedTracks['tracks']):
                #print(i, track['artists'][0]['name'], " : ", track['name'], " (",track['uri'], ")")
                recommendedTracksUriList.append(track['uri'])
        return recommendedTracksUriList

def createPlaylistFromUriList(sp, uri_list, playlistName, playlistDescription):
        #create playlist from uri_list
        userID = sp.me()['id']
        newPlaylist = sp.user_playlist_create(userID, playlistName, public=False, collaborative=False, description=playlistDescription)
        sp.user_playlist_add_tracks(userID, newPlaylist['id'], uri_list)
        return newPlaylist['uri']


def playGenre(sp, genre):
        '''
        desc:
         - create Playlist with only a genre given
         - see sp.recommendation_genre_seeds()['genres'] for available genres
        param:
         - genre: genre of which the recommendation is based on
        return:
         - playlist-URI
        '''
        if str.lower(genre) in sp.recommendation_genre_seeds()['genres']:
                favoriteGenreArtists = getFavoriteArtists(sp, genre)
                recommended_tracks = getRecommendations(sp, artistList=favoriteGenreArtists[:4], genreList=[genre])
                playlist_uri = createPlaylistFromUriList(sp, recommended_tracks, "tolle " + genre + " Lieder", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
                return playlist_uri
        return "not possible for this genre"