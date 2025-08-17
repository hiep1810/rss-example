from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tasks.worker import run_vietstock_scraper, add
from tasks.celery_app import celery_app
from celery.result import AsyncResult

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
    Returns the structured result upon completion.
    """
    task_result = AsyncResult(task_id, app=celery_app)

    if not task_result.ready():
        # Task is not finished, could be PENDING, STARTED, etc.
        # We can also check if the task is unknown to the backend
        if task_result.backend.get(task_result.id) is None:
            return JSONResponse(
                status_code=404,
                content={"task_id": task_id, "status": "NOT_FOUND", "result": "Task ID not found."}
            )
        
        return JSONResponse({"task_id": task_id, "status": task_result.status, "result": None})

    if task_result.successful():
        result = task_result.get()
        return JSONResponse({"task_id": task_id, "status": "SUCCESS", "result": result})
    else:
        # Task failed
        return JSONResponse(
            status_code=500,
            content={"task_id": task_id, "status": "FAILURE", "result": str(task_result.info)}
        )

@router.post("/debug/celery-test")
def celery_test(x: int = 5, y: int = 10):
    """
    Triggers a simple Celery task to test the connection.
    """
    task = add.delay(x, y)
    return JSONResponse({"task_id": task.id, "message": f"Task to add {x} + {y} started."})
