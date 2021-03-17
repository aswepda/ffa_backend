import spotipy
from collections import Counter
from datetime import datetime

# Return json:
# {'message': 'Dies ist eine Nachricht.', 'data': {}, 'speakMessage': true}


def getAlbumFromArtist(sp, albumName, artistName):
    '''
    desc:
     - get album based on album name and artist name
    param:
     - authenticated spotify api instance
     - name of album
     - name of artist
    return:
     - list of Spotify-URI of albums
    '''
    albumsUriList = []
    albums = sp.search(q='album:' + albumName + ' artist:' +
                       artistName, type='album', market='DE')
    print(albums)
    # return album only if artistName matches exactly
    for album in albums['albums']['items']:
        if str.lower(album['artists'][0]['name']) == str.lower(artistName):
            albumsUriList.append(album['uri'])
    return albumsUriList


def getArtist(sp, name):
    '''
    desc:
     - get artist based on name
    param:
     - authenticated spotify api instance
     - name of artist
    return:
     - list of Spotify-URI of artist
    '''
    # search artist
    artistsUriList = []
    artists = sp.search(q='artist:' + name, type='artist')
    # return Artist only if name matches exactly
    for artist in artists['artists']['items']:
        if str.lower(artist['name']) == str.lower(name):
            artistsUriList.append(artist['uri'])
    return artistsUriList


def getPlaylists(sp, name):
    '''
    desc:
     - get playlists of current user
     - if a name is given, return only playlists with matching name
    param:
     - authenticated spotify api instance
     - name of playlist (optional)
    return:
     - list of Spotify-URI of playlists
    '''
    userPlaylistsWithName = getUserPlaylists(sp, name)
    if userPlaylistsWithName != []:
        return userPlaylistsWithName
    else:
        playlistsUriList = []
        playlists = sp.search(q='playlist:' + name, type='playlist')
        for playlist in playlists['playlists']['items']:
            playlistsUriList.append(playlist['uri'])
        return playlistsUriList


def getUserPlaylists(sp, name=None):
    '''
    desc:
     - get playlists of current user
     - if a name is given, return only playlists with matching name
    param:
     - authenticated spotify api instance
     - name of playlist (optional)
    return:
     - list of Spotify-URI of playlists
    '''
    playlistsUriList = []
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if name is None or str.lower(name) in str.lower(playlist['name']):
            playlistsUriList.append(playlist['uri'])
    return playlistsUriList


def getFavoriteTracks(sp):
    '''
    desc:
     - get favorite tracks from user
    param:
     - authenticated spotify api instance
    return:
     - list of Spotify-URI of favorite tracks
    '''
    favoriteTracksUriList = []
    for j in range(0, 100, 49):
        favoriteTracks = sp.current_user_top_tracks(
            limit=49, offset=j, time_range='medium_term')
        for track in favoriteTracks['items']:
            favoriteTracksUriList.append(track['uri'])
    return favoriteTracksUriList


def getFavoriteArtists(sp, genre=None):
    '''
    desc:
     - get favorite artists from user
    param:
     - authenticated spotify api instance
     - genre: optional, if set, artists need to have music of that genre
    return:
     - list of Spotify-URI of favorite artists
    '''
    favoriteArtistsUriList = []
    for j in range(0, 100, 49):
        favoriteArtists = sp.current_user_top_artists(
            limit=49, offset=j, time_range='medium_term')
        for artist in favoriteArtists['items']:
            if genre is None or str.lower(genre) in artist['genres']:
                favoriteArtistsUriList.append(artist['uri'])
    return favoriteArtistsUriList


def getFavoriteGenres(sp):
    '''
    desc:
     - get favorite genres from user (based on top 98 Artists genres)
    param:
     - authenticated spotify api instance
    return:
     - list of favorite genres sorted by decreasing popularity 
    '''
    genres = []
    favoriteArtists = sp.current_user_top_artists(
        limit=50, offset=0, time_range='medium_term')
    for artist in favoriteArtists['items']:
        for element in artist['genres']:
            genres.append(element)
    genresList = [key for key, _ in Counter(genres).most_common(50)]
    return genresList


def getRecommendations(sp, artistList=None, genreList=None, trackList=None):
    '''
    desc:
     - get gecommendations based on given artists / genres / tracks
     - at least one artist / genre / track needs to be given
    param:
     - authenticated spotify api instance
     - list of artists (optional)
     - list of genres (optional)
     - list of tracks (optional)
    return:
     - list of recommended track uris
    '''
    recommendedTracksUriList = []
    recommendedTracks = sp.recommendations(
        seed_artists=artistList, seed_genres=genreList, seed_tracks=trackList, limit=50, country='from_token')
    for track in recommendedTracks['tracks']:
        recommendedTracksUriList.append(track['uri'])
    return recommendedTracksUriList


def createPlaylistFromUriList(sp, uri_list, playlistName, playlistDescription):
    '''
    desc:
     - create a new playlist and add al tracks from uri_list to it
    param:
     - authenticated spotify api instance
     - list of tracks
     - name for new playlist
     - description for new playlist
    return:
     - playlist-URI
    '''
    userID = sp.me()['id']
    newPlaylist = sp.user_playlist_create(
        userID, playlistName, public=False, collaborative=False, description=playlistDescription)
    sp.user_playlist_add_tracks(userID, newPlaylist['id'], uri_list)
    return newPlaylist['uri']


def playGenre(sp, genre):
    '''
    desc:
     - create Playlist with only a genre given
     - recommendation is based on 4 artists + genre or on 5 artists if genre is not available
     - see sp.recommendation_genre_seeds()['genres'] for available genres
    param:
     - authenticated spotify api instance
     - genre: genre of which the recommendation is based on
    return:
     - playlist-URI
    '''
    favoriteGenreArtists = getFavoriteArtists(sp, genre)
    if str.lower(genre) in sp.recommendation_genre_seeds()['genres']:
        recommended_tracks = getRecommendations(
            sp, artistList=favoriteGenreArtists[:4], genreList=[genre])
    elif favoriteGenreArtists != []:
        recommended_tracks = getRecommendations(
            sp, artistList=favoriteGenreArtists[:5])
    else:
        return "not possible for this genre"
    playlist_uri = createPlaylistFromUriList(sp, recommended_tracks, "tolle " + genre + " Lieder",
                                             "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
    return playlist_uri


def playMusicFromYear(sp, year):
    '''
    desc:
     - add the spotify public top 50 songs from a year to a new playlist
    param:
     - authenticated spotify api instance
     - year
    return:
     - playlist-URI
    '''
    yearTracksUriList = []
    track_results = sp.search(
        q='year:' + year, type='track', limit=50, market='DE')
    for track in track_results['tracks']['items']:
        yearTracksUriList.append(track['uri'])
    playlist_uri = createPlaylistFromUriList(
        sp, yearTracksUriList, year + " Mix", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
    return playlist_uri
