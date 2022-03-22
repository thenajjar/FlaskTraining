from src.database.users import users_db
from src.twilio.verify import send_otp_sms, verify_otp_sms
from src.swagger.swagger_schemas import *
from src.wtforms.wtforms_templates import *
from src.errors.errors_fun import error_response
from src.routes.validation import valid_request_type, valid_user

from src.hashlib.encryption import encrypt
from src.jwt.tokens import tokenize, valid_jwt, decode_token

from flask import request, Response, json
from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource


def password_match(main_password, confirm_password, message=None):
    """Takes main password and a password to compare it with, and raises an error if 
    the passwords are not matching.

    Args:
        main_password (str): the main password
        confirm_password (str): the confirmation password to compare

    Raises:
        Exception: passwords values are not matching
    """
    # default message if message is not set
    if not message:
        message = 'Passwords are not matching.'
    # check if passwords are not matching
    if main_password != confirm_password:
        raise Exception("409", "CONFLICT", message, "")


class users_api(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
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
        user_form = RegisterNewUserForm()
        # validate the form data
        user_form.validate_on_submit()
        # catch any data validation errors
        errors = user_form.errors
        # loop through the errors if any
        for field, error_messages in errors.items():
            # return first error as a response
            return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        # one way encryption for the passwords to store them
        password = encrypt(request.form['password'])
        confirm_password = encrypt(request.form['confirm_password'])
        role = str(request.form['role']).lower()
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
        # otp_status = send_otp_sms(phone)
        otp_status = "hello"
        # the reponse body to send in flask response
        payload = json.dumps({
            "user_id": user_id,
        })
        # if an otp message was sent successfuly
        if otp_status:
            return Response(
                response=payload,
                status=201,
                # the response body content type
                mimetype="application/json"
            )
        else:
            return error_response("409", "CONFLICT", "OTP status error.", otp_status)


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
            if int(user_id) != int(request_user_id):
                if users_db.get_role('user_id', request_user_id) != 'admin':
                    return error_response('403', 'UNAUTHORIZED', 'You dont have permission.', "")
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        try:
            _, name, username, email, _, phone, role = users_db.get_user(user_id)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        payload = json.dumps({
            "user_id": user_id,
            "email": email,
            "username": username,
            "name": name,
            "phone": phone,
            "role": role
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
    @valid_jwt
    @doc(description='Verify the OTP code to register new users', tags=['Register'])
    @use_kwargs(OTPRequestSchema, location=('json'))
    @marshal_with(OTPResponseSchema)
    def post(self):
        """Take a userid and OTP from the request, and validates if the OTP 

        Returns:
            _type_: flask response class containing user data
        """
        otp_form = OTPVerifyForm()
        otp_form.validate_on_submit()
        errors = otp_form.errors
        for field, error_messages in errors.items():
            return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
        user_id = request.form['user_id']
        otp = request.form['otp']
        try:
            _, name, username, email, _, phone, _ = users_db.get_user(user_id)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
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
                mimetype="application/json"
            )
        else:
            return error_response("409", "CONFLICT", "OTP verfication failed.", verify_status)


class login_api(MethodResource, Resource):
    @valid_request_type(types=("multipart/form-data",))
    def post(self):
        login_form = LoginForm()
        login_form.validate_on_submit()
        errors = login_form.errors
        for field, error_messages in errors.items():
            return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
        username = request.form['username']
        password = encrypt(request.form['password'])
        try:
            valid_user(username, password)
        except Exception as error:
            return error_response(error.args[0], error.args[1], error.args[2], error.args[3])
        payload = json.dumps({
                    "username": username
                })
        user_id = users_db.get_id('username', username)
        token = tokenize({'user_id': int(user_id)})
        response = Response(
            response=payload,
            status=200,
            # the response body content type
            mimetype="application/json"
        )
        response.headers['Authorization'] = "Bearer " + token
        return response