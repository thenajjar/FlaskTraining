from urllib import response
from src.database.users import users_db
from src.swagger.swagger_schemas import *
from src.wtforms.wtforms_templates import *
from src.errors.errors_fun import error_response
from src.routes.validation import valid_request_type, valid_user, valid_wtform, password_match

from src.hashlib.encryption import encrypt
from src.jwt.tokens import tokenize, valid_jwt, decode_token

from flask import request, Response, json
from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource


class users_api(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=RegisterNewUserForm)
    @doc(description='Register a new user', tags=['Register'])
    @use_kwargs(RegisterUserRequestSchema, location=('json'))
    @marshal_with(RegisterUserResponseSchema)
    def post(self):
        """Takes a request containing users details, and creates new user 
        and returns user_id if a user was created

        Returns:
            class: flask response class containin guser_id as response body
        """
        # a wtform template for regisertering new users with data validation
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        # one way encryption for the passwords to store them
        password = encrypt(request.form['password'])
        confirm_password = encrypt(request.form['confirm_password'])
        role = "user"
        # make sure the passwords are matching
        try:
            password_match(password, confirm_password)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        # try to create a new user with the users details
        try:
            user_id = users_db.create_user(
                name, username, email, phone, password, role)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        # send an otp message to the user
        print("sending otp")
        from src.twilio.otp import send_otp_sms_call
        send_otp_sms_call(phone)
        print("sent otp")
        # the reponse body to send in flask response
        payload = json.dumps({
            "user_id": user_id,
            "username": username
        })
        token = tokenize({'user_id': int(user_id)})
        # if an otp message was sent successfuly
        response = Response(
            response=payload,
            status=201,
            # the response body content type
            mimetype="application/json"
        )
        response.headers['Authorization'] = "Bearer " + token
        return response


class users_api_get(MethodResource, Resource):
    @valid_jwt
    @doc(description='Get all the users details', tags=['Users'])
    @use_kwargs(GetUserRequestSchema, location=('json'))
    @marshal_with(GetUserResponseSchema)
    def get(self, user_id):
        """ Takes a user_id from a request and returns the data of that 
        user if the user exists and sends an otp code to that user.

        Returns:
            class: flask response class containing user data
        """
        try:
            jwt_token = request.headers['authorization'].split(" ")[1]
            request_user_id = decode_token(jwt_token)['user_id']
            if int(user_id) != int(request_user_id) and users_db.get_role('user_id', request_user_id) != 'admin':
                return error_response('403', 'UNAUTHORIZED', 'You dont have permission.', "")
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        try:
            _, name, username, email, _, phone, *_ = users_db.get_user(
                user_id)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        payload = json.dumps({
            "user_id": user_id,
            "email": email,
            "username": username,
            "name": name,
            "phone": phone
        })
        response = Response(
            response=payload,
            status=200,
            # the response body content type
            mimetype="application/json"
        )
        return response


class verify_api(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=OTPVerifyForm)
    @valid_jwt
    @doc(description='Verify the OTP code to register new users', tags=['Register'])
    @use_kwargs(OTPRequestSchema, location=('json'))
    @marshal_with(OTPResponseSchema)
    def post(self):
        """Take a userid and OTP from the request, and validates if the OTP code is correct

        Returns:
            class: flask response class containing user data
        """
        user_id = request.form['user_id']
        otp = request.form['otp']
        try:
            _, name, username, email, _, phone, _ = users_db.get_user(user_id)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        try:
            from src.twilio.otp import verify_otp_sms
            verify_status = verify_otp_sms(phone, otp)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        if verify_status:
            return Response(
                response=json.dumps({
                    "user_id": user_id,
                    "email": email,
                    "username": username,
                    "name": name,
                    "phone": phone
                }),
                status=200,
                # the response body content type
                mimetype="application/json"
            )
        else:
            return error_response("409", "CONFLICT", "OTP verfication failed.", verify_status)


class login_api(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=LoginForm)
    def post(self):
        """authenticate the user credintials using username and password and sends a 
        jwt token in response header

        Returns:
            class: flask response class containing jwt token if the user is authorized
        """
        username = request.form['username']
        password = encrypt(request.form['password'])
        try:
            valid_user(username, password)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        user_id = users_db.get_id('username', username)
        token = tokenize({'user_id': int(user_id)})
        payload = json.dumps({
            "username": username,
            "user_id": user_id  
        })
        response = Response(
            response=payload,
            status=200,
            # the response body content type
            mimetype="application/json"
        )
        response.headers['Authorization'] = "Bearer " + token
        return response
