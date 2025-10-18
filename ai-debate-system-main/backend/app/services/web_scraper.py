"""
Web Scraper Service
Scrapes web content for debate topics with responsible AI practices
"""

from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from app.config import settings
from app.security.content_filter import ContentFilter
import logging
import asyncio

logger = logging.getLogger(__name__)

class WebScraper:
    """
    Web scraping service with content filtering and rate limiting
    """
    
    def __init__(self):
        self.timeout = settings.SCRAPING_TIMEOUT
        self.max_pages = settings.MAX_SCRAPE_PAGES
        self.content_filter = ContentFilter()
        self.headers = {
            'User-Agent': 'AI-Debate-System/1.0 (Educational Purpose)'
        }
    
    async def scrape_topic(
        self, 
        topic: str, 
        sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape web content related to debate topic
        """
        scraped_content = []
        
        # Default sources for educational content
        if not sources:
            sources = await self._generate_search_urls(topic)
        
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            tasks = []
            for url in sources[:self.max_pages]:
                tasks.append(self._scrape_url(client, url))
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict) and result.get("content"):
                    # Filter content for safety
                    if self.content_filter.is_safe(result["content"]):
                        scraped_content.append(result)
        
        logger.info(f"Scraped {len(scraped_content)} pages for topic: {topic}")
        return scraped_content
    
    async def _scrape_url(self, client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
        """Scrape a single URL"""
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "content": text[:5000],  # Limit content length
                "source": urlparse(url).netloc,
                "scrape_success": True
            }
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {"url": url, "error": str(e), "scrape_success": False}
    
    async def _generate_search_urls(self, topic: str) -> List[str]:
        """Generate search URLs for topic (simulated)"""
        # In production, integrate with search APIs or use predefined sources
        base_urls = [
            f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
            f"https://www.britannica.com/search?query={topic}",
        ]
        return base_urls
