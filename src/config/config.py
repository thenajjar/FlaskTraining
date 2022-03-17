from pickletools import read_uint1
from src.config.flask_config import *
from src.config.app_config import *

from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

class configurations(object):
    def __init__(self, env):
        if not env:
            env = 'd'
        flask_conf = FlaskDevelopmentConfig.configs
        app_conf = AppDevelopmentConfig.configs
        if env.lower() in ['production', 'p', 'prod']:
            flask_conf = FlaskProductionConfig.configs
            app_conf = AppProductionConfig.configs
        elif env.lower() in ['development', 'd', 'dev']:
            flask_conf = FlaskDevelopmentConfig.configs
            app_conf = AppDevelopmentConfig.configs
        elif env.lower() in ['test', 't', 'testing']:
            flask_conf = FlaskTestingConfig.configs
            app_conf = AppTestingConfig.configs
        self.settings = {'env': env, 'flask': flask_conf, 'app': app_conf}
    
    def __call__(self): 
        return self.settings
        
    def get(self, key):
        try:
            value = self.settings['app'][str(key)]
        except Exception as error:
            raise Exception(error)
        return  value
    
config_env = getenv('APP_ENV')
app_configs = configurations(config_env)