from flask import request
import flask_api
from flask_api import exceptions, status
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.route('/api/v1/users/<int:UserId>/tracks/<int:TrackId>/descriptions',
  methods=['POST', 'GET'])
def create_user_track_description(UserId, TrackId):
  if request.method == 'GET':
    try:
        description = queries.description_by_userid_trackid(UserId=UserId, TrackId=TrackId)
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
      queries.create_description(UserId=UserId, TrackId=TrackId, Comment=comment)
    except Exception as e:
      return { 'error': str(e) }, status.HTTP_409_CONFLICT, { "Content-Type": "application/json" }

    location_url = f'http://localhost:8000/api/v1/users/{UserId}/tracks/{TrackId}/descriptions'
    return description , status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url }
