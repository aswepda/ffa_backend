import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_cred
from collections import Counter

#create a permission scope and authenticate
sp_user_top_read = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_cred.client_id, client_secret= spotify_cred.client_secret, redirect_uri=spotify_cred.redirect_url, scope="user-top-read"))
sp_playlist_modify_private = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_cred.client_id, client_secret= spotify_cred.client_secret, redirect_uri=spotify_cred.redirect_url, scope="playlist-modify-private"))
sp_notPersonal = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_cred.client_id, client_secret= spotify_cred.client_secret))


'''
# get related artists
related_artist_result = sp_notPersonal.artist_related_artists('spotify:artist:3K0GDmmiRwn1Zc7RZzTeAz')
print(related_artist_result)

get artist
artist_result = sp_notPersonal.artist('spotify:artist:6CYtFzjQMM00sSC8yZjxCY')
print(artist_result)

#get album
album_result = sp_notPersonal.album('spotify:album:7cX5qEjIAFq8iL5JW2jedw')
print(album_result)

#search artist
results = sp_notPersonal.search(q='artist:Tyala', type='artist')
print(results)

#recently played
recently_played = sp_user_top_read.current_user_recently_played()
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
    track_results = sp_notPersonal.search(q='year:2012', type='track', limit=50,offset=j, market='DE')
    for i, t in enumerate(track_results['tracks']['items']):
        print(j + i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")

'''
def getUserPlaylists():
        #get playlists of current user
        playlistsUriList = []
        playlists = sp_user_top_read.current_user_playlists()
        for i, playlist in enumerate(playlists['items']):
                print(i, playlist['name'], ": ", playlist['description'], " , uri: ", playlist['uri'])
                playlistsUriList.append(playlist['uri'])
        return playlistsUriList


def getFavoriteTracks():
        # get favorite tracks from user
        favoriteTracksUriList = []
        for j in range(0,100,49):
                favoriteTracks = sp_user_top_read.current_user_top_tracks(limit=49, offset=j, time_range='medium_term')
                for i, track in enumerate(favoriteTracks['items']):
                        #print(j + i, track['artists'][0]['name'], " : ", track['name'], " (",track['uri'], ")")
                        favoriteTracksUriList.append(track['uri'])
        return favoriteTracksUriList

def getFavoriteArtists(genre=None):
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
                favoriteArtists = sp_user_top_read.current_user_top_artists(limit=49, offset=j, time_range='medium_term')
                for i, artist in enumerate(favoriteArtists['items']):
                        if genre is None or genre in artist['genres']:
                                #print(j + i, artist['name'], " (",artist['uri'], ")")
                                favoriteArtistsUriList.append(artist['uri'])
        return favoriteArtistsUriList

def getFavoriteGenres():
        # get favorite genres from user (based on top 98 Artists genres)
        genres = []
        for j in range(0,100,49):
                favoriteArtists = sp_user_top_read.current_user_top_artists(limit=49, offset=j, time_range='medium_term')
                for i, artist in enumerate(favoriteArtists['items']):
                        for element in artist['genres']:
                                genres.append(element)
        genresList = [key for key, _ in Counter(genres).most_common(100)]
        return genresList

def getRecommendations(artistList=None, genreList=None, trackList=None):
        #get recommendations based on track list
        recommendedTracksUriList = []
        recommendedTracks = sp_user_top_read.recommendations(seed_artists=artistList, seed_genres=genreList, seed_tracks=trackList, limit=20, country='DE')
        for i, track in enumerate(recommendedTracks['tracks']):
                #print(i, track['artists'][0]['name'], " : ", track['name'], " (",track['uri'], ")")
                recommendedTracksUriList.append(track['uri'])
        return recommendedTracksUriList


def createPlaylistFromUriList(uri_list, playlistName, playlistDescription):
        #create playlist from uri_list
        userID = sp_user_top_read.me()['id']
        newPlaylist = sp_playlist_modify_private.user_playlist_create(userID, playlistName, public=False, collaborative=False, description=playlistDescription)
        sp_playlist_modify_private.user_playlist_add_tracks(userID, newPlaylist['id'], uri_list)
        return newPlaylist['uri']


def createPlaylistfromGenre(genre):
        '''
        desc:
         - create Playlist with only a genre given
         - see sp_user_top_read.recommendation_genre_seeds()['genres'] for available genres
        param:
         - genre: genre of which the recommendation is based on
        return:
         - playlist-URI
        '''
        if genre in sp_user_top_read.recommendation_genre_seeds()['genres']:
                favoriteGenreArtists = getFavoriteArtists(genre)
                recommended_tracks = getRecommendations(artistList=favoriteGenreArtists[:4], genreList=[genre])
                playlist_uri = createPlaylistFromUriList(recommended_tracks, "tolle " + genre + " Lieder", "automatisch erstellt von FFA")
                return playlist_uri
        return "not possible for this genre"



playlist_uri = createPlaylistfromGenre('metalcore')
print(playlist_uri)