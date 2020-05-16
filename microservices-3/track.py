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

# session = cassandra.connect()

@app.cli.command('init')
def init_db():
    with app.app_context():
        cluster = Cluster(['172.17.02'])
        session = cassandra.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS data WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 3 };
        """)
        session.set_keyspace('data')

        session.execute("""DROP TABLE IF EXISTS users;""")
        session.execute("""DROP TABLE IF EXISTS tpd;""")

        session.execute('CREATE TABLE IF NOT EXISTS users (user_id UUID, username TEXT, password TEXT, display_name TEXT, email TEXT, homepage_url TEXT, PRIMARY KEY(user_id));')
        session.execute('CREATE TABLE IF NOT EXISTS tpd (track_id UUID, track_name TEXT, album TEXT, artist TEXT, length INT, url TEXT, art TEXT, user_id UUID, playlist_id UUID, playlist_name TEXT, playlist_description TEXT, comment TEXT, PRIMARY KEY(track_id));')

        session.execute("""
            CREATE INDEX IF NOT EXISTS on tpd (playlist_id);
        """)
        session.execute("""
            CREATE INDEX IF NOT EXISTS on tpd (user_id);
        """)


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
    session.set_keyspace('data')

    track = request.data
    required_fields = ['TrackName', 'Album', 'Artist', 'Length', 'Url']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError()
    try:
        if not 'Art' in track.keys():
            track['Art'] = None

        TrackId = uuid.uuid4() # UUID object
        track['TrackID'] = TrackId
        # intTrackId = int(TrackId) # int representation of UUID object

        session.execute("""
            INSERT INTO tpd (track_id, track_name, album, artist, length, url, art)
                VALUES (%(track_idid)s, %(track_name)s, %(album)s, %(artist)s, %(length)s, %(url)s, %(art)s);""",
                { 'track_id': TrackId, 'track_name': track['TrackName'], 'album': track['Album'], 'artist': track['Artist'], 'length': track['Length'], 'url': track['Url'], 'art': track['Art'] }
        )

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
    session.set_keyspace('data')

    track = request.data
    required_fields = ['TrackId']

    if not all([field in track for field in required_fields]):
        raise exceptions.ParseError
    try:
        for updates in track:
            if updates == 'TrackName':
                session.execute("""
                    UPDATE tpd
                        SET %(track_name)s
                        WHERE id = %(track_id)s;""",
                        { 'track_name': track['TrackName'], 'track_id': track['TrackId'] }
                )
            if updates == 'Album':
                session.execute("""
                    UPDATE tpd
                        SET %(album)s
                        WHERE id = %(track_id)s;""",
                        { 'album': track['Album'], 'track_id': track['TrackId'] }
                )
            if updates == 'Artist':
                session.execute("""
                    UPDATE tpd
                        SET %(artist)s
                        WHERE id = %(track_id)s;""",
                        { 'artist': track['Artist'], 'track_id': track['TrackId'] }
                )
            if updates == 'Length':
                session.execute("""
                    UPDATE tpd
                        SET %(length)s
                        WHERE id = %(track_id)s;""",
                        { 'length': track['Length'], 'track_id': track['TrackId'] }
                )
            if updates == 'Url':
                session.execute("""
                    UPDATE tpd
                        SET %(url)s
                        WHERE id = %(track_id)s;""",
                        { 'url': track['Url'], 'track_id': track['TrackId'] }
                )
            if updates == 'Art':
                session.execute("""
                    UPDATE tpd
                        SET %(art)s
                        WHERE id = %(track_id)s;""",
                        { 'art': track['Art'], 'track_id': track['TrackId'] }
                )

        # TODO: select might return a list even if its one
        track = session.execute("""
            SELECT track_name, album, artist, length, url, art
                FROM tpd
                WHERE track_id = %(track_id)s;""",
                { 'track_id': track['TrackId'] }
        )

    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return track, status.HTTP_201_CREATED

# deletes a track, from a given 'id'
    # if no 'id' is given then returns '400 BAD REQUEST'
def delete_track(track):
    session.set_keyspace('data')

    if 'id' in track:
            track = {
                "TrackId": track['id']
            }
            try:
                session.execute("""
                    DELETE FROM tpd
                        WHERE id = %(track_id)s;""",
                        { 'track_id': track['TrackId'] }
                )
            except Exception as e:
                return { 'error': str(e) }, status.HTTP_409_CONFLICT
            if track:
                return {"info": "Successfully deleted"}, status.HTTP_200_OK
            else:
                raise exceptions.NotFound()
    return {'error': "Did not provide an id for track to be deleted"}, status.HTTP_400_BAD_REQUEST

# returns a track given 'id'. If no ID is given then return all tracks.
    # do this to activate flaskAPI, so we can easily POST, PUT...
def get_track(track):
    session.set_keyspace('data')

    if 'id' in track:
        track = {
            "TrackId": track['id']
        }
        myUUID = str(track['TrackId'])
        myUUID = uuid.UUID(myUUID)
        track['TrackId'] = myUUID
        try:
            session.execute("""
                SELECT track_name, album, artist, length, url, art
                    FROM tpd
                    WHERE track_id = %(track_id)s;""",
                    { 'track_id': track['TrackId'] }
                )

        except Exception as e:
            return e

    track['TrackId'] = str(uuid.UUID(bytes=track['TrackId']))
    if track:
        return track
    else:
        raise exceptions.NotFound()
