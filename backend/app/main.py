from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.scrapper import scrape_hellowork_links, scrape_wttj_links, scrape_indeed_links, scrape_france_travail_links

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
    scraping_in_progress = True  # Indique que le scraping a commencé
    try:
        job_data = {
            "hellowork": scrape_hellowork_links(),
            "wttj": scrape_wttj_links(),
            "indeed": scrape_indeed_links(),
            "france_travail": scrape_france_travail_links()
        }
    finally:
        scraping_in_progress = False  # Indique que le scraping est terminé

@app.get("/jobs")
async def get_jobs():
    # Retourne les données si le scraping est terminé
    if scraping_in_progress:
        return {"status": "in_progress", "jobs": None}
    return {"status": "completed", "jobs": job_data}

@app.post("/start-scraping")
async def start_scraping(background_tasks: BackgroundTasks):
    # Démarre le scraping en arrière-plan
    if not scraping_in_progress:
        background_tasks.add_task(scrape_all_jobs)
        return {"status": "started"}
    return {"status": "already_in_progress"}