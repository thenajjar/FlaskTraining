import datetime
import json

import jwt
from flask import request

from src.dotenv.load import get_var


def tokenize(payload_data, exp_time=None):
    """Takes a payload and a secret and returns a JWT token.

    Args:
        payload_data (json, str): the body of the JWT token
        exp_time (int): the time in minutes for the token expiration

    Returns:
        str: a JWT token of the payload and secret
    """
    if not exp_time:
        exp_time = 1440
    else:
        exp_time += 180
    secret = get_var('JWT_SECRET')
    # make sure the type is json, and if it's string convert it to json
    if type(payload_data) == str:
        payload_data = json.loads(payload_data)
    # convert the payload_data json and the secret into jwt token string
    exp_timestamp = int(datetime.datetime.fromisoformat(
        str(datetime.datetime.utcnow() + datetime.timedelta(minutes=int(exp_time)))).timestamp())
    payload_data.update({"exp": exp_timestamp})
    token = jwt.encode(
        payload=payload_data,
        key=str(secret)
    )
    return token


def decode_token(token):
    """Validate a JWT token

    Args:
        token: jwt token

    Returns:
        payload (json): the payload of the JWT token
    """
    secret = get_var('JWT_SECRET')
    # make sure the type is json, and if it's string convert it to json
    try:
        payload = jwt.decode(jwt=str(token), key=str(secret), algorithms=["HS256", ])
        return payload
    except Exception as jwt_error:
        raise Exception("401", "UNAUTHORIZED", "Authentication failed.", jwt_error)


def valid_jwt(fun):
    """validates a barear jwt token from a request authorization header

    Args:
        fun (function): a flask request function with an authorization header
    """

    def wrapper(*args, **kwargs):
        try:
            jwt_token = request.headers['authorization'].split(" ")[1]
            decode_token(jwt_token)
            return fun(*args, **kwargs)
        except Exception as error:
            return error

    return wrapper
