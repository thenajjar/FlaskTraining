from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Api
from flask_caching import Cache
from flask_apispec import FlaskApiSpec

from src.configModule.config import app_configs
from src.redisModule.redis_config import RedisCache


def generate_app():
    """Generate configured flask application

    Returns:
        app: flask application
        db: sqlalchemy database
        cache: Rediscache
        api: restful api
        docs: flask api spec
    """
    # define flask app
    new_app = Flask(__name__, template_folder='templates')
    # update the flask app to the selected config
    new_app.config.update(app_configs.settings['flask'])
    # create the redis cache
    new_cache = Cache(new_app, config=RedisCache.config)
    # define the restful api
    new_api = Api(new_app)
    # define and create sqlachemy database object
    new_db = SQLAlchemy(new_app)
    # generate documentations to be used with swagger
    new_docs = FlaskApiSpec(new_app)
    return new_app, new_db, new_cache, new_api, new_docs


app, db, cache, api, docs = generate_app()
