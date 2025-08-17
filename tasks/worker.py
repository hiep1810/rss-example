from celery import Celery
from scrapers.vietstock import scrape_vietstock_articles

# Create Celery app instance
celery_app = Celery('tasks', include=['tasks.worker'])

# Load configuration from a separate file
celery_app.config_from_object('celeryconfig')

@celery_app.task
def run_vietstock_scraper():
    """
    Celery task that runs the Vietstock article scraper.
    """
    return scrape_vietstock_articles()

@celery_app.task
def add(x, y):
    """
    A simple debug task that adds two numbers.
    """
    return x + y
