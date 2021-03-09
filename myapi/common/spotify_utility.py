import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotify_cred

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


#get playlists of current user
playlists = sp_user_top_read.current_user_playlists(limit=2, offset=0)
print(playlists)
for i, t in enumerate(playlists['items']):
        print(t['name'], ": ", t['description'], " , uri: ", t['uri'])
'''

# get favorite tracks from user
favorite_tracks_uri_list = []
#for j in range(0,100,50):
track_results = sp_user_top_read.current_user_top_tracks(limit=5, offset=0, time_range='long_term')
for i, t in enumerate(track_results['items']):
        print(i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")
        favorite_tracks_uri_list.append(t['uri'])
print(favorite_tracks_uri_list)

'''
print("###################################")
# get favorite tracks from user
#for j in range(0,100,50):
track_results = sp_user_top_read.current_user_top_artists(limit=5, offset=0, time_range='medium_term')
for i, t in enumerate(track_results['items']):
        print(i + 1, t['name'], " : ", t['genres'], " (",t['uri'], ")")


#get recommendations based on genre
recommend = sp_user_top_read.recommendations(seed_artists=None, seed_genres='Rock', seed_tracks=track_uri, limit=5, country='DE')
print(recommend)
'''

#get recommendations based on track list
recommend_tracks_uri_list = []
recommend_tracks = sp_user_top_read.recommendations(seed_artists=None, seed_genres=None, seed_tracks=favorite_tracks_uri_list[:5], limit=50, country='DE')
print(recommend_tracks)
for i, t in enumerate(recommend_tracks['tracks']):
        print(i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")
        recommend_tracks_uri_list.append(t['uri'])
print(recommend_tracks_uri_list)


#create playlist from uri_list
userID = sp_user_top_read.me()['id']
playlistName = "Recommendations based on Favorite tracks"
new_playlist = sp_playlist_modify_private.user_playlist_create(userID, playlistName, public=False, collaborative=False, description='Created on XXX from FFA, Recommendations based on 50 favorite tracks')
sp_playlist_modify_private.user_playlist_add_tracks(userID, new_playlist['id'], recommend_tracks_uri_list)