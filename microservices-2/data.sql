-- $ sqlite3 music.db < sqlite.sql

BEGIN TRANSACTION;
--DROP TABLE IF EXISTS "Track";
DROP TABLE IF EXISTS "User";
DROP TABLE IF EXISTS "Playlist";
DROP TABLE IF EXISTS "PlaylistTrack";
DROP TABLE IF EXISTS "Description";

--CREATE TABLE "Track" (
 --       "TrackId"       INTEGER NOT NULL,
   --     "TrackName"  NVARCHAR(200) NOT NULL,
     --   "Album" NVARCHAR(220) NOT NULL,
       -- "Artist"        NVARCHAR(220),
        --"Length"        INTEGER NOT NULL,
        --"Url"   TEXT NOT NULL,
 --       "Art"   TEXT,
--        CONSTRAINT "PK_Track" PRIMARY KEY("TrackId"),
 --       UNIQUE("TrackName","Album")
--);
CREATE TABLE "User" (
        "UserId"        INTEGER NOT NULL PRIMARY KEY UNIQUE,
        "Username"      TEXT NOT NULL UNIQUE,
        "Password"      TEXT NOT NULL,
        "Display_name"  TEXT NOT NULL,
        "Email" TEXT NOT NULL UNIQUE,
        "Homepage_url"     TEXT
);
CREATE TABLE "Playlist" (
        "PlaylistId"    INTEGER NOT NULL,
        "PLaylistName"  NVARCHAR(120),
        "UserId"        INTEGER,
        "PlaylistDescription" TEXT,
        CONSTRAINT "PK_Playlist" PRIMARY KEY("PlaylistId"),
        UNIQUE("UserId","PlaylistName")
);
CREATE TABLE "Description" (
        "TrackId"       INTEGER NOT NULL,
        "UserId"        INTEGER NOT NULL,
        "Comment"       TEXT NOT NULL,
        FOREIGN KEY("UserId") REFERENCES "User"("UserId"),
        FOREIGN KEY("TrackId") REFERENCES "Track"("TrackId"),
        UNIQUE("TrackId","UserId")
);
CREATE TABLE "PlaylistTrack" (
        "PlaylistId"    INTEGER NOT NULL,
        "TrackId"       GUID,
        FOREIGN KEY("PlaylistId") REFERENCES "Playlist"("PlaylistId") ON DELETE NO ACTION ON UPDATE NO ACTION,
--        FOREIGN KEY("TrackId") REFERENCES "Track"("TrackId") ON DELETE NO ACTION ON UPDATE NO ACTION,
        UNIQUE("TrackId","PlaylistId")
);
--INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('For Those About To Rock (We Salute You)', 'For Those About to Rock We Salute You','Angus Young, Malcolm Young, Brian Johnson', 343719,"file://somewhere.mp3", "Example.jpg");
--INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('Fast As a Shark', 'Restless and Wild','F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman', 230619, "file://somewhere.mp3","Example.jpg");
--INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('Restless and Wild', 'Restless and Wild','F. Baltes, R.A. Smith-Diesel, S. Kaufman, U. Dirkscneider & W. Hoffman', 252051, "file://somewhere.mp3","Example.jpg");
--INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('Princess of the Dawn', 'Restless and Wild','Deaffy & R.A. Smith-Diesel', 343719, "file://somewhere.mp3","Example.jpg");
INSERT INTO Playlist(PlaylistName, UserId, PlaylistDescription) VALUES('Good Songs', 1, 'Songs that are good');
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(1, 1);
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(2, 1);
INSERT INTO Playlist(PlaylistName, UserId, PlaylistDescription) VALUES('More Good Songs', 1, 'MORE Songs that are good!!!!!');
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(1, 2);
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(2, 2);
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(3, 2);
INSERT INTO PlaylistTrack(TrackId, PlaylistId) VALUES(4, 2);
COMMIT;
