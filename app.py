# from src.database_module.users import create_table
from src.routes.flask_routes import *
from src.config.flask_config import *

from flask import Flask
from flask_restful import Api

from flask_apispec.extension import FlaskApiSpec

import jwt
import sys

# define flask app
app = Flask(__name__, template_folder='templates')
# define the restful api
api = Api(app)
# production configs for flask
pcfg = FlaskProductionConfig.configs
# developmenet configs for flask
dcfg = FlaskDevelopmentConfig.configs
# testing configs for flask
tcfg = FlaskTestingConfig.configs
# update the flask app to the selected config
app.config.update(dcfg)
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
    app.run()


if __name__ == "__main__":
    try:
        create_db_arg = str(sys.argv[1])
        print(create_db_arg)
        main(create_db_arg)
    except:
        main()
