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
                request_content_type = request.headers['content-type'].split(";")[0]
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
    try:
        user_id = users_db.get_id('username', username)
        _, _, _, _, db_password, *_ = users_db.get_user(user_id)
        if password == db_password:
            return True
        else:
            raise Exception("403", "UNAUTHORIZED", "Wrong password or username.", "")
    except Exception as error:
        raise Exception("403", "UNAUTHORIZED", "Wrong password or username.", error)