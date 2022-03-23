from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


swagger_url = '/swagger/'
swagger_ui_url = '/docs/'
redis_url = 'redis://localhost:6379'

class FlaskProductionConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask environment
        'ENV': "production",
        # run flask in debug mode
        'DEBUG': False,
        # initiate a test client
        'TESTING': False,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegistrationAPI',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': swagger_url,  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': swagger_ui_url,  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "production_key",
        'CELERY_BROKER_URL': redis_url,
        'RESULT_BACKEND': redis_url
    }


class FlaskDevelopmentConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask environment
        'ENV': "development",
        # run flask in debug mode
        'DEBUG': True,
        # initiate a test client
        'TESTING': True,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegistrationAPI (Dev)',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': swagger_url,  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': swagger_ui_url,  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "development_key",
        'CELERY_BROKER_URL': redis_url,
        'RESULT_BACKEND': redis_url
    }


class FlaskTestingConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask environment
        'ENV': "development",
        # run flask in debug mode
        'DEBUG': False,
        # initiate a test client
        'TESTING': True,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegistrationAPI (Test)',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': swagger_url,  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': swagger_ui_url,  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "testing_key",
        'CELERY_BROKER_URL': redis_url,
        'RESULT_BACKEND': redis_url
    }
