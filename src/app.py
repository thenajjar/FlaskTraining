from flask import Flask, render_template, Response, json, request
from flask_restful import Api, Resource
from db import create_table, create_user, get_user
from send_sms import send_otp_sms, verify_otp_sms
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__, template_folder='templates')
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

class RegisterUserRequestSchema(Schema):
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='+966541942414')
    password = fields.Str(default='password')

class RegisterUserResponseSchema(Schema):
    user_id = fields.Str(default='1')
    
class GetUserResponseSchema(Schema):
    user_id = fields.Str(default='1')
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='+966541942414')
    
class GetUserRequestSchema(Schema):
    user_id = fields.Str(default='1')
    
class OTPResponseSchema(Schema):
    user_id = fields.Str(default='1')
    username = fields.Str(default='username')
    name = fields.Str(default='FirstName LastName')
    email = fields.Str(default='email@domain.com')
    phone = fields.Str(default='+966541942414')
    
class OTPRequestSchema(Schema):
    user_id = fields.Str(default='1')

class OTPSchema(Schema):
    message = fields.Str(default='Success')
    
@app.route("/")
def my_form():
    ''' Loads an html file template using jinja
    '''
    return render_template('register.html.jinja')


class users_api(MethodResource, Resource):
    @doc(description='Register a new user', tags=['Register'])
    @use_kwargs(RegisterUserRequestSchema, location=('json'))
    @marshal_with(RegisterUserResponseSchema)
    def post(self):
        ''' Registers new user into users database from a post request
        '''
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        user_id = create_user(name, username, email, phone, password)
        otp_status = send_otp_sms(phone)
        print("send otp status", otp_status)
        if otp_status:
            return Response(
                response=json.dumps({
                    "data": {
                        "id": user_id,
                    }
                }),
                status=201,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({
                    "data": {
                        "id": user_id,
                    }
                }),
                status=405,
                mimetype="application/json"
            )

class users_db_api(MethodResource, Resource):
    @doc(description='Get all the users details', tags=['Users'])
    @use_kwargs(GetUserRequestSchema, location=('json'))
    @marshal_with(GetUserResponseSchema)
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
        
class verify_api(MethodResource, Resource):
    @doc(description='Verify the OTP code to register new users', tags=['Register'])
    @use_kwargs(OTPRequestSchema, location=('json'))
    @marshal_with(OTPResponseSchema)
    def post(self, user_id):
        ''' Take a userid and returns the data of that user
        '''
        _, name, username, email, _, phone = get_user(user_id)
        otp = request.form['otp']
        print("otp:", otp, " ,phone:", phone)
        verify_status = verify_otp_sms(phone, otp)
        print("verify status", verify_status)
        if verify_status:
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
        else:
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
                status=409,
                mimetype="application/json"
            )

api.add_resource(users_api, '/users')
api.add_resource(users_db_api, '/users/<string:user_id>')
api.add_resource(verify_api, '/verify/<string:user_id>')
docs.register(users_api)
docs.register(users_db_api)
docs.register(verify_api)

if __name__ ==  "__main__":
    # create_table()
    app.run(debug=True)