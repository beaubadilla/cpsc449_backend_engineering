-- $ sqlite3 tracks3.db < sqlite.sql

BEGIN TRANSACTION;
DROP TABLE IF EXISTS "Track";

CREATE TABLE "Track" (
        "TrackId"       GUID,
        "TrackName"  NVARCHAR(200) NOT NULL,
        "Album" NVARCHAR(220) NOT NULL,
        "Artist"        NVARCHAR(220),
        "Length"        INTEGER NOT NULL,
        "Url"   TEXT NOT NULL,
        "Art"   TEXT,
        CONSTRAINT "PK_Track" PRIMARY KEY("TrackId"),
        UNIQUE("TrackName","Album")
);

INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('Princess of the Dawn', 'Restless and Wild','Deaffy & R.A. Smith-Diesel', 343719, "file://somewhere.mp3","Example.jpg");

COMMIT;
