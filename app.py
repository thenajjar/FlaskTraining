# from src.database_module.users import create_table
from src.routes.flask_routes import *

from flask import Flask
from flask_restful import Api

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

import jwt
import sys

# define flask app
app = Flask(__name__, template_folder='templates')
# define the restful api
api = Api(app)
# set testing enviroment
app.config['TESTING'] = True

app.config.update({
    # settings for swagger
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',  # URI to access UI of API Doc
    'SECRET_KEY': "test",
    # CSRF key for wtforms
    'WTF_CSRF_SECRET_KEY': "test123"
})

# generate swagger documentation
docs = FlaskApiSpec(app)

api.add_resource(users_api, '/users')
api.add_resource(users_api_get, '/users/<string:user_id>')
api.add_resource(verify_api, '/verify')
docs.register(users_api)
docs.register(users_api_get)
docs.register(verify_api)


def main(args=None):
    if args:
        print(type(args))
    # create_table()
    app.run(debug=True)


if __name__ == "__main__":
    try:
        create_db_arg = str(sys.argv[1])
        print(create_db_arg)
        main(create_db_arg)
    except:
        main()
