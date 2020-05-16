-- :name add_track_to_playlist :affected
INSERT INTO PlaylistTrack(TrackId, PlaylistId)
VALUES(:TrackId, :PlaylistId)