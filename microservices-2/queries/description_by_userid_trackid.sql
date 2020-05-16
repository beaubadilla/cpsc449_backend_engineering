-- :name description_by_userid_trackid :one
Select Comment
from Description
WHERE UserId = :UserId and TrackId = :TrackId
