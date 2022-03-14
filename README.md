# Flask Training Project
A project to train on REST API, PostgresSQL, Flask, Cron, Dockers

# Installation
### Installation
Create a local folder for your repo in your Windows OS
Open CMD and change directory to your local repo folder
Execute the follwing command in CMD to clone the repo
```
git clone https://github.com/thenajjar/FlaskTraining.git
```
Change the directory to the project folder "FlaskTraining"
Make a copy of .env file and add a name after for example ".env.var"
Add your twilio api keys
Change to src folder and create a folder named database.ini
Copy and paste the following values with your PostgresSQL db info
```
[postgresql]
host=
database=
user=
password=
```
Create and activate virtualenv
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
Open the project folder and execute the following command
```
python src/app.py
```
go to http://127.0.0.1:5000/

### API
To register a new user send a post request to
```
/users
```
Build your post request inclduing following values in the json response body
```
{
    "data": {
        "id": user_id,
        "email": email,
        "username": username,
        "name": name,
        "phone": phone
    }
}
```
It will return the userdata with the user_id that the db assigned

To get user data using the user id send a GET request
```
/users/<user id>
```



