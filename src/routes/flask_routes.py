from flask import request, Response, json
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from src.sqlalchemyModule.db_connection import db
from src.sqlalchemyModule.users import UsersDb
from src.errorsModule.errors_fun import error_response
from src.hashlibModule.encryption import encrypt
from src.jwtModule.tokens import tokenize, valid_jwt, decode_token
from src.routes.validation import valid_request_type, valid_user, valid_wtform, password_match
from src.swaggerModule.swagger_schemas import GetUserRequestSchema, GetUserResponseSchema, RegisterUserRequestSchema, \
    RegisterUserResponseSchema, OTPResponseSchema, OTPRequestSchema
from src.wtformsModule.wtforms_templates import RegisterNewUserForm, OTPVerifyForm, LoginForm
from src.twilioModule.otp import verify_otp_sms, send_otp_sms_call

json_mime_type = "application/json"


class UsersApi(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=RegisterNewUserForm)
    @doc(description='Register a new user', tags=['Register'])
    @use_kwargs(RegisterUserRequestSchema, location=('json'))
    @marshal_with(RegisterUserResponseSchema)
    def post(self):
        """Takes a request containing users details, and creates new user 
        and returns user_id if a user was created

        Returns:
            class: flask response class containing user_id as response body
        """
        # a wtform template for registering new users with data validation
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
            new_user = UsersDb(name=name, username=username, email=email, phone=phone, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            user_id = new_user.user_id
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        # send an otp message to the user
        send_otp_sms_call(phone)
        # the response body to send in flask response
        payload = json.dumps({
            "user_id": user_id,
            "username": username
        })
        token = tokenize({'user_id': int(user_id)})
        # if an otp message was sent successfully
        response = Response(
            response=payload,
            status=201,
            # the response body content type
            mimetype=json_mime_type
        )
        response.headers['Authorization'] = "Bearer " + token
        return response


class UsersApiGet(MethodResource, Resource):
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
        user = UsersDb.query.get(user_id)
        try:
            jwt_token = request.headers['authorization'].split(" ")[1]
            request_user_id = decode_token(jwt_token)['user_id']
            request_user = UsersDb.query.get(request_user_id)
            if int(user_id) != int(request_user.user_id):
                if request_user.role != 'admin':
                    return error_response('403', 'UNAUTHORIZED', 'You dont have permission.', "")
        except Exception as error:
            return error_response('403', 'UNAUTHORIZED', 'You dont have permission.', error.args[3])
        name = user.name
        email = user.email
        username = user.username
        phone = user.phone
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
            mimetype=json_mime_type
        )
        return response


class VerifyApi(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=OTPVerifyForm)
    @valid_jwt
    @doc(description='Verify the OTP code to register new users', tags=['Register'])
    @use_kwargs(OTPRequestSchema, location=('json'))
    @marshal_with(OTPResponseSchema)
    def post(self):
        """Take a user_id and OTP from the request, and validates if the OTP code is correct

        Returns:
            class: flask response class containing user data
        """
        user_id = request.form['user_id']
        otp = request.form['otp']
        user = UsersDb.query.get(user_id)
        name = user.name
        email = user.email
        username = user.username
        phone = user.phone
        try:
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
                mimetype=json_mime_type
            )
        else:
            return error_response("409", "CONFLICT", "OTP verification failed.", verify_status)


class LoginApi(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    @valid_wtform(form=LoginForm)
    def post(self):
        """authenticate the user credentials using username and password and sends a
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
        user = UsersDb.query.filter_by(username=username).first()
        user_id = user.user_id
        token = tokenize({'user_id': int(user_id)})
        payload = json.dumps({
            "username": username,
            "user_id": user_id
        })
        res = Response(
            response=payload,
            status=200,
            # the response body content type
            mimetype=json_mime_type
        )
        res.headers['Authorization'] = "Bearer " + token
        return res
