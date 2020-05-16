-- :name delist_track_from_playlists :affected
DELETE FROM PlaylistTrack
WHERE TrackId = :TrackId;