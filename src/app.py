from flask import Flask, request, render_template, Response, json

app = Flask(__name__, template_folder='templates')

users_list = []

@app.route("/")
def my_form():
    ''' Returns a jinja template object from an html template
    '''
    return render_template('register.html.jinja')

@app.route('/register', methods=['POST'])
def my_form_post():
    ''' Registers new user into users_list from a post request
    '''
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    user_id = str(len(users_list))
    users_list.append({
                "id": user_id,
                "email": email,
                "username": username,
                "name": name,
                "phone": phone,
                "password": password
            })
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
    
@app.route('/users/<string:user_id>/', methods=['GET'])
def my_form_get(user_id):
    ''' Take a userid and returns the data of that user
    '''
    username = users_list[int(user_id)]['username']
    name = users_list[int(user_id)]['name']
    email = users_list[int(user_id)]['email']
    phone = users_list[int(user_id)]['phone']
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

if __name__ ==  "__main__":
    app.run(debug=True)