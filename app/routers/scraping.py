from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tasks.worker import run_vietstock_scraper, celery_app
from tasks.worker import celery_app

router = APIRouter()

@router.post("/scrape/vietstock")
def start_vietstock_scrape():
    """
    Starts the Vietstock scraping task in the background.
    """
    task = run_vietstock_scraper.delay()
    return JSONResponse({"task_id": task.id})

@router.get("/scrape/status/{task_id}")
def get_scrape_status(task_id: str):
    """
    Checks the status of a scraping task.
    """
    task_result = celery_app.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return JSONResponse(result)
