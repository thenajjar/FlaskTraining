# Flask User Registration API
A project to train on REST API, PostgresSQL, Flask, Cron, Dockers

# Installation
### Installation
Create a local folder for your repo in your Windows OS
Open CMD and change directory to your local repo folder
Execute the follwing command in CMD to clone the repo
```
git clone https://github.com/thenajjar/Flask_User_Registration_API.git
```
Change the directory to the project folder "Flask_User_Registration_API-main"
Make a copy of .env.example file and rename it to be
```
.env
```
open .env file and add your twilio api keys to it and choose the environment you want to run your application as (production, deveolpment, testing)
Change directory to src/database
Make copy of database.ini.example and name it to be
```
database.ini
```
open the database.ini and fill in your postgres database and host information

Go back to main project folder and create and activate virtualenv
```
python -m virtualenv venv
.\venv\Scripts\activate.bat
```
install the requirments
```
pip install -r requirements.txt
```
You're ready to go!


### Usage
Open the base project folder and execute the following command
```
python -m app
```
Now you can make calls to the API

# API
### Usage
To register a new user send a post request to
```
/users
```
Build your post request inclduing following values as multipart/form-data content-type
```
"id": <user_id>,
"email": <email>,
"username": <username>,
"name": <first and last name>,
"phone": <phone>,
"password": <password>,
"confirm_password": <password confirmation>
```
It will return the user_id that the db assigned to the new user if successful

To get luser data from the database use the user id to send a GET request as follows
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


