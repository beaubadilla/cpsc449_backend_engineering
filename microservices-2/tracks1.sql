-- $ sqlite3 tracks1.db < sqlite.sql

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

INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('For Those About To Rock (We Salute You)', 'For Those About to Rock We Salute You','Angus Young, Malcolm Young, Brian Johnson', 343719,"file://somewhere.mp3", "Example.jpg");
INSERT INTO Track(TrackName, Album, Artist, Length, Url, Art) VALUES('Fast As a Shark', 'Restless and Wild','F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman', 230619, "file://somewhere.mp3","Example.jpg");

COMMIT;
