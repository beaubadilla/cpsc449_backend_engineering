from cassandra.cluster import cluster

# Assume Prof. creates keyspace with
# CREATE KEYSPACE mykeyspace WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 3 }
cluster = Cluster(['172.17.0.2'])
session = cluster.connect()

session.execute("""
  CREATE KEYSPACE IF NOT EXISTS myKS WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 3 }
""")
session.execute('USE myKS')

session.execute("""
  CREATE TABLE users (
    user_id UUID,
    username TEXT,
    password TEXT,
    display_name TEXT,
    email TEXT,
    homepage_url TEXT,
    PRIMARY KEY((user_id))
  );
""")

# tpd = tracks, playlists, descriptions
session.execute("""
  CREATE TABLE tpd (
    id UUID,
    track_name TEXT,
    album TEXT,
    artist TEXT,
    length INTEGER,
    url TEXT,
    art TEXT,
    user_ids set<UUID>,
    playlist_id set<UUID>,
    PRIMARY KEY((id))
  );
""")

session.execute("""
  CREATE TABLE playlistID (
    playlist_id UUID,
    name TEXT,
    description TEXT,
    PRIMARY KEY((playlist_id))
  );
""")

# Tracks
## Create
session.execute("""
  INSERT INTO tpd (id, track_name, album, artist, length, url, art)
    VALUES (%(id)s, %(track_name)s, %(album)s, %(artist)s, %(length)s, %(url)s, %(art)s);""",
  { 'id': uuid(), 'track_name': track_name, 'album': album, 'artist': artist, 'length': length, 'url': url, 'art': art }
)
## Retrieve
session.execute("""
  SELECT track_name, album, artist, length, url, art
    FROM tpd
    WHERE id = %(id)s;""",
  { 'id': id }
)
## Edit
session.execute("""
  UPDATE tpd
    SET %(track_name)s, %(album)s, %(artist)s, %(length)s, %(url)s, %(art)s
    WHERE id = %(id)s;""",
  { 'track_name': track_name, 'album': album, 'artist': artist, 'length': length, 'url': url, 'art': art, 'id': id }
)
## Delete
session.execute("""
  DELETE FROM tpd
    WHERE id = %(id)s;""",
  { 'id': id }
)
# Playlists
## Retrieve
session.execute("""
  
""")
## Delete
session.execute("""
  
""")
## List all
session.execute("""
  
""")
## List by particular user
session.execute("""
  
""")
# Users
## Create
session.execute("""
  
""")
## Retrieve (don't include password)
session.execute("""
  
""")
## Delete
session.execute("""
  
""")
## Change user's password
session.execute("""
  
""")
## Authenticate
session.execute("""
  
""")
# Descriptions
## Create
session.execute("""
  
""")
## Retrieve
session.execute("""
  
""")