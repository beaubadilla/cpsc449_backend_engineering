# cpsc449_microservices

## Steps to run: 
```sh
$ python3 -m pip install passlib
$ pip install python-dotenv
$ pip install pugsql
$ pip install bcrypt
$ pip install Flask-API
```
```sh
$ flask init
```
```sh
$ foreman start
```
```sh
$ chmod +x RESTpopulation.sh
```
```sh
$ ./RESTpopulation.sh
```


## examples: </br>

# USER
## Create User
### Request
POST http://localhost:5000/api/v1/users
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
GET http://localhost:5000/api/v1/users/<int:id>
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
DELETE http://localhost:5000/api/v1/users/<int:id>
### Response Body
```python
{
  "success": "True"
}
```
## Change User's Password
### Request
PATCH http://localhost:5000/api/v1/users/passwords
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
GET http://localhost:5000/api/v1/users/authentications
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
POST http://localhost:5100/api/v1/users/<int:id>/tracks/<int:id>/descriptions
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
GET http://localhost:5100/api/v1/users/<int:id>/tracks/<int:id>/descriptions
### Response Body
```python
{
  "TrackId": int,
  "UserId": int,
  "Comment": string
}
```
# Tracks

### - Create a new track:

POST http://localhost:5300/api/v1/tracks 
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
    "TrackId": int,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```
### - Retrieve a track:

GET http://localhost:5300/api/v1/tracks?id={TrackId}
### Response Body
```python
{
    "TrackId": int,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```

### - Edit a track:

PUT http://localhost:5300/api/v1/tracks
### Parameters
```python
{
    "TrackId": int,
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
    "TrackId": int,
    "TrackName": string,
    "Album": string,
    "Artist": string,
    "Length": int,
    "Url": string,
    "Art": string
}
```

### - Delete a track:

DELETE http://localhost:5300/api/v1/tracks?id={TrackId}
### Response Body
```python
{ "info": "Successfully deleted."}
```
</br>
# Playlists

### - Create a new playlist:

POST http://localhost:5200/api/v1/playlists 

### Parameters
```python
{
    "PlaylistName": string,
    "UserId": int,
    "Description": string,
    "Tracks": [{"TrackId": int}, {"TrackId": int}, {"TrackId": int}]
}
```
### Response Body
```python
{
    "PlaylistId": int,
    "PlaylistName": string,
    "UserId": int,
    "Description": string,
    "Tracks": [{"TrackId": int}, {"TrackId": int}, {"TrackId": int}]
}
```

### - Retrieve a playlist:

GET http://localhost:5200/api/v1/users/playlists/{PlaylistId}
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

DELETE http://localhost:5200/api/v1/users/playlists/{PlaylistId}
### Response Body
```python
{ "info": "Successfully deleted."}
```

### - List all playlists:

GET http://localhost:5200/api/v1/playlists HTTP/1.1

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

GET http://localhost:5200/api/v1/playlists?uid={UserId}
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

GET http://localhost:5300/api/v1/tracks HTTP/1.1

### another way to get a playlist

GET http://localhost:5200/api/v1/playlists?id=1 HTTP/1.1

### add a track into a playlist

POST http://127.0.0.1:5200/api/v1/users/1/playlists/1/tracks HTTP/1.1
### Parameters
```python
{
    "TrackId": int
}
```

### remove a track from a playlist

DELETE http://localhost:5200/api/v1/users/1/playlists/1/tracks/1 HTTP/1.1

###
