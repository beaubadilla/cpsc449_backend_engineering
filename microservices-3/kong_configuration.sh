# Tracks Microservice
curl -i -X POST \
--url http://localhost:8001/upstreams \
--data 'name=api.v1.tracks.service' # name must equal host of respective Service Object

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.tracks.service/targets \
--data 'target=127.0.0.1:5300'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.tracks.service/targets \
--data 'target=127.0.0.1:5301'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.tracks.service/targets \
--data 'target=127.0.0.1:5302'

curl -i -X POST \
--url http://localhost:8001/services \
--data 'name=tracks-service' \
--data 'host=api.v1.tracks.service' \
--data 'path=/api/v1/tracks'

curl -i -X POST \
--url http://localhost:8001/services/tracks-service/routes \
--data 'name=tracks-route' \
--data 'paths=/api/v1/tracks/' \
--data 'methods[]=GET&methods[]=POST&methods=PUT&methods=DELETE'


# Users Microservice
curl -i -X POST \
--url http://localhost:8001/upstreams \
--data 'name=api.v1.users.service'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.users.service/targets \
--data 'target=127.0.0.1:5000'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.users.service/targets \
--data 'target=127.0.0.1:5001'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.users.service/targets \
--data 'target=127.0.0.1:5002'

curl -i -X POST \
--url http://localhost:8001/services \
--data 'name=users-service' \
--data 'host=api.v1.users.service' \
--data 'path=/api/v1/users'

curl -i -X POST \
--url http://localhost:8001/services/users-service/routes \
--data 'name=users-route' \
--data 'paths=/api/v1/users' \
--data 'methods[]=GET&methods[]=POST&methods[]=DELETE&methods[]=PATCH'


# Descriptions Microservice
curl -i -X POST \
--url http://localhost:8001/upstreams \
--data 'name=api.v1.descriptions.service'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.descriptions.service/targets \
--data 'target=127.0.0.1:5100'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.descriptions.service/targets \
--data 'target=127.0.0.1:5101'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.descriptions.service/targets \
--data 'target=127.0.0.1:5102'

curl -i -X POST \
--url http://localhost:8001/services \
--data 'name=descriptions-service' \
--data 'host=api.v1.descriptions.service' \
--data 'path=/'

curl -i -X POST \
--url http://localhost:8001/services/descriptions-service/routes \
--data 'name=descriptions-route' \
--data-urlencode 'paths=/api/v1/users/\d+/tracks/\d+/descriptions' \
--data 'methods[]=GET&methods[]=POST' \
--data 'strip_path=false'


# Playlists Microservice
curl -i -X POST \
--url http://localhost:8001/upstreams \
--data 'name=api.v1.playlists.service'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.playlists.service/targets \
--data 'target=127.0.0.1:5200'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.playlists.service/targets \
--data 'target=127.0.0.1:5201'

curl -i -X POST \
--url http://localhost:8001/upstreams/api.v1.playlists.service/targets \
--data 'target=127.0.0.1:5202'

curl -i -X POST \
--url http://localhost:8001/services \
--data 'name=playlists-service' \
--data 'host=api.v1.playlists.service' \
--data 'path=/'

curl -i -X POST \
--url http://localhost:8001/services/playlists-service/routes \
--data 'name=playlists-route' \
--data 'paths[]=/api/v1/playlists&paths[]=/api/v1/users/playlists' \
--data 'methods[]=GET&methods[]=POST&methods[]=DELETE' \
--data 'strip_path=false'


# Media
curl -i -X POST \
--url http://localhost:8001/services \
--data 'name=media-service' \
--data 'protocol=http' \
--data 'host=localhost' \
--data 'port=9000' \
--data 'path=/tracks'

curl -i -X POST \
--url http://localhost:8001/services/media-service/routes \
--data 'name=media-route' \
--data 'paths[]=/media' \
--data 'methods[]=GET' \
