-- :name create_playlist :insert
INSERT INTO Playlist(PlaylistName, UserId, PlaylistDescription)
VALUES(:PlaylistName, :UserId, :Description)