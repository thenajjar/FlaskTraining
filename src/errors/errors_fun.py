from flask import Response, json

from src.config.config import app_configs


def error_response(http_response_code, error_code, error_description, error_payload=""):
    """Takes http response code, and error code string and description to that error code, 
    and an optional error payload, and returns these values in a json formatted response. 

    Args:
        http_response_code (int, str): the http response code
        error_code (str): the error type
        error_description (str): description about the error
        error_payload (str) optional: additional information about the error

    Returns:
        class: a flask response class
    """
    # print additional error payload if the app settings err_payload is set to true
    if app_configs.get("ERROR_PAYLOAD"):
        # make sure the additional error payload is not empty
        if error_payload:
            return Response(
                response=json.dumps({
                    "error_code": str(error_code),
                    "error_description": str(error_description),
                    "error_payload": str(error_payload)
                }),
                # http response code
                status=int(http_response_code)
            )
    # if both cases before fail, return a response without additional error_payload
    return Response(
        response=json.dumps({
            "error_code": str(error_code),
            "error_description": str(error_description)
        }),
        # http response code
        status=int(http_response_code)
    )
