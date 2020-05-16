-- :name update_track_artist :affected
update Track set Artist = :Artist
where TrackId = :TrackId;