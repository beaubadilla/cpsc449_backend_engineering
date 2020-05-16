-- :name all_playlist_by_userid :many
SELECT Playlist.PlaylistName, Track.Url, User.Username, Playlist.PlaylistDescription
FROM Playlist
JOIN PlaylistTrack ON Playlist.PlaylistId = PlaylistTrack.PlaylistId INNER JOIN Track ON PlaylistTrack.TrackId = Track.TrackId INNER JOIN User ON Playlist.UserId = User.UserId
WHERE Playlist.UserId = :UserId