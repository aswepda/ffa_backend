import spotipy
from collections import Counter
from datetime import datetime


# Return json:
# {'message': 'Dies ist eine Nachricht.', 'data': {}, 'speakMessage': true}



def getAlbumFromArtist(sp, albumName, artistName):
        albumsUriList = []
        albums = sp.search(q='album:'+ albumName + ' artist:' + artistName , type='album', market='DE')
        print(albums)
        #return album only if artistName matches exactly
        
        for album in albums['albums']['items']:
                if str.lower(album['artists'][0]['name']) == str.lower(artistName):
                        albumsUriList.append(album['uri'])
        return albumsUriList

def getArtist(sp, name):
        #search artist
        artistsUriList = []
        artists = sp.search(q='artist:'+ name , type='artist')
        #return Artist only if name matches exactly
        for artist in artists['artists']['items']:
                if str.lower(artist['name']) == str.lower(name):
                        artistsUriList.append(artist['uri'])
        return artistsUriList

def getPlaylists(sp, name):
        userPlaylistsWithName = getUserPlaylists(sp, name)
        if userPlaylistsWithName != []:
                return userPlaylistsWithName
        else:
                playlistsUriList = []
                playlists = sp.search(q='playlist:'+ name , type='playlist')
                for playlist in playlists['playlists']['items']:
                        playlistsUriList.append(playlist['uri'])
                return playlistsUriList
               
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
                                favoriteArtistsUriList.append(artist['name'])
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
         - recommendation is based on 4 artists + genre or on 5 artists if genre is not available
         - see sp.recommendation_genre_seeds()['genres'] for available genres
        param:
         - genre: genre of which the recommendation is based on
        return:
         - playlist-URI
        '''
        favoriteGenreArtists = getFavoriteArtists(sp, genre)
        if str.lower(genre) in sp.recommendation_genre_seeds()['genres']:
                recommended_tracks = getRecommendations(sp, artistList=favoriteGenreArtists[:4], genreList=[genre])
        elif favoriteGenreArtists != []:
                recommended_tracks = getRecommendations(sp, artistList=favoriteGenreArtists[:5])
        else:
                return "not possible for this genre"
        playlist_uri = createPlaylistFromUriList(sp, recommended_tracks, "tolle " + genre + " Lieder", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
        return playlist_uri

def playMusicFromYear(sp, year):
        yearTracksUriList = []
        track_results = sp.search(q='year:'+ year, type='track', limit=50, market='DE')
        for i, track in enumerate(track_results['tracks']['items']):
                #print(j + i + 1, t['artists'][0]['name'], " : ", t['name'], " (",t['uri'], ")")
                yearTracksUriList.append(track['uri'])
        playlist_uri = createPlaylistFromUriList(sp, yearTracksUriList, year + " Mix", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
        return playlist_uri