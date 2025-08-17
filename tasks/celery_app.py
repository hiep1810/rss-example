from celery import Celery

# Create a centrally configured Celery app instance
celery_app = Celery('tasks', include=['tasks.worker'])

# Load configuration from the celeryconfig.py file
celery_app.config_from_object('celeryconfig')
