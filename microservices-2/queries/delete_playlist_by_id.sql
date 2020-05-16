-- :name delete_playlist_by_id :affected
delete From Playlist
WHERE PlaylistId = :PlaylistId;