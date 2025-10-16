"""
API Package
FastAPI routes and endpoints
"""

from app.api.routes import debate, documents, webscrape

__all__ = ['debate', 'documents', 'webscrape']