"""
GIVEN there are active users
WHEN an exercise is created by the admin
AND the exercise's user is NULL
THEN the exercise should be assigned to all users
AND any existing user exercise by the same name is not overwritten
"""
