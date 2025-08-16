from celery import Celery
from scrapers.vietstock import scrape_vietstock_articles

# Configure Celery
celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def run_vietstock_scraper():
    """
    Celery task that runs the Vietstock article scraper.
    """
    return scrape_vietstock_articles()
