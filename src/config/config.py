from pickletools import read_uint1
from src.config.flask_config import *
from src.config.app_config import *

from dotenv import load_dotenv, find_dotenv
from os import getenv

# Load the enviornment variables
load_dotenv(find_dotenv())


class configurations(object):
    """Class to store application settings in a dictionary called settings
    """

    def __init__(self, env=None):
        if not env:
            # define environment as deveolopment if user didn't specify an env
            env = 'd'
        # default flask configuration to development env
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
        """get a value from settings dictionary based on a key

        Args:
            key (str): the settings dictionary key used to return a value

        Raises:
            Exception: if key is not present in the settings dictionary

        Returns:
            value: the value of the key in the settings dictionary of app settings
        """
        try:
            value = self.settings['app'][str(key)]
        except Exception as error:
            raise Exception(error)
        return value


config_env = getenv('APP_ENV')
app_configs = configurations(config_env)
