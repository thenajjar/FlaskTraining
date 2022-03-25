from flask_sqlalchemy import SQLAlchemy

from src.configModule.config import app_configs
from src.redisModule.redis_config import RedisCache
from flask import Flask

from flask_restful import Api
from flask_caching import Cache

from flask_apispec import FlaskApiSpec

def generate_app():

    # define flask app
    app = Flask(__name__, template_folder='templates')
    # update the flask app to the selected config
    app.config.update(app_configs.settings['flask'])
    # create the redis cache
    cache = Cache(app, config=RedisCache.config)
    # define the restful api
    api = Api(app)
    db = SQLAlchemy(app)

    docs = FlaskApiSpec(app)
    return (app, db, cache, api, docs)


app, db, cache, api, docs = generate_app()