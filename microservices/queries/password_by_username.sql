-- :name password_by_username :1
SELECT Password from User 
WHERE Username = :Username