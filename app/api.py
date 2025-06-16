from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.scraper import scrape_content
from app.ai_processor import spin_content, review_content
from app.storage import save_version, retrieve_version

app = FastAPI(title="Book Publication Workflow API")

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    """
    Scrape content from a URL and store it.
    """
    try:
        text = scrape_content(request.url)
        save_version("original", text, "original")
        return {"status": "success", "text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/spin")
async def spin():
    """
    Spin the scraped content using AI.
    """
    try:
        with open("data/content/chapter1.txt", "r", encoding="utf-8") as f:
            text = f.read()
        spun_text = spin_content(text)
        save_version("ai_spun", spun_text, "ai_spun")
        return {"status": "success", "text": spun_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review")
async def review():
    """
    Review the spun content and provide feedback.
    """
    try:
        with open("data/content/chapter1_spun.txt", "r", encoding="utf-8") as f:
            text = f.read()
        reviewed_text, review_note = review_content(text)
        save_version("ai_reviewed", reviewed_text, "ai_reviewed")
        return {"status": "success", "text": reviewed_text, "review": review_note}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/versions")
async def get_versions():
    """
    Retrieve all stored versions.
    """
    try:
        versions = retrieve_version(all_versions=True)
        return {"status": "success", "versions": versions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))