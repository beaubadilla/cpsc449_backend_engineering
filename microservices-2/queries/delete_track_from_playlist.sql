-- :name delete_track_from_playlist :affected
delete From PlaylistTrack
WHERE PlaylistId = :PlaylistId AND TrackId = :TrackId;