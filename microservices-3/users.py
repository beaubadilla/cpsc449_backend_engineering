from flask import request
from flask_api import status, exceptions
from passlib.hash import bcrypt
import flask_api
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

@app.route('/api/v1/users', methods=['POST'])
def create_user():
  user = request.data
  required_fields = ['username', 'password', 'display_name', 'email'] # password is non-hashed at this point

  if not all([field in user for field in required_fields]):
    raise exceptions.ParseError()

  user_id = uuid.uuid4()
  username = user['username']
  password = user['password']
  display_name = user['display_name']
  email = user['email']

  try:
    hashed_password = bcrypt.using(rounds=16).hash(password) # 16 rounds should take ~4 seconds to compute, salts defaulty
    if 'homepage_url' in user:
      homepage_url = user['homepage_url']
    else:
      homepage_url = None

    session.execute("""
      INSERT INTO users (user_id, username, password, display_name, email, homepage_url)
        VALUES (%(user_id)s, %(username)s, %(password)s, %(display_name)s, %(email)s, %(homepage_url)s);""",
      { 'user_id': user_id, 'username': username, 'password': hashed_password, 'display_name': display_name, 'email': email, 'homepage_url': homepage_url }
    )

    del user['password'] # Do not want response to include hashed password
  except Exception as e:
    return { 'error': str(e) }, status.HTTP_409_CONFLICT, { "Content-Type": "application/json" }

  user['user_id'] = user_id

  location_url = f'http://localhost:8000/api/v1/users/{user_id}'
  return user, status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url }

@app.route('/api/v1/users/<int:UserId>', methods=['GET','DELETE'])
def user(UserId):
  if request.method == 'GET':
    return retrieve_user_profile(UserId)
  elif request.method == 'DELETE':
    return delete_user_profile(UserId)

def retrieve_user_profile(UserId):
  # TODO: select might return collection, even if its just one record
  user_profile = session.execute("""
    SELECT user_id, username, display_name, email, homepage_url
      FROM users
      WHERE user_id = %(user_id)s;""",
      { 'user_id': UserId }
  )

  if user_profile:
    return user_profile, status.HTTP_200_OK, { "Content-Type": "application/json" }
  else:
    raise exceptions.NotFound()

def delete_user_profile(UserId):
  try:
    session.execute("""
      DELETE FROM users
        WHERE user_id = %(user_id)s;""",
        { 'user_id': UserId }
    )
  except Exception as e:
    return { 'error': str(e) }, status.HTTP_409_CONFLICT, { "Content-Type": "application/json" }

  return { 'success': True }, status.HTTP_204_NO_CONTENT, { "Content-Type": "application/json" }

@app.route('/api/v1/users/passwords', methods=['PATCH'])
def change_user_password():
  request_data = request.data
  required_fields = [ 'username', 'current_password', 'new_password']

  if not all([field in request_data for field in required_fields]):
    raise exceptions.ParseError()

  username = request_data['username']
  current_password = request_data['current_password']
  new_password = request_data['new_password']
  # TODO: select might return collection even if its one record
  db_password = session.execute("""
    SELECT password
      FROM users
      WHERE username = %(username)s;""",
      { 'username': username }
  )

  # Authenticate user to only allow user to change their password
  if bcrypt.verify(current_password, db_password):
    hashed_password = bcrypt.using(rounds=16).hash(new_password)
    session.execute("""
      UPDATE users
        SET %(password)s
        WHERE user_id = %(user_id)s;""",
        { 'password': hashed_password }
    )
  else:
    return { 'success': 'False' }, status.HTTP_400_BAD_REQUEST, { "Content-Type": "application/json" }

  return { 'success': 'True' }, status.HTTP_204_NO_CONTENT, { "Content-Type": "application/json" }

@app.route('/api/v1/users/authentications', methods=['GET'])
def authenticate_user():
  request_data = request.data
  required_fields = ['username', 'password']

  if not all([field in request_data for field in required_fields]):
    raise exceptions.ParseError()

  username = request_data['username']
  password = request_data['password']
  # TODO: might return collection even if its just one record
  db_password = session.execute("""
    SELECT password
      FROM users
      WHERE username = %(username)s;""",
      { 'username': username }
  )

  if bcrypt.verify(password, db_password): # salt is encoded in hashed password
    return { 'success': 'True' }, status.HTTP_200_OK, { "Content-Type": "application/json" }
  else:
    return { 'success': 'False' }, status.HTTP_400_BAD_REQUEST,{ "Content-Type": "application/json" }
