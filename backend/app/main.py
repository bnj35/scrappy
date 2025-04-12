from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.scrapper import scrape_hellowork_links, scrape_wttj_links, scrape_indeed_links, scrape_france_travail_links
from playwright.sync_api import sync_playwright

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
async def get_jobs():
    # Combine les résultats des trois fonctions
    jobs = {
        "hellowork": scrape_hellowork_links(),
        "wttj": scrape_wttj_links(),
        "indeed": scrape_indeed_links(),
        "france_travail": scrape_france_travail_links()
    }
    return {"jobs": jobs}

    #test route#

# @app.get("/jobs")
# async def get_jobs():
#     return {"jobs": {"hellowork": ["https://example.com/job1"], "wttj": [], "indeed": []}}