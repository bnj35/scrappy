from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.scrapper import scrape_hellowork_links, scrape_wttj_links, scrape_indeed_links, scrape_france_travail_links
from sqlalchemy.orm import Session
from app.db import SessionLocal, Job, Base, engine
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales pour stocker les données et l'état
job_data = {}
scraping_in_progress = False

def scrape_all_jobs():
    global job_data, scraping_in_progress
    scraping_in_progress = True
    try:
        job_data = {
            "hellowork": scrape_hellowork_links(),
            "wttj": scrape_wttj_links(),
            "indeed": scrape_indeed_links(),
            "france_travail": scrape_france_travail_links()
        }
        # Mettre à jour la base de données avec les données scrappées
        db = SessionLocal()
        update_jobs([job for source in job_data.values() for job in source], db)
    except Exception as e:
        print(f"Erreur lors du scraping : {e}")
    finally:
        scraping_in_progress = False

@app.get("/scrap-jobs")
async def get_jobs():
    # Retourne les données si le scraping est terminé
    if scraping_in_progress:
        return {"status": "in_progress", "jobs": None}
    return {"status": "completed", "jobs": job_data}


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import HTTPException

@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db)):
    try:
        jobs = db.query(Job).all()
        return {"jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

class JobData(BaseModel):
    source: str
    title: str
    company: Optional[str]
    location: Optional[str]
    contract: Optional[str]
    duration: Optional[str]
    date: Optional[str]
    offer_url: str

@app.post("/jobs")
def update_jobs(job_data: List[JobData], db: Session = Depends(get_db)):
    try:
        for job in job_data:
            existing_job = db.query(Job).filter(Job.source == job.source, Job.offer_url == job.offer_url).first()
            if existing_job:
                # Update existing job
                existing_job.title = job.title
                existing_job.company = job.company
                existing_job.location = job.location
                existing_job.contract = job.contract
                existing_job.duration = job.duration
                existing_job.date = job.date
                existing_job.updated_at = datetime.now()
            else:
                # Insert new job
                new_job = Job(
                    source=job.source,
                    title=job.title,
                    company=job.company,
                    location=job.location,
                    contract=job.contract,
                    duration=job.duration,
                    date=job.date,
                    offer_url=job.offer_url,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                db.add(new_job)
        db.commit()
        return {"message": "Jobs updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database update error: {e}")

@app.post("/start-scraping")
async def start_scraping(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    global scraping_in_progress

    # Check if scraping is already in progress
    if scraping_in_progress:
        return {"status": "already_in_progress"}

    # Define the scraping and database update logic
    def scrape_and_update():
        global scraping_in_progress
        scraping_in_progress = True  # Set scraping status to in progress
        try:
            scrape_all_jobs()  # Call scrape_all_jobs to perform scraping and update the database
        finally:
            scraping_in_progress = False  # Reset scraping status when done

    # Start the scraping process in the background
    background_tasks.add_task(scrape_and_update)
    return {"status": "started"}