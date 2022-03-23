from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

class FlaskProductionConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask enviornment
        'ENV': "production",
        # run flask in debug mode
        'DEBUG': False,
        # initate a test client
        'TESTING': False,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegesterationAPI',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/docs/',  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "production_key",
        'CELERY_BROKER_URL': 'redis://localhost:6379',
        'RESULT_BACKEND': 'redis://localhost:6379'
    }
    
class FlaskDevelopmentConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask enviornment
        'ENV': "development",
        # run flatsk in debug mode
        'DEBUG': True,
        # initate a test client
        'TESTING': True,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegesterationAPI (Dev)',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/docs/',  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "development_key",
        'CELERY_BROKER_URL': 'redis://localhost:6379',
        'RESULT_BACKEND': 'redis://localhost:6379'
    }
    
class FlaskTestingConfig(object):
    """Class to store flask settings in a dictionary called settings
    """
    configs = {
        # the flask enviornment
        'ENV': "development",
        # run flatsk in debug mode
        'DEBUG': False,
        # initate a test client
        'TESTING': True,
        # settings for swagger
        'APISPEC_SPEC': APISpec(
            title='FlaskUserRegesterationAPI (Test)',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='3.0.3'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/docs/',  # URI to access UI of API Doc
        'SECRET_KEY': "test",
        # CSRF key for wtforms
        'WTF_CSRF_SECRET_KEY': "testing_key",
        'CELERY_BROKER_URL': 'redis://localhost:6379',
        'RESULT_BACKEND': 'redis://localhost:6379',
    }