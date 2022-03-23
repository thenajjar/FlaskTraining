from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api

from src.celery.celery_config import make_celery
from src.config.config import app_configs
from src.routes.flask_routes import UsersApi, UsersApiGet, LoginApi, VerifyApi

# define flask app
app = Flask(__name__, template_folder='templates')
# define the restful api
api = Api(app)
# update the flask app to the selected config
app.config.update(app_configs.settings['flask'])
# create celery app
celery = make_celery(app)
celery.autodiscover_tasks(('src.twilio.otp',))
# generate swagger documentation
docs = FlaskApiSpec(app)

# define flask routes and link them to the api resource classes
api.add_resource(UsersApi, '/users')
api.add_resource(UsersApiGet, '/users/<string:user_id>')
api.add_resource(VerifyApi, '/verify')
api.add_resource(LoginApi, '/login')

# register swagger docs to each api resource
docs.register(UsersApi)
docs.register(UsersApiGet)
docs.register(VerifyApi)


def main():
    app.run()


if __name__ == "__main__":
    main()
