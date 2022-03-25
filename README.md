# Flask User Registration API
A project to train on REST API, PostgresSQL, Flask, Cron, Dockers

# Installation
### Installation
Create a local folder for your repo in your Windows OS
Open CMD and change directory to your local repo folder
Execute the following command in CMD to clone the repo
```
git clone https://github.com/thenajjar/Flask_User_Registration_API.git
```
Change the directory to the project folder "Flask_User_Registration_API-main"
Make a copy of .env.example file and rename it to be
```
.env
```
open .env file and add your twilio api keys, postgres db settings, and redis cache settings to it and choose the environment you want to run your application as (production, development, testing)

Go back to main project folder and create and activate virtualenv
```
python -m virtualenv venv
.\venv\Scripts\activate.bat
```
install the requirements
```
pip install -r requirements.txt
```
You're ready to go!

### Usage
Make sure you have a redis server running and Postgres
Open the base project folder and execute the following commands
```
.\Scripts\celery.bat
.\Scripts\run.bat
```
Now you can make calls to the API

### Database setup
If you don't have a database created yet, then go to project folder and make sure that the flask application is running as explained in Usage section.
execute the following command
```
flask db init
flask db migrate
flask db upgrade
```

# API
### Usage
####To register a new user
send a post request to
```
/users
```
Build your post request including the following values as multipart/form-data content-type
```
"user_id": <user_id>,
"email": <email>,
"username": <username>,
"name": <first and last name>,
"phone": <phone>,
"password": <password>,
"confirm_password": <password confirmation>
```
It will return the user_id that the db assigned to the new user if successful along with a jwt token in the authorization header of the request, and you will receive a sms OTP in your phone.

####To verify the user after registration
use the JWT token you recieved from creating a user along the OTP code and send a post request to
```
/verify
```
Build your post request including the following values as multipart/form-data content-type and include JWT token in authorization header
```
"user_id": <user_id>,
"otp": <otp code>
```

####To login
send post request to
```
/login
```
including the following values as multipart/form-data content-type
```
"username": <username>,
"password": <the user password>
```
You will receive a JWT token in the response authorization header if successful

####To get user data
send a GET request as follows along with JWT token from regeisteration or login in the request authorization header
```
/users/<user id>
```
It will return a json message including the user details:
```
{
    "id": <user_id>,
    "email": <email>,
    "username": <username>,
    "name": <first and last name>,
    "phone": <phone>
}
```
### Validation
### Errors


