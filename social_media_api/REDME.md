## How to Register and Authenticate Users
Registration
Endpoint: POST /accounts/register/
Fields:
username (required)
email (required)
password (required)
bio (optional)
profile_picture (optional)
Login
Endpoint: POST /accounts/login/

Fields:

username (required)
password (required)
Response:

Returns an authentication token.
User Profile
Endpoint: GET /accounts/profile/

Headers:

Authorization: Token your_generated_token
Fields:

username
email
bio
profile_picture
followers_count
following_count
User Model Overview
The custom user model extends Django's AbstractUser and includes:

bio: Text field for user biography.
profile_picture: Image field for profile picture.
followers: Many-to-many field to other users.