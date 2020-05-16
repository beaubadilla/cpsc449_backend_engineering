-- :name all_playlist_track_url :many
SELECT Playlist.PlaylistName, User.Username, Playlist.PlaylistDescription, PlaylistTrack.TrackId
FROM Playlist
JOIN PlaylistTrack ON Playlist.PlaylistId = PlaylistTrack.PlaylistId INNER JOIN User ON Playlist.UserId = User.UserId
