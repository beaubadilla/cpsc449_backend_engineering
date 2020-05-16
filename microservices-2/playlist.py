# Using some code from https://github.com/ProfAvery/cpsc449/tree/master/flaskapi-pugsql

import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Available endpoints: </h1>
    <h2>Playlists: </h2>
<ol><li><a href="/api/v1/playlists">Create playlist</a><p>{
    "PlaylistName": "sample playlist",
    "UserId": "1",
    "Description": "Sample Description",
    "Tracks": [{"TrackId": 4}, {"TrackId": 1}, {"TrackId": 3}]
}</p></li><li><a href="/api/v1/playlists?id=1">Retieve a playlist</a></li><li><a href="/api/v1/users/playlists/1">Delete a track</a></li><li><a href="/api/v1/playlists">List all playlists</a></li><li><a href="/api/v1/playlists?uid=1">Retrieve playlists by a user</a></li></ol>'''


# endpoint to get all playlists, Create playlist
@app.route('/api/v1/playlists', methods = ['GET', 'POST'])
def playlist_otptions():
    # 'GET' handles the following possibilities:
        # playlists given userID
        # playlist given PlaylistId
        # all playlists
    if request.method == 'GET':
        return get_playlist(request.args)

    elif request.method == 'POST':
        return create_playlist(request.data)

# endpoint to get a playlist by id
@app.route('/api/v1/users/playlists/<int:id>', methods = ['GET', 'DELETE'])
def playlist_id(id):
    id = {
        'id': id
    }
    if request.method == 'GET':
        return get_playlist(id)
    elif request.method == 'DELETE':
        return delete_playlist(id)

# endpoint to add a track
@app.route('/api/v1/users/<int:UserId>/playlists/<int:PlaylistId>/tracks', methods = ['POST'])
def add_track(UserId, PlaylistId):
    playlistInfo = request.data
    playlistInfo['PlaylistId'] = PlaylistId
    required_fields = ['PlaylistId', 'TrackId']
    if not all([field in playlistInfo for field in required_fields]):
        raise exceptions.ParseError()
    return add_to_playlist(playlistInfo)

@app.route('/api/v1/users/<int:UserId>/playlists/<int:PlaylistId>/tracks/<int:TrackId>', methods = ['DELETE'])
def delete_track_playlist(UserId, TrackId, PlaylistId):
    track = {
        'TrackId': TrackId,
        'PlaylistId': PlaylistId
    }
    return delete_playlist_track(track)


# gets playlist tracks, playlist name, playlist description
def get_playlist(playlist):
    # if playlist id is given, then return all track urls from that playlist
    if 'id' in playlist:
        playlist = {
            "PlaylistId": playlist['id']
        }
        try:
            playlist = queries.playlist_all_track_url(**playlist)
        except Exception as e:
            return e
        playlist = list(playlist)

    # if there is a userid given, then return all playlist from that user
    elif 'uid' in playlist:
        playlist = {
            "UserId": playlist['uid']
        }
        try:
            playlist = queries.all_playlist_by_userid(**playlist)
        except Exception as e:
            return e
        playlist = list(playlist)

    # If no id is given, then return all playlists
    else:
        try:
            playlist = queries.all_playlist_all_track_url()
        except Exception as e:
            return e
        playlist = list(playlist)

    # if playlist is empty then it does not exist in DB.
    if playlist:
        return playlist, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()

# creates a playlist and adds tracks
def create_playlist(playlistInfo):
    playlistInfo = request.data
    required_fields = ['PlaylistName', 'UserId', 'Tracks']
    if not all([field in playlistInfo for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if not isinstance(playlistInfo['Tracks'], list):
            raise exceptions.ParseError()
        if not 'Description' in playlistInfo.keys():
            playlistInfo['Description'] = None
        # insert playlist into table
        playlistInfo['PlaylistId'] = queries.create_playlist(**playlistInfo)
        try:
            # insert tracks of playlists into 'PlaylistTrack' table
            for track in playlistInfo['Tracks']:
                track['PlaylistId'] = playlistInfo['PlaylistId']
                track = add_to_playlist(track)
        except Exception as e:
            return { 'error': str(e) }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    PlaylistId = playlistInfo['PlaylistId']
    location_url = f'http://localhost:5200/api/v1/users/playlists/{PlaylistId}'
    return playlistInfo, status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url}

# Adds a track into playlist, must pass in 'TrackId' and 'PlaylistId'
def add_to_playlist(track):
    required_fields = ['PlaylistId', 'TrackId']
    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        check = queries.track_by_id(**track)
        if check:
            check = queries.playlist_by_id(**track)
            if check:
                track = queries.add_track_to_playlist(**track)
            else:
                return {"error": "Playlist does not exist."}, status.HTTP_400_BAD_REQUEST
        else:
            return {"error": "Track does not exist."}, status.HTTP_400_BAD_REQUEST

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    if track:
        return {"info": "Successfully added track."}, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()

# deletes playlist from playlist table and deletes all \
    # playlist tracks from table PlaylistTrack
def delete_playlist(playlist):

    playlist['PlaylistId'] = playlist['id']
    try:
        queries.delete_playlist_track_by_id(**playlist)
        playlist = queries.delete_playlist_by_id(**playlist)

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    if playlist:
        return {"info": "Successfully deleted"}, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()

# Track removed from playlist given 'PlaylistId' and 'TrackId'
def delete_playlist_track(track):
    try:
        track = queries.delete_track_from_playlist(**track)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    if track:
        return {"info": "Successfully deleted"}, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()
