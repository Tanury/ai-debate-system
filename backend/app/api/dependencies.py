"""
API Shared Dependencies -- > for FastAPI routes
"""

from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.security.auth import AuthService, verify_token
from app.security.rate_limiter import RateLimiter
from app.agents.agent_coordinator import AgentCoordinator
from app.services.llm_service import LLMService
from app.services.information_retrieval import InformationRetrieval
from app.services.web_scraper import WebScraper
from app.services.document_processor import DocumentProcessor
import logging

logger = logging.getLogger(__name__)

# Singleton instances
_coordinator = None
_llm_service = None
_ir_service = None
_web_scraper = None
_doc_processor = None
_rate_limiter = None

def get_coordinator() -> AgentCoordinator:
    """Get agent coordinator singleton"""
    global _coordinator
    if _coordinator is None:
        _coordinator = AgentCoordinator()
    return _coordinator

def get_llm_service() -> LLMService:
    """Get LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service

def get_ir_service() -> InformationRetrieval:
    """Get information retrieval service singleton"""
    global _ir_service
    if _ir_service is None:
        _ir_service = InformationRetrieval()
    return _ir_service

def get_web_scraper() -> WebScraper:
    """Get web scraper singleton"""
    global _web_scraper
    if _web_scraper is None:
        _web_scraper = WebScraper()
    return _web_scraper

def get_document_processor() -> DocumentProcessor:
    """Get document processor singleton"""
    global _doc_processor
    if _doc_processor is None:
        _doc_processor = DocumentProcessor()
    return _doc_processor

def get_rate_limiter() -> RateLimiter:
    """Get rate limiter singleton"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
    return _rate_limiter

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Verify API key for protected endpoints (optional)
    """
    if x_api_key is None:
        # For now, allow without API key (can be enforced later)
        return None
    
    # Add your API key verification logic here
    # For now, just log it
    logger.info(f"API key provided: {x_api_key[:10]}...")
    return x_api_key

async def get_current_user(token: Optional[str] = Header(None)):
    """
    Get current authenticated user from JWT token
    """
    if token is None:
        return None
    
    try:
        payload = verify_token(token)
        return payload
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None

async def require_authentication(token: str = Header(..., alias="Authorization")):
    """
    Require authentication for protected endpoints
    """
    if not token or not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = token.replace("Bearer ", "")
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return payload

async def check_rate_limit(
    client_id: str,
    rate_limiter: RateLimiter = Depends(get_rate_limiter)
):
    """
    Check rate limit for client
    """
    if not await rate_limiter.check_rate_limit(client_id):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    return True