from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

class FlaskProductionConfig(object):
    configs = {
        'ENV': "production",
        'DEBUG': False,
        'TESTING': False,
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
    }
    
class FlaskDevelopmentConfig(object):
    configs = {
        'ENV': "development",
        'DEBUG': True,
        'TESTING': True,
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
    }
    
class FlaskTestingConfig(object):
    configs = {
        'ENV': "development",
        'DEBUG': True,
        'TESTING': True,
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
    }