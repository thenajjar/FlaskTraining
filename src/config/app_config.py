class AppProductionConfig(object):
    """Production Environment settings for the application.
    """
    configs = {
        # Boolen to display additional error payload used for development purposes
        'ERROR_PAYLOAD': False
    }


class AppDevelopmentConfig(object):
    """Development Environment settings for the application.
    """
    configs = {
        # Boolen to display additional error payload used for development purposes
        'ERROR_PAYLOAD': True
    }


class AppTestingConfig(object):
    """Test Environment settings for the application.
    """
    configs = {
        # Boolen to display additional error payload used for development purposes
        'ERROR_PAYLOAD': True
    }
