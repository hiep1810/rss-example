from .celery_app import celery_app
from scrapers.vietstock import scrape_vietstock_articles
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@celery_app.task
def cleanup_file(file_path: str):
    """
    Celery task to delete a file.
    """
    try:
        os.remove(file_path)
        logging.info(f"Successfully deleted file: {file_path}")
    except OSError as e:
        logging.error(f"Error deleting file {file_path}: {e}")

@celery_app.task(bind=True)
def run_vietstock_scraper(self):
    """
    Celery task that runs the Vietstock article scraper and schedules a cleanup task.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Scraping started'})
    result = scrape_vietstock_articles()
    file_path = result.get("file_path")

    if file_path:
        # Schedule the cleanup task to run after the result expires
        cleanup_delay = self.app.conf.result_expires + 10  # Add a 10-second buffer
        cleanup_file.apply_async(args=[file_path], countdown=cleanup_delay)
        logging.info(f"Scheduled cleanup for {file_path} in {cleanup_delay} seconds.")

    return result

@celery_app.task
def add(x, y):
    """
    A simple debug task that adds two numbers.
    """
    return x + y
