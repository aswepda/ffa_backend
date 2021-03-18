import spotipy
from collections import Counter
from datetime import datetime
import json


def getAlbumFromArtist(sp, albumName, artistName):
    '''
    desc:
     - get album based on album name and exactly matching artist name
    param:
     - authenticated spotify api instance
     - name of album
     - name of artist
    return:
     - list of Spotify-URI of albums
     - JSON with:
        - message to read out loud
        - list of JSON objects of albums
            - album URI
            - album name
            - List of artists
            - track count
            - release date
    '''
    albumsList = []
    albums = sp.search(q='album:' + albumName + ' artist:' + artistName, type='album', market='DE')
    for album in albums['albums']['items']:
        artists = []
        isFromArtist = False
        for artist in album['artists']:
            artists.append(artist['name'])
            artistString = str(artists).replace('\'', '').replace('[', '').replace(']', '')
            # return album only if artistName matches exactly
            if str.lower(artist['name']) == str.lower(artistName):
                isFromArtist = True
        if isFromArtist == True:
            albumJson = {"uri": album['uri'],
                         "name": album['name'],
                         "artist": artistString,
                         "track_count": album['total_tracks'],
                         "release": album['release_date']}
            albumsList.append(albumJson)
    data = {"message": 'Ich habe folgende Alben mit dem Namen ' + albumName + ' von ' + artistName + ' gefunden:',
            "data": albumsList,
            "speakMessage": True}
    return data


def getArtist(sp, name):
    '''
    desc:
     - get artist based on name
    param:
     - authenticated spotify api instance
     - name of artist
    return:
     - JSON with:
        - message to read out loud
        - list of JSON objects of artists with matching name:
            - artist URI
            - artist name
            - List of artist genres
            - artist follower count
    '''
    # search artist
    artistsList = []
    artists = sp.search(q='artist:' + name, type='artist')
    # return Artist only if name matches exactly
    for artist in artists['artists']['items']:
        if str.lower(artist['name']) == str.lower(name):
            artistsList.append(artist['uri'])
            artistJson = {"uri": artist['uri'],
                          "name": artist['name'],
                          "genres": artist['genres'],
                          "followers": artist['followers']['total']}
            artistsList.append(artistJson)
        data = {"message": 'Hier hast du den Interpreten ' + name,
                "data": artistsList,
                "speakMessage": True}
    return data


def getPlaylists(sp, name):
    '''
    desc:
     - get playlists of current user
     - if the user doesn't have a playlist with that name, return other public playlists with a matching name
    param:
     - authenticated spotify api instance
     - name of playlist
    return:
     - JSON with:
        - message to read out loud
        - list of JSON objects of playlists with matching name:
            - playlists URI
            - playlists name
            - playlists description
            - playlists owner
            - track count
    '''
    userPlaylistsWithName = getUserPlaylists(sp, name)
    if userPlaylistsWithName['data'] != []:
        return userPlaylistsWithName
    else:
        playlistsList = []
        playlists = sp.search(q='playlist:' + name, type='playlist')
        for playlist in playlists['playlists']['items']:
            playlistJson = {"uri": playlist['uri'],
                            "name": playlist['name'],
                            "description": playlist['description'],
                            "owner": playlist['owner']['display_name'],
                            "track_count": playlist['tracks']['total']}
            playlistsList.append(playlistJson)
    data = {"message": 'Hier sind ' + name + ' Playlists:',
            "data": playlistsList,
            "speakMessage": True}
    return data


def getUserPlaylists(sp, name=None):
    '''
    desc:
     - get playlists of current user
     - if a name is given, return only playlists with matching name
    param:
     - authenticated spotify api instance
     - name of playlist (optional)
    return:
     - JSON with:
        - message to read out loud
        - list of JSON objects of public user playlists:
            - playlists URI
            - playlists name
            - playlists description
            - playlists owner
            - track count
    '''
    playlistsList = []
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if name is None or str.lower(name) in str.lower(playlist['name']):
            playlistJson = {"uri": playlist['uri'],
                            "name": playlist['name'],
                            "description": playlist['description'],
                            "owner": playlist['owner']['display_name'],
                            "track_count": playlist['tracks']['total']}
            playlistsList.append(playlistJson)
    if name is None:
        data = {"message": 'Hier sind alle deine Playlists',
                "data": playlistsList,
                "speakMessage": True}
    else:
        data = {"message": 'Hier sind alle deine Playlists mit dem Namen ' + name,
                "data": playlistsList,
                "speakMessage": True}
    return data


def getFavoriteTracks(sp):
    '''
    desc:
     - get favorite tracks from user
    param:
     - authenticated spotify api instance
    return:
     - JSON with:
        - message to read out loud
        - list of JSON objects of favorite tracks:
            - track URI
            - track name
            - track album
            - track artist
    '''
    favoriteTracksList = []
    for j in range(0, 5, 49):
        favoriteTracks = sp.current_user_top_tracks(limit=49, offset=j, time_range='medium_term')
        for track in favoriteTracks['items']:
            artists = []
            for artist in track['artists']:
                artists.append(artist['name'])
            artistString = str(artists).replace('\'', '').replace('[', '').replace(']', '')
            trackJson = {"uri": track['uri'],
                         "name": track['name'],
                         "album": track['album']['name'],
                         "artist": artistString}
            favoriteTracksList.append(trackJson)
    data = {"message": 'Hier sind deine Lieblings Lieder:',
            "data": favoriteTracksList,
            "speakMessage": True}
    return data


def getFavoriteArtists(sp, genre=None):
    '''
    desc:
     - get favorite artists from user
    param:
     - authenticated spotify api instance
     - genre: optional, if set, artists need to have music of that genre
    return:
     - JSON with:
        - message to read out loud
        - list of JSON objects of favorite artists (of the given genre):
            - artist URI
            - artist name
            - List of artist genres
            - artist follower count
    '''
    favoriteArtistsList = []
    for j in range(0, 100, 49):
        favoriteArtists = sp.current_user_top_artists(limit=49, offset=j, time_range='medium_term')
        for artist in favoriteArtists['items']:
            if genre is None or str.lower(genre) in artist['genres']:
                artistJson = {"uri": artist['uri'],
                              "name": artist['name'],
                              "genres": artist['genres'],
                              "followers": artist['followers']['total']}
                favoriteArtistsList.append(artistJson)
    if genre is None:
        data = {"message": 'Hier sind deine Lieblings Interpreten',
                "data": favoriteArtistsList,
                "speakMessage": True}
    else:
        data = {"message": 'Hier sind deine Lieblings Interpreten aus dem Genre ' + genre,
                "data": favoriteArtistsList,
                "speakMessage": True}
    return data


def getFavoriteGenres(sp):
    '''
    desc:
     - get favorite genres from user (based on top 98 Artists genres)
    param:
     - authenticated spotify api instance
    return:
     - JSON with:
        - message to read out loud
        - list of favorite genres sorted by decreasing popularity 
    '''
    genres = []
    favoriteArtists = sp.current_user_top_artists(limit=50, offset=0, time_range='medium_term')
    for artist in favoriteArtists['items']:
        for element in artist['genres']:
            genres.append(element)
    genresList = [key for key, _ in Counter(genres).most_common(50)]
    data = {"message": 'Hier sind deine Lieblings Genres:',
            "data": genresList,
            "speakMessage": True}
    return data


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
    recommendedTracks = sp.recommendations(seed_artists=artistList, seed_genres=genreList, seed_tracks=trackList, limit=50, country='from_token')
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
     - playlist Json
    '''
    userID = sp.me()['id']
    newPlaylist = sp.user_playlist_create(userID, playlistName, public=False, collaborative=False, description=playlistDescription)
    sp.user_playlist_add_tracks(userID, newPlaylist['id'], uri_list)
    return newPlaylist


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
     - JSON with:
        - message to read out loud
        - playlist URI
        - playlist name
        - playlist description
    '''
    favoriteGenreArtists = getFavoriteArtists(sp, genre)
    if str.lower(genre) in sp.recommendation_genre_seeds()['genres']:
        recommended_tracks = getRecommendations(sp, artistList=favoriteGenreArtists[:4], genreList=[genre])
    elif favoriteGenreArtists != []:
        recommended_tracks = getRecommendations(sp, artistList=favoriteGenreArtists[:5])
    else:
        return getPlaylists(sp, genre)
    playlist = createPlaylistFromUriList(sp, recommended_tracks, "tolle " + genre + " Lieder", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
    data = {"message": 'Hier sind tolle ' + genre + ' Lieder, die dir gefallen könnten',
            "data": {"uri": playlist['uri'],
                     "name": playlist['name'],
                     "description": playlist['description']},
            "speakMessage": True}
    return data


def playMusicFromYear(sp, year):
    '''
    desc:
     - add the spotify public top 50 songs from a year to a new playlist
    param:
     - authenticated spotify api instance
     - year
    return:
     - JSON with:
        - message to read out loud
        - playlist URI
        - playlist name
        - playlist description
    '''
    yearTracksUriList = []
    track_results = sp.search(q='year:' + year, type='track', limit=50, market='DE')
    for track in track_results['tracks']['items']:
        yearTracksUriList.append(track['uri'])
    playlist = createPlaylistFromUriList(sp, yearTracksUriList, year + " Mix", "automatisch erstellt von FFA am " + datetime.now().strftime("%d.%m.%Y um %H:%M"))
    data = {"message": 'Hier sind die Top Lieder aus dem Jahr' + year,
            "data": {"uri": playlist['uri'],
                     "name": playlist['name'],
                     "description": playlist['description']},
            "speakMessage": True}
    return data
