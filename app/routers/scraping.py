from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tasks.worker import run_vietstock_scraper, add
from tasks.celery_app import celery_app
from celery.result import AsyncResult
from celery import states

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
    Return current state and (if available) progress/result for a Celery task.
    Never guesses NOT_FOUND based on raw backend reads.
    """
    task = AsyncResult(task_id, app=celery_app)
    state = task.state

    # Check if this task ID ever existed in backend
    if state == states.PENDING and task.backend.get(task.id) is None:
        return JSONResponse(
            status_code=404,
            content={"task_id": task_id, "status": "NOT_FOUND", "result": None}
        )

    if state == states.SUCCESS:
        return JSONResponse(
            status_code=200,
            content={"task_id": task_id, "status": "SUCCESS", "result": task.get()}
        )

    # FAILURE
    if state == states.FAILURE:
        # task.info is usually an Exception; str(...) makes it JSONable
        return JSONResponse(
            status_code=500,
            content={"task_id": task_id, "status": "FAILURE", "error": str(task.info)}
        )

    # PENDING / RECEIVED / STARTED / RETRY → still working
    payload = {
        "task_id": task_id,
        "status": state,
        "result": None
    }
    # If your task calls update_state with a dict, surface it as meta/progress
    if isinstance(task.info, dict):
        payload["meta"] = task.info

    # 202 = “in progress”
    return JSONResponse(status_code=202, content=payload)

@router.post("/debug/celery-test")
def celery_test(x: int = 5, y: int = 10):
    """
    Triggers a simple Celery task to test the connection.
    """
    task = add.delay(x, y)
    return JSONResponse({"task_id": task.id, "message": f"Task to add {x} + {y} started."})
