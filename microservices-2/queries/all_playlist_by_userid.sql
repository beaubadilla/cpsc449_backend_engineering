-- :name all_playlist_by_userid :many
SELECT Playlist.PlaylistName, User.Username, Playlist.PlaylistDescription, PlaylistTrack.TrackId
FROM Playlist
JOIN PlaylistTrack ON Playlist.PlaylistId = PlaylistTrack.PlaylistId INNER JOIN User ON Playlist.UserId = User.UserId
WHERE Playlist.UserId = :UserId
