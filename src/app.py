from flask import Flask, request, render_template, Response, json
from flask_restful import Api, Resource
from db import create_table, create_user, get_user


app = Flask(__name__, template_folder='templates')
api = Api(app)

@app.route("/")
def my_form():
    ''' Loads an html file template using jinja
    '''
    return render_template('register.html.jinja')

@app.route("/profile")
def user_profile():
    ''' Loads an html file template using jinja
    '''
    return render_template('user_profile.html.jinja')


class users_api(Resource):
    def post(self):
        ''' Registers new user into users database from a post request
        '''
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        user_id = create_user(name, username, email, phone, password)
        return Response(
            response=json.dumps({
                "data": {
                    "id": user_id,
                    "email": email,
                    "username": username,
                    "name": name,
                    "phone": phone
                }
            }),
            status=201,
            mimetype="application/json"
        )


class users_db_api(Resource):      
    def get(self, user_id):
        ''' Take a userid and returns the data of that user
        '''
        _, name, username, email, _, phone = get_user(user_id)
        return Response(
            response=json.dumps({
                "data": {
                    "id": user_id,
                    "email": email,
                    "username": username,
                    "name": name,
                    "phone": phone
                }
            }),
            status=200,
            mimetype="application/json"
        )
        

api.add_resource(users_api, '/users', endpoint = 'users')
api.add_resource(users_db_api, '/users/<string:user_id>', endpoint = 'user')
if __name__ ==  "__main__":
    # create_table()
    app.run(debug=True)