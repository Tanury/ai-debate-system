"""
Web Scraping Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.services.web_scraper import WebScraper
from app.services.information_retrieval import InformationRetrieval
from app.security.input_validator import InputValidator
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
validator = InputValidator()

class ScrapeRequest(BaseModel):
    topic: str
    urls: Optional[List[str]] = None

@router.post("/scrape")
async def scrape_topic(
    request: ScrapeRequest,
    scraper: WebScraper = Depends(),
    ir_service: InformationRetrieval = Depends()
):
    """Scrape web content for debate topic"""
    
    # Validate topic
    if not validator.validate_topic(request.topic):
        raise HTTPException(status_code=400, detail="Invalid topic")
    
    # Validate URLs if provided
    if request.urls:
        for url in request.urls:
            if not validator.validate_url(url):
                raise HTTPException(status_code=400, detail=f"Invalid URL: {url}")
    
    # Scrape content
    scraped_content = await scraper.scrape_topic(request.topic, request.urls)
    
    # Add to vector store
    if scraped_content:
        documents = [{
            "content": item["content"],
            "metadata": {
                "url": item["url"],
                "source": item.get("source", ""),
                "title": item.get("title", "")
            }
        } for item in scraped_content if item.get("scrape_success")]
        
        await ir_service.add_documents(documents)
    
    return {
        "topic": request.topic,
        "pages_scraped": len(scraped_content),
        "successful": sum(1 for item in scraped_content if item.get("scrape_success")),
        "results": scraped_content
    }
