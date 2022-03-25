from celery import Celery
from src.configModule.create_app import app


def make_celery(application):
    """Initialize celeryModule application with configurations from src.configModule.flask_config

    Args:
        application: flask application

    Returns:
        class: celeryModule application
    """
    celery_app = Celery(
        application.import_name,
        backend=application.config['RESULT_BACKEND'],
        broker=application.config['CELERY_BROKER_URL']
    )
    celery_app.conf.update(application.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with application.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)
celery.autodiscover_tasks(('src.twilioModule.otp',))
