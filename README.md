# Vietstock RSS Scraper

This project is a web scraper for fetching articles from `vietstock.vn` via its RSS feeds. It is built as a web application using FastAPI and Celery for background processing.

## Project Structure

- `app/`: Contains the FastAPI web application.
  - `main.py`: The entry point for the FastAPI application.
  - `routers/scraping.py`: Defines the API endpoints for starting and monitoring scraping tasks.
- `scrapers/`: Contains the core scraping logic.
  - `vietstock.py`: The module responsible for scraping articles from `vietstock.vn`.
- `tasks/`: Contains the Celery task definitions.
  - `worker.py`: Sets up Celery and defines the background task for running the scraper.
- `celeryconfig.py`: Configuration for Celery.
- `requirements.txt`: A list of the Python dependencies for the project.

## How to Set Up and Run the Project

### Prerequisites

- Python 3.8+
- Redis (or another message broker supported by Celery)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hiep1810/rss-example.git
   cd rss-example
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the message broker:**
   Make sure your Redis server is running.

2. **Start the Celery worker:**
   ```bash
   celery -A tasks.celery_app worker --loglevel=info
   ```

3. **Start the FastAPI application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /scrape/vietstock`: Starts a new scraping task.
- `GET /scrape/status/{task_id}`: Checks the status of a scraping task.

## Refactoring and Future Improvements

This project can be improved in several ways:

- **Eliminate Redundancy:** The root `main.py` script is redundant and should be removed. The web application provides a more robust way to run the scraper.
- **Configuration Management:** Hardcoded values (like the base URL for scraping) should be moved to a configuration file or managed through environment variables.
- **Logging:** The `print()` statements should be replaced with a structured logging library like Python's built-in `logging` module.
- **Data Storage:** Currently, the scraped data is saved to a CSV file. For a more scalable solution, consider using a database (e.g., SQLite, PostgreSQL, or a NoSQL database) to store the articles.
- **Error Handling:** The error handling can be improved to be more specific and provide better feedback when a task fails.
- **Dockerize the Application:** The project could be containerized using Docker to simplify the setup and deployment process.
