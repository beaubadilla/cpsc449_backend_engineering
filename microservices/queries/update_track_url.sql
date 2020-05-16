-- :name update_track_url :affected
update Track set Url = :Url
where TrackId = :TrackId;