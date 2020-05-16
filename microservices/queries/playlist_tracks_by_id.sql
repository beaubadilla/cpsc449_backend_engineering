-- :name playlist_tracks_by_id :many
SELECT TrackId FROM PlaylistTrack WHERE PlaylistId = :PlaylistId