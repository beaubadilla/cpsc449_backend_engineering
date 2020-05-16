-- :name delete_track_by_id :affected
delete From Track
WHERE TrackId = :TrackId;