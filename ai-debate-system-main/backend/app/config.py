"""
Configuration Management with Ollama Support
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI Debate System"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # LLM Configuration - UPDATED FOR OLLAMA
    LLM_PROVIDER: str = "ollama"  # Options: "ollama", "openai", "anthropic"
    
    # Ollama Settings (FREE!)
    OLLAMA_URL: str = "http://localhost:11434"
    
    # OpenAI Settings (optional, only if using OpenAI)
    OPENAI_API_KEY: str = ""
    
    # Anthropic Settings (optional, only if using Anthropic)
    ANTHROPIC_API_KEY: str = ""
    
    # Model Selection based on provider
    LLM_MODEL: str = "llama3.2:3b"  # Ollama model
    # For OpenAI: "gpt-4-turbo-preview" or "gpt-3.5-turbo"
    # For Anthropic: "claude-3-sonnet-20240229"
    
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    
    # Embedding Model
    EMBEDDING_MODEL: str = "nomic-embed-text"  # For Ollama
    # For OpenAI: "text-embedding-ada-002"
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./data/vector_store"
    
    # Database
    DATABASE_URL: str = "sqlite:///./debate_system.db"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".docx", ".doc"]
    
    # Web Scraping
    SCRAPING_TIMEOUT: int = 30
    MAX_SCRAPE_PAGES: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()