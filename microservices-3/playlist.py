# Using some code from https://github.com/ProfAvery/cpsc449/tree/master/flaskapi-pugsql

import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import uuid
from cassandra.cluster import Cluster
from flask_cassandra import CassandraCluster # pip3 install flask-cassandra
from flask import Flask

app = Flask(__name__)
cassandra = CassandraCluster()

app.config['CASSANDRA_NODES'] = ['172.17.02']

session = cassandra.connect()
session.set_keyspace('data')

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
            session.execute("""
                SELECT playlist_name, playlist_description
                    FROM tpd
                    LIMIT 1
                    WHERE user_id = %(playlist_id)s""",
                { 'playlist_id': playlist['PlaylistId'] }
            )
        except Exception as e:
            return e
        playlist = list(playlist)

    # if there is a userid given, then return all playlist from that user
    elif 'uid' in playlist:
        playlist = {
            "UserId": playlist['uid']
        }
        try:
            playlist = session.execute("""
                SELECT playlist_name, playlist_description
                    FROM tpd
                    LIMIT 1
                    WHERE user_id = %(user_id)s""",
                    { 'user_id': playlist['UserId'] }
            )
        except Exception as e:
            return e
        playlist = list(playlist)

    # If no id is given, then return all playlists
    else:
        try:
            playlist = session.execute("""
                SELECT playlist_name, playlist_description
                    FROM tpd
                """,
            )
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
    playlist_id = uuid.uuid4()
    if not all([field in playlistInfo for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if not isinstance(playlistInfo['Tracks'], list):
            raise exceptions.ParseError()
        if not 'Description' in playlistInfo.keys():
            playlistInfo['Description'] = None
        # insert playlist into table
        try:
            # insert tracks of playlists into 'PlaylistTrack' table
            for track in playlistInfo['Tracks']:
                # check if there's a track

                track_already_in_playlist = session.execute("""
                    SELECT track_name, album, artist, length, art
                        WHERE track_id = %(track_id)s AND
                            playlist_id IS NULL AND
                            user_id IS NULL;""",
                        { 'track_id': track['TrackId'] }
                )
                # syntax probably wrong
                if track_already_in_playlist is None:
                    session.execute("""
                        UPDATE tpd
                            SET %(user_id)s, %(playlist_id)s
                            WHERE track_id = %(track_id)s""",
                            { 'user_id': playlistInfo['UserId'], 'playlist_id': playlist_id, 'track_id': track['TrackId'] }
                        )
                else:
                    # Create another partition using the same track info, but new track_id
                        # Allows for searching playlist by either user_id or playlist_id
                    track_id = uuid.uuid4()
                    track['TrackId'] = track_id
                    track_name = track_already_in_playlist['track_name']
                    album = track_already_in_playlist['album']
                    artist = track_already_in_playlist['artist']
                    length = track_already_in_playlist['length']
                    url = track_already_in_playlist['url']
                    art = track_already_in_playlist['art']
                    session.execute("""
                        INSERT INTO tpd (track_id, track_name, album, artist, length, url, art, playlist_id, user_id, playlist_name, playlist_description)
                            VALUES (%(track_id)s, %(track_name)s, %(album)s, %(artist)s, %(length)s, %(url)s, %(art)s, %(playlist_id)s, %(userid)s, %(playlist_name)s, %(playlist_description)s);""",
                            { 'track_id': track_id, 'track_name': track_name, 'album': album, 'artist': artist, 'length': length, 'url': url, 'art': art, 'playlist_id': playlist_id, 'playlist_name': playlistInfo['PlaylistName'], 'playlist_description': playlistInfo['Description'], 'user_id': playlistInfo['UserId'] }
                    )
        except Exception as e:
            return { 'error': str(e) }, status.HTTP_409_CONFLICT
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    playlistInfo['PlaylistId'] = playlist_id
    location_url = f'http://localhost:5200/api/v1/users/playlists/{PlaylistId}'
    return playlistInfo, status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url}

# deletes playlist from playlist table and deletes all \
    # playlist tracks from table PlaylistTrack
def delete_playlist(playlist):

    playlist['PlaylistId'] = playlist['id']
    try:
        session.execute("""
            DELETE
                FROM tpd
                where playlist_id = %(playlist_id)s""",
                { 'playlist_id': playlist['PlaylistId'] }
            )

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT
    if playlist:
        return {"info": "Successfully deleted"}, status.HTTP_200_OK
    else:
        raise exceptions.NotFound()
