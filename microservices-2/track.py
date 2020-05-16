import sys
import flask_api
from flask import request
from flask_api import status, exceptions
import pugsql
import uuid
import sqlite3


app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

queries1 = pugsql.module('tracks1_queries/')
queries1.connect(app.config['DATABASE_URL1'])

queries2 = pugsql.module('tracks2_queries/')
queries2.connect(app.config['DATABASE_URL2'])

queries3 = pugsql.module('tracks3_queries/')
queries3.connect(app.config['DATABASE_URL3'])

sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))

@app.cli.command('init')
def init_db():
    with app.app_context():
        db1 = queries1._engine.raw_connection()
        word_file1 = open('tracks1.sql', mode = 'r', encoding='utf-8')
        word_file_read1 = word_file1.read()
        word_file1.close()

        db1.cursor().executescript(word_file_read1)
        db1.commit()

        db2 = queries2._engine.raw_connection()
        word_file2 = open('tracks2.sql', mode = 'r', encoding='utf-8')
        word_file_read2 = word_file2.read()
        word_file2.close()

        db2.cursor().executescript(word_file_read2)
        db2.commit()

        db3 = queries3._engine.raw_connection()
        word_file3 = open('tracks3.sql', mode = 'r', encoding='utf-8')
        word_file_read3 = word_file3.read()
        word_file3.close()

        db3.cursor().executescript(word_file_read3)
        db3.commit()

        db = queries._engine.raw_connection()
        word_file = open('data.sql', mode='r', encoding='utf-8')
        word_file_read = word_file.read()
        word_file.close()

        db.cursor().executescript(word_file_read)
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Available endpoints: </h1>
    <h2>Tracks: </h2>
<ol><li><a href="/api/v1/tracks">Create a track</a><p>{
    "TrackName": "sample",
    "Album": "An Album",
    "Artist": "An Artist",
    "Length": 12345,
    "Url": "file://aplace/this.mp3",
    "Art": "something.jpg"
}</p></li><li><a href="/api/v1/tracks?id=2">Retrieve a track</a></li><li><a href="/api/v1/tracks">Edit a track</a><p>{
    "TrackId": 1,
    "TrackName": "Updated name",
    "Album": "Updated Album",
    "Artist": "Updated Artist",
    "Length": 12345,
    "Url": "file://aplace/this.mp3",
    "Art": "something.jpg"
}</p></li><li><a href="/api/v1/tracks?id=1">Delete a track</a></li></ol>
'''

# all track endpoints will leade here
@app.route('/api/v1/tracks', methods=['POST', 'GET', 'DELETE', 'PUT'])
def tracks():
    if request.method == 'GET':
        return get_track(request.args), status.HTTP_200_OK

    elif request.method == 'POST':
        return create_track(request.data)

    elif request.method == 'DELETE':
        return delete_track(request.args)

    elif request.method == 'PUT':
        return edit_track(request.data)

# allows the creation of a new track to ne inserted into DB.
    # If no Art is given, then we declare it to NULL
def create_track(track):
    track = request.data
    required_fields = ['TrackName', 'Album', 'Artist', 'Length', 'Url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if not 'Art' in track.keys():
            track['Art'] = None

        TrackId = uuid.uuid4() # UUID object
        track['TrackID'] = TrackId
        intTrackId = int(TrackId) # int representation of UUID object
        shard_key = intTrackId % 3

        if shard_key == 0:
                queries1.create_track(**track)
        elif shard_key == 1:
                queries2.create_track(**track)
        elif shard_key == 2:
                queries3.create_track(**track)

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    location_url = f'http://localhost:5300/api/v1/tracks?id={TrackId}'

    return track, status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url}

# edits track given the TrackId. Since this is a PUT,
    # it is expected to pass in the whole object to
    #  replace the current object
        #(Optional): since we are given a whole object with PUT, there
            # is no need to have different files for each column update.
            # Unless we are doing PATCH.
def edit_track(track):
    track = request.data
    required_fields = ['TrackId']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError
    try:
        shard_key = track['TrackId'] % 3
        if shard_key == 0:
            for updates in track:
                if updates == 'TrackName':
                    b = queries1.update_track_name(**track)
                if updates == 'Album':
                    b = queries1.update_track_album(**track)
                if updates == 'Artist':
                    b = queries1.update_track_artist(**track)
                if updates == 'Length':
                    b = queries1.update_track_length(**track)
                if updates == 'Url':
                    b = queries1.update_track_url(**track)
                if updates == 'Art':
                    b = queries1.update_track_art(**track)
            track = queries1.track_by_id(**track)

        elif shard_key == 1:
            for updates in track:
                if updates == 'TrackName':
                    b = queries2.update_track_name(**track)
                if updates == 'Album':
                    b = queries2.update_track_album(**track)
                if updates == 'Artist':
                    b = queries2.update_track_artist(**track)
                if updates == 'Length':
                    b = queries2.update_track_length(**track)
                if updates == 'Url':
                    b = queries1.update_track_url(**track)
                if updates == 'Art':
                    b = queries2.update_track_art(**track)
            track = queries2.track_by_id(**track)

        elif shard_key == 2:
            for updates in track:
                if updates == 'TrackName':
                    b = queries3.update_track_name(**track)
                if updates == 'Album':
                    b = queries3.update_track_album(**track)
                if updates == 'Artist':
                    b = queries3.update_track_artist(**track)
                if updates == 'Length':
                    b = queries3.update_track_length(**track)
                if updates == 'Url':
                    b = queries3.update_track_url(**track)
                if updates == 'Art':
                    b = queries3.update_track_art(**track)
            track = queries3.track_by_id(**track)

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

# deletes a track, from a given 'id'
    # if no 'id' is given then returns '400 BAD REQUEST'
def delete_track(track):
    if 'id' in track:
            track = {
                "TrackId": track['id']
            }
            try:
                shard_key = track['TrackId'] % 3
                if shard_key == 0:
                    queries1.delist_track_from_playlists(**track)
                    track = queries1.delete_track_by_id(**track)

                elif shard_key == 1:
                    queries2.delist_track_from_playlists(**track)
                    track = queries2.delete_track_by_id(**track)

                elif shard_key == 2:
                    queries3.delist_track_from_playlists(**track)
                    track = queries3.delete_track_by_id(**track)
            except Exception as e:
                return { 'error': str(e) }, status.HTTP_409_CONFLICT
            if track:
                return {"info": "Successfully deleted"}, status.HTTP_200_OK
            else:
                raise exceptions.NotFound()
    return {'error': "Did not provide an id for track to be deleted"}, status.HTTP_400_BAD_REQUEST

# Returns all tracks in the DB.
def all_tracks():
    all_tracks1 = queries1.all_tracks()
    all_tracks2 = queries2.all_tracks()
    all_tracks3 = queries3.all_tracks()
    all_tracks = all_tracks1 + all_tracks2 + all_tracks3
    return list(all_tracks)

# returns a track given 'id'. If no ID is given then return all tracks.
    # do this to activate flaskAPI, so we can easily POST, PUT...
def get_track(track):
    if 'id' in track:
        track = {
            "TrackId": track['id']
        }
        myUUID = str(track['TrackId'])
        myUUID = uuid.UUID(myUUID)
        track['TrackId'] = myUUID
        shard_key = myUUID.int % 3
        try:
            if shard_key == 0:
            	track = queries1.track_by_id(**track)
            elif shard_key == 1:
            	track = queries2.track_by_id(**track)
            elif shard_key == 2:
            	track = queries3.track_by_id(**track)

        except Exception as e:
            return e
    else:
        return all_tracks()
    track['TrackId'] = str(uuid.UUID(bytes=track['TrackId']))
    if track:
        return track
    else:
        raise exceptions.NotFound()
