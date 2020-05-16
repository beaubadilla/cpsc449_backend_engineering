-- :name update_track_art :affected
update Track set Art = :Art
where TrackId = :TrackId;