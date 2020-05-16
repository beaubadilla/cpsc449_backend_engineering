-- :name update_track_album :affected
update Track set Album = :Album
where TrackId = :TrackId;