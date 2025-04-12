from fastapi import FastAPI
from app.scraper import scrape_jobs

app = FastAPI()

@app.get("/jobs")
async def get_jobs():
    jobs = await scrape_jobs()
    return {"jobs": jobs}
