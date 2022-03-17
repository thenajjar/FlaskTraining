class AppProductionConfig(object):
    configs = {
        'ERROR_PAYLOAD': False
    }
    
class AppDevelopmentConfig(object):
    configs = {
        'ERROR_PAYLOAD': True
    }
    
class AppTestingConfig(object):
    configs = {
        'ERROR_PAYLOAD': True
    }