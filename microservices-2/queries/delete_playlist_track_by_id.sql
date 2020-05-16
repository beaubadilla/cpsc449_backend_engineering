-- :name delete_playlist_track_by_id :affected
delete From PlaylistTrack
WHERE PlaylistId = :PlaylistId;