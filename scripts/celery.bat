@echo
:: run the celery app
:: to debug add: --loglevel=DEBUG, or --loglevel=INFO
celery -A app.celery worker --loglevel=INFO --concurrency 1 -P solo

pause