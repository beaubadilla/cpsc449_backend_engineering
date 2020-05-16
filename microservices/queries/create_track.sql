-- :name create_track :insert
INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art)
VALUES(:TrackName, :Album, :Artist, :Length, :Url, :Art)