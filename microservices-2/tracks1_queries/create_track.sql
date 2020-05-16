-- :name create_track :insert
INSERT INTO Track(TrackID, TrackName, Album, Artist, Length, Url, Art)
VALUES(:TrackID, :TrackName, :Album, :Artist, :Length, :Url, :Art)