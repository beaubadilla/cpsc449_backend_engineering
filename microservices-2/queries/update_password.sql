-- :name update_password :affected
UPDATE User set Password = :Password
WHERE Username = :Username;
