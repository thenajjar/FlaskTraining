from src.errors.errors_fun import error_response
from src.database.users import users_db
from flask import request


def valid_request_type(types):
    """Check if content type of a flask response of an inner function is valid type.

    Args:
        types (tuple): a tuple that includes all acceptable content types
    """
    def inner(fun):
        def wrapper(*args, **kwargs):
            try:
                # exctract the request content-type from a request
                request_content_type = request.headers['content-type'].split(";")[
                    0]
                if request_content_type not in types:
                    return error_response(409, "SYNTAX", "Unacceptable content-type",
                                          "Please only use multipart/form-data content-type")
                return fun(*args, **kwargs)
            except:
                return error_response(409, "SYNTAX", "Missing request body",
                                      "Please include multipart/form-data body")
        return wrapper
    return inner


def valid_user(username, password):
    """validate username and password and make sure they belong to the same user

    Args:
        types (tuple): a tuple that includes all acceptable content types

    Returns:
        True (boolen): if password matches the user password in the db
    """
    try:
        user_id = users_db.get_id('username', username)
        _, _, _, _, db_password, *_ = users_db.get_user(user_id)
        if password == db_password:
            return True
        else:
            raise Exception("403", "UNAUTHORIZED",
                            "Wrong password or username.", "")
    except Exception as error:
        raise Exception("403", "UNAUTHORIZED",
                        "Wrong password or username.", error)


def valid_wtform(form):
    """Validates request fields with wtforms validations

    Args:
        form(class): wtform template
    """
    def inner(fun):
        def wrapper(*args, **kwargs):
            try:
                # exctract the request content-type from a request
                # jtforms for OTP request
                new_form = form()
                # validate the request form fields
                new_form.validate_on_submit()
                # make sure there are no errors
                errors = new_form.errors
                for field, error_messages in errors.items():
                    return error_response(409, "CONFLICT", error_messages[0].replace("Field", field).replace("This field", field + " field"))
                return fun(*args, **kwargs)
            except:
                return error_response(409, "SYNTAX", "Missing request body",
                                      "Please include multipart/form-data body")
        return wrapper
    return inner


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
