-- :name update_track_length :affected
update Track set Length = :Length
where TrackId = :TrackId;