-- :name create_user :insert
INSERT INTO User(Username, Password, Display_Name, Email, Homepage_url)
VALUES(:Username, :Password, :Display_name, :Email, :Homepage_url)
