from flask import request
import flask_api
from flask_api import exceptions, status
from cassandra.cluster import Cluster
from flask_cassandra import CassandraCluster # pip3 install flask-cassandra
from flask import Flask

app = Flask(__name__)
cassandra = CassandraCluster()

app.config['CASSANDRA_NODES'] = ['172.17.02']

session = cassandra.connect()
session.set_keyspace('data')

@app.route('/api/v1/users/<int:UserId>/tracks/<int:TrackId>/descriptions',
  methods=['POST', 'GET'])
def create_user_track_description(UserId, TrackId):
  if request.method == 'GET':
    try:
        description = session.execute("""
          SELECT comment
            FROM tpd
            WHERE user_id = %(user_id)s AND track_id = %(track_id)s;""",
            { 'user_id': UserId, 'track_id': TrackId }
        )
    except Exception as e:
        return e
    if description:
      return description, status.HTTP_200_OK, { "Content-Type": "application/json"}
    else:
      raise exceptions.NotFound()

  if request.method == 'POST':
    description = request.data

    if 'description' not in description:
      raise exceptions.ParseError()

    comment = description['description']

    try:
      session.execute("""
        UPDATE tpd
          SET %(comment)s
          WHERE user_id = %(user_id)s AND track_id = %(track_id)s;""",
          { 'user_id': UserId, 'track_id': TrackId }
      )
    except Exception as e:
      return { 'error': str(e) }, status.HTTP_409_CONFLICT, { "Content-Type": "application/json" }

    location_url = f'http://localhost:8000/api/v1/users/{UserId}/tracks/{TrackId}/descriptions'
    return description , status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url }
