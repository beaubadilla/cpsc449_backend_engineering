#!/bin/bash

#5000 is users
#5100 is descriptions
#5200 is playlist
#5300 is tracks

#Add users
curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"username": "musicluvr123", "password": "bigtreble444", "display_name": "Music Luvr", "email": "musicluvr123@gmail.com", "User_homepage_url": "musiclover.com"}' \
	http://localhost:5000/api/v1/users

curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"username": "rockstar73", "password": "rockstarpassword", "display_name": "Rockstar", "email": "bigrocker73@gmail.com", "User_homepage_url": "rockstar.com"}' \
	http://localhost:5000/api/v1/users

#Add tracks
curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"TrackName": "Imagine", "Album": "Instant Karma: The Amnesty International Campaign to Save Darfur", "Artist": "Avril Lavigne", "Length": "192329", "Url": "file://localhost/F:/Music/iTunes/iTunes%20Music/Compilations/Instant%20Karma_%20The%20Amnesty%20International/10%20Imagine.m4p"}' \
	http://localhost:5300/api/v1/tracks

curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"TrackName": "Oh, My Love", "Album": "Instant Karma: The Amnesty International Campaign to Save Darfur", "Artist": "Jackson Browne", "Length": "159473", "Url": "file://localhost/F:/Music/iTunes/iTunes%20Music/Compilations/Instant%20Karma_%20The%20Amnesty%20International/09%20Oh,%20My%20Love.m4p"}' \
	http://localhost:5300/api/v1/tracks

curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"TrackName": "Jump Around", "Album": "House of Pain", "Artist": "House Of Pain", "Length": "217835", "Url": "file://localhost/F:/Music/iTunes/iTunes%20Music/House%20Of%20Pain/House%20of%20Pain/02%20Jump%20Around.mp3"}' \
	http://localhost:5300/api/v1/tracks

#Add playlists
curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"PlaylistName": "My Cool Playlist", "UserId": "1", "Description": "my playlist", "Tracks": [{"TrackId": 2}, {"TrackId": 1}, {"TrackId": 3}]}' \
	http://127.0.0.1:5200/api/v1/playlists

curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"PlaylistName": "HOT TRACKS", "UserId": "2", "Description": "v hot", "Tracks": [{"TrackId": 2}, {"TrackId": 3}]}' \
	http://127.0.0.1:5200/api/v1/playlists

#Add track descriptions
curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"description": "Chill lo fi beats yo"}' \
	http://127.0.0.1:5100/api/v1/users/1/tracks/1/descriptions

curl \
	--header "Content-type: application/json" \
	--request POST \
	--data '{"description": "This song slaps."}' \
	http://127.0.0.1:5100/api/v1/users/2/tracks/3/descriptions
