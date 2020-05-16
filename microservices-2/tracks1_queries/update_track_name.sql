-- :name update_track_name :affected
update Track set TrackName = :TrackName
where TrackId = :TrackId;