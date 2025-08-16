from fastapi import FastAPI
from .routers import scraping

app = FastAPI()

app.include_router(scraping.router)

@app.get("/")
def read_root():
    return {"message": "Scraping API is running"}
