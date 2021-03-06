# cpsc449_microservices_2

## Steps to run: 
```sh
$ python3 -m pip install passlib
$ pip install python-dotenv
$ pip install pugsql
$ pip install bcrypt
$ pip install Flask-API
```
```sh
$ chmod +x kong_configuration.sh
$ ./kong_configuration.sh
```
```sh
$ flask init
```
```sh
$ foreman start -m xspf=1,users=3,descriptions=3,track=3,playlist=3
```
```sh
$ chmod +x population.sh
```
```sh
$ ./RESTpopulation.sh
```


## examples: </br>

# PLAYLIST IN XPSF
## GET playlist XML
### Request
GET http://localhost:8000/api/v1/makeplaylist/<int:id>
### Response Body 
{playlistTitle}.xpsf

# USER
## Create User
### Request
POST http://localhost:8000/api/v1/users
### Parameters
```python
{
  "username": string,
  "password": string,
  "display_name": string,
  "email": string,
  "homepage_url": string # OPTIONAL
 ```
### Response Body
```python
{
  "username": string,
  "display_name": string,
  "email": string,
  "homepage_url": string # 'None' if not provided in request
}
 ```
## Retrieve User Profile
### Request
GET http://localhost:8000/api/v1/users/<int:id>
### Response Body
```python
{
  "Username": string,
  "Password": string,
  "Display_name": string,
  "Email": string,
  "Homepage_url": string # 'None' if not provided in request
}
```
## Delete User Profile
### Request
DELETE http://localhost:8000/api/v1/users/<int:id>
### Response Body
```python
{
  "success": "True"
}
```
## Change User's Password
### Request
PATCH http://localhost:8000/api/v1/users/passwords
### Parameters
```python
{
  "username": string,
  "current_password": string,
  "new_password": string
}
```
### Response Body
```python
{
  "success": "True"
}
```
## Authenticate User
### Request
GET http://localhost:8000/api/v1/users/authentications
### Parameters
```python
{
  "username": string,
  "password": string
}
```
### Response Body
```python
{
  "success": "True"
}
```
# Descriptions
## Create Description
### Request
POST http://localhost:8000/api/v1/users/<int:UserId>/tracks/<GUID:TrackID>/descriptions
### Parameters
```python
{
  "description": string
}
```
### Response Body
```python
{
  "description": string
}
```
## Retrieve Description
### Request
GET http://localhost:8000/api/v1/users/<int:UserId>/tracks/<GUID:TrackId>/descriptions
### Response Body
```python
{
  "TrackId": GUID,
  "UserId": int,
  "Comment": string
}
```
# Tracks

### - Create a new track:

POST http://localhost:8000/api/v1/tracks 
### Parameters
```python
{
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```
### Response Body
```python
{
    "TrackId": GUID,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```
### - Retrieve a track:

GET http://localhost:8000/api/v1/tracks?id={TrackGUID}
### Response Body
```python
{
    "TrackId": GUID,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```

### - Edit a track:

PUT http://localhost:8000/api/v1/tracks
### Parameters
```python
{
    "TrackId": GUID,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```
### Response Body
```python
{
    "TrackId": GUID,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```

### - Delete a track:

DELETE http://localhost:8000/api/v1/tracks?id={TrackGUID}
### Response Body
```python
{ "info": "Successfully deleted."}
```
</br>

# Playlists

### - Create a new playlist:

POST http://localhost:8000/api/v1/playlists 

### Parameters
```python
{
    "PlaylistName": string,
    "UserId": int,
    "Description": string,
    "Tracks": [{"TrackId": GUID}, {"TrackId": GUID}, {"TrackId": GUID}]
}
```
### Response Body
```python
{
    "PlaylistId": int,
    "PlaylistName": string,
    "UserId": int,
    "Description": string,
    "Tracks": [{"TrackId": GUID}, {"TrackId": GUID}, {"TrackId": GUID}]
}
```

### - Retrieve a playlist:

GET http://localhost:8000/api/v1/users/playlists/{PlaylistId}
### Response Body
```python
[
   {
      "PlaylistName": string,
      "Username": string,
      "Description": string,
      "TrackUrl": string
    }...
]
```
### - Delete a playlist:

DELETE http://localhost:8000/api/v1/users/playlists/{PlaylistId}
### Response Body
```python
{ "info": "Successfully deleted."}
```

### - List all playlists:

GET http://localhost:8000/api/v1/playlists HTTP/1.1

### Response Body
```python
[
   {
      "PlaylistName": string,
      "Username": string,
      "Description": string,
      "TrackUrl": string
    }...
]
```

### - Lists playlists created by a particular user:

GET http://localhost:8000/api/v1/playlists?uid={UserId}
```python
[
   {
      "PlaylistName": string,
      "PlaylistName": string,
      "Username": string,
      "Description": string,
      "TrackUrl": string
    }...
]
```



</br>

# Extras:


### get all tracks

GET http://localhost:8000/api/v1/tracks HTTP/1.1

### another way to get a playlist

GET http://localhost:8000/api/v1/playlists?id=1 HTTP/1.1

### add a track into a playlist

POST http://127.0.0.1:8000/api/v1/users/1/playlists/1/tracks HTTP/1.1
### Parameters
```python
{
    "TrackId": GUID
}
```

### remove a track from a playlist

DELETE http://localhost:8000/api/v1/users/1/playlists/1/tracks/1 HTTP/1.1

###
