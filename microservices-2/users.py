from flask import request
from flask_api import status, exceptions
from passlib.hash import bcrypt
import flask_api
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])

@app.route('/api/v1/users', methods=['POST'])
def create_user():
  user = request.data
  required_fields = ['username', 'password', 'display_name', 'email'] # password is non-hashed at this point

  if not all([field in user for field in required_fields]):
    raise exceptions.ParseError()

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

    user['user_id'] = queries.create_user(Username=username,Password=hashed_password, Display_name=display_name, Email=email, Homepage_url=homepage_url)

    del user['password'] # Do not want response to include hashed password
  except Exception as e:
    return { 'error': str(e) }, status.HTTP_409_CONFLICT, { "Content-Type": "application/json" }

  user_id = user['user_id']
  location_url = f'http://localhost:8000/api/v1/users/{user_id}'
  return user, status.HTTP_201_CREATED, { "Content-Type": "application/json", "Location": location_url }

@app.route('/api/v1/users/<int:UserId>', methods=['GET','DELETE'])
def user(UserId):
  if request.method == 'GET':
    return retrieve_user_profile(UserId)
  elif request.method == 'DELETE':
    return delete_user_profile(UserId)

def retrieve_user_profile(UserId):
  user_profile = queries.user_by_id(UserId=UserId)

  if user_profile:
    return user_profile, status.HTTP_200_OK, { "Content-Type": "application/json" }
  else:
    raise exceptions.NotFound()

def delete_user_profile(UserId):
  try:
    queries.delete_user(UserId=UserId)
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
  db_password = queries.password_by_username(Username=username)['Password']

  # Authenticate user to only allow user to change their password
  if bcrypt.verify(current_password, db_password):
    hashed_password = bcrypt.using(rounds=16).hash(new_password)
    queries.update_password(Username=username, Password=hashed_password)
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
  db_password = queries.password_by_username(Username=username)['Password']

  if bcrypt.verify(password, db_password): # salt is encoded in hashed password
    return { 'success': 'True' }, status.HTTP_200_OK, { "Content-Type": "application/json" }
  else:
    return { 'success': 'False' }, status.HTTP_400_BAD_REQUEST,{ "Content-Type": "application/json" }
