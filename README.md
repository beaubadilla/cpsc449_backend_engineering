<br />
<p align="center">
  <h1 align="center">Microservice Architecture</h1>

  <p align="center">
    Practice developing application programming interfaces(APIs) under a microservice architecture.<br/>
    Project for <a href="http://www.fullerton.edu/">Cal State Fullerton</a>'s Back-End Engineer course(CPSC 449).
    <br />
    <a href="https://github.com/beaubadilla/cpsc449_backend_engineering/issues">Report Bug or Request Feature</a>
  </p>
</p>

## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
  * [Code Snippets](#code-snippets)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [License](#license)
* [Contact](#contact)

## About the Project

This project simulates the back-end for a music playlist creation app(users, tracks, playlists, playlists' descriptions). It was split up into three parts for the duration of the semester. Every student grouped up with two other students because our professor wanted to imitate a realistic development team. In addition, each group member had a designated role(Developer, Developer, Operations) in which we would swap roles for each part of the project. It aimed to have us implement everything we learned about **scalability: representation state transfer(REST) APIs,  database sharding and replication, caching, stateful v.s. stateless, SQL vs NoSQL**.

* **microservices**: Assigned to the <ins>Developer</ins> role, my responsibility was implementing REST APIs for users and playlist descriptions.
* **microservices-2**: Assigned to the <ins>Operations</ins> role, my responsbility was configuring Kong Gateway and setting up the procfile.
* **microservices-3**: Assigned to the <ins>Developer</ins> role, my responsibility was creating a wide-column database and converting all our SQL queries into CQL queries.


### Built With
Languages: Python 3.x, SQL/CQL
* microservices - [Flask](https://flask.palletsprojects.com/en/1.1.x/), [PugSQL](https://pugsql.org/), [SQLite](https://docs.python.org/3/library/sqlite3.html)
* microservices-2 - [Kong Gateway](https://konghq.com/kong/)
* microservices-3 - [ScyllaDB](https://www.scylladb.com/)

### Code Snippets
microservices: API to authenticate a user
```python
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
```

microservices-2: curl commands configuring tracks' route
```sh
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
```

microservices-3: CQL statement to add a track
```python
session.execute("""
  INSERT INTO tpd (id, track_name, album, artist, length, url, art)
    VALUES (%(id)s, %(track_name)s, %(album)s, %(artist)s, %(length)s, %(url)s, %(art)s);""",
  { 'id': uuid(), 'track_name': track_name, 'album': album, 'artist': artist, 'length': length, 'url': url, 'art': art }
)
```
## Getting Started

### Prerequisites

Download [Python 3.x](https://www.python.org/downloads/)

### Installation

1. Clone the repo
```sh
git clone https://github.com/beaubadilla/cpsc449_backend_engineering.git
```
2. Follow the README.md for each individual part.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Beau Jayme De Guzman Badilla - beau.badilla@gmail.com - [LinkedIn](https://www.linkedin.com/in/beau-jayme-badilla/)
