from .celery_app import celery_app
from scrapers.vietstock import scrape_vietstock_articles

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
