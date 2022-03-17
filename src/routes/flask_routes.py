from src.database.users import create_user, get_user
from src.twilio.verify import send_otp_sms, verify_otp_sms
from src.swagger.swagger_schemas import *
from src.wtforms.wtforms_templates import *

from flask import request, Response, json
from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource


def error_response(http_response_code, error_code, error_description, error_payload=""):
    """
    Takes http response code, and error code string and description to that error code, 
    and an optional error payload, and returns these values in a json formatted response    
    """

    if error_payload:
        return Response(
            response=json.dumps({
                "error_code": str(error_code),
                "error_description": str(error_description),
                "error_payload": str(error_payload)
            }),
            status=int(http_response_code)
        )
    else:
        return Response(
            response=json.dumps({
                "error_code": str(error_code),
                "error_description": str(error_description)
            }),
            status=int(http_response_code)

        )


def password_match(main_password, confirm_password, message=None):
    """ takes main password and a password to compare it with, and raises an error if 
    the passwords are not matching
    """
    if not message:
        message = 'Passwords are not matching.'
    if main_password != confirm_password:
        raise Exception(message)


class users_api(MethodResource, Resource):
    @doc(description='Register a new user', tags=['Register'])
    @use_kwargs(RegisterUserRequestSchema, location=('json'))
    @marshal_with(RegisterUserResponseSchema)
    def post(self):
        """ Registers new user into users database from a post request
        """
        try:
            request_media_type = request.headers['content-type'].split(";")[0]
            if request_media_type != "multipart/form-data":
                return error_response(409, "SYNTAX", "Unacceptable content-type",
                                      "Please only use multipart/form-data content-type")
        except:
            return error_response(409, "SYNTAX", "Missing request body",
                                  "Please include multipart/form-data body")
        user_form = RegisterNewUserForm()
        user_form.validate_on_submit()
        errors = user_form.errors
        for field, error_messages in errors.items():
            return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        try:
            password_match(password, confirm_password)
        except Exception as error_message:
            return error_response(409, "CONFLICT", error_message)
        user_id = create_user(name, username, email, phone, password)
        # otp_status = send_otp_sms(phone)
        otp_status = "hello"
        if otp_status:
            return Response(
                response=json.dumps({
                    "data": {
                        "user_id": user_id,
                    }
                }),
                status=201,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({
                    "data": {
                        "user_id": user_id,
                    }
                }),
                status=405,
                mimetype="application/json"
            )


class users_api_get(MethodResource, Resource):
    @doc(description='Get all the users details', tags=['Users'])
    @use_kwargs(GetUserRequestSchema, location=('json'))
    @marshal_with(GetUserResponseSchema)
    def get(self, user_id):
        """ Take a userid and returns the data of that user
        """
        try:
            _, name, username, email, _, phone = get_user(user_id)
        except Exception as error_message:
            return error_response(404, "NOT_FOUND", error_message)
        return Response(
            response=json.dumps({
                "data": {
                    "user_id": user_id,
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
    def post(self):
        """ Take a userid and returns the data of that user
        """
        try:
            request_media_type = request.headers['content-type'].split(";")[0]
            if request_media_type != "multipart/form-data":
                return error_response(409, "SYNTAX", "Unacceptable content-type",
                                      "Please only use multipart/form-data content-type")
        except:
            return error_response(409, "SYNTAX", "Missing request body",
                                  "Please include multipart/form-data body")
        otp_form = OTPVerifyForm()
        otp_form.validate_on_submit()
        errors = otp_form.errors
        for field, error_messages in errors.items():
            return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
        user_id = int(request.form['user_id'])
        otp = str(request.form['otp'])
        try:
            _, name, username, email, _, phone = get_user(user_id)
        except Exception as error_message:
            return error_response(404, "NOT_FOUND", error_message)
        verify_status = verify_otp_sms(phone, otp)
        if verify_status:
            return Response(
                response=json.dumps({
                    "data": {
                        "user_id": user_id,
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
                        "user_id": user_id,
                        "email": email,
                        "username": username,
                        "name": name,
                        "phone": phone
                    }
                }),
                status=409,
                mimetype="application/json"
            )
