# Execute 'foreman start -m users=3,descriptions=3,playlist=3,track=3'
# Populate with users
curl -i -X POST \
--url http://localhost:8000/api/v1/users \
--data 'username=mtndew' \
--data 'password=ilovemtndew' \
--data 'display_name=iammtndew' \
--data 'email=mtndewislife@email.com'

curl -i -X POST \
--url http://localhost:8000/api/v1/users \
--data 'username=water' \
--data 'password=ilovewater' \
--data 'display_name=hydrohomie' \
--data 'email=waterislife@email.com'

curl -i -X POST \
--url http://localhost:8000/api/v1/users \
--data 'username=milktea' \
--data 'password=ilovemilktea' \
--data 'display_name=iammilktea' \
--data 'email=milkteaislife@email.com'

# Populate with tracks
# Note: cannot have any data attributes have a ' character within value
curl -i -X POST \
--url http://localhost:8000/api/v1/tracks \
--data 'TrackName=DDU-DU DDU-DU' \
--data 'Album=SQUARE UP' \
--data 'Artist=BLACKPINK' \
--data 'Length=50' \
--data 'Url=/blackpinksong1.mp3'

curl -i -X POST \
--url http://localhost:8000/api/v1/tracks \
--data 'TrackName=WHISTLE' \
--data 'Album=SQUARE ONE' \
--data 'Artist=BLACKPINK' \
--data 'Length=60' \
--data 'Url=/blackpinksong2.mp3'

curl -i -X POST \
--url http://localhost:8000/api/v1/tracks \
--data 'TrackName=STAY' \
--data 'Album=SQUARE TWO' \
--data 'Artist=BLACKPINK' \
--data 'Length=100' \
--data 'Url=/blackpinksong3.mp3'

# Cannot populate playlists or descriptions since tracks have randomly-generated id
# Populate with playlists
# curl -i -X POST \
# --url http://localhost:8000/api/v1/playlists \
# --header "Content-type: application/json" \
# --data '{"PlaylistName": "Kpop", "UserId": "2", "Description": "Best Kpop Group", "Tracks": [{"TrackId": "9"}, {"TrackId": "10"}, {"TrackId": "11"}]}'
#
# # Populate with descriptions
# curl -i -X POST \
# --url http://localhost:8000/api/v1/users/2/tracks/1/descriptions \
# --data 'description=Sick rap'
