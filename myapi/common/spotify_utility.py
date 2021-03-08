import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotify_cred

#create a permission scope and authenticate
scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_cred.client_id, client_secret= spotify_cred.client_secret, redirect_uri=spotify_cred.redirect_url, scope=scope))


'''
#query request
results = sp.current_user_recently_played()
#print result
for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'] , " (",track['uri'], ")")


# spotify best tracks of certain years
artist_name = []
track_name = []
popularity = []
track_id = []
print("2005:")
print("#######################################################")
print("#######################################################")
print("#######################################################")
for j in range(0,10,50):
    track_results = sp.search(q='year:2005', type='track', limit=50,offset=j)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
        print(j + i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ") , pop: ", t['popularity'])

#get playlists of current user
playlists = sp.current_user_playlists(limit=50, offset=0)
for i, t in enumerate(playlists['items']):
        print(t['name'], ": ", t['description'], " , uri: ", t['uri'])

'''
for j in range(0,10,50):
        track_results = sp.current_user_top_tracks(limit=50, offset=0, time_range='long_term')
        for i, t in enumerate(track_results['items']):
                print(j + i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")
