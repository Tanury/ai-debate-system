"""
FastAPI Application Entry Point
Implements the main API server with all routes and middleware
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
from typing import List
import logging

from app.config import settings
from app.api.routes import debate, documents, webscrape
from app.security.rate_imiter import RateLimiter
from app.security.auth import verify_token
from app.agents.agent_coordinator import AgentCoordinator
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    logger.info("Starting AI Debate System")
   
    # Initialize agent coordinator

    app.state.coordinator = AgentCoordinator()
    yield
    logger.info("Shutting down AI Debate System")

app = FastAPI(
    title = "AI Debate System",
    description = "Mutli-Agent AI Debate Platform with LLM Integration",
    version = "1.0.0",
    lifespan = lifespan
)

#security middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

#rate limiting
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

#Include Routers
app.include_router(debate.router, prefix="/api/v1/debate",tags=["debate"])
app.include_router(documents.router, prefix="/api/v1/documents",tags=["documents"])
app.include_router(webscrape.router, prefix="/api/v1/webscrape", tags=["scrape"])

@app.get("/")
async def root():
    return {
        "message": "AI Debate System API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": "active"}

#web socket for real-time debating
@app.websocket("/ws/debate/{debate_id}")
async def debate_websocket(websocket: WebSocket, debate_id: str):
    await websocket.accept()
    coordinator = app.state.coordinator

    try:
        while True:
            data = await websocket.receive_json()

            #process through agent coordinator
            result = await coordinator.process_debate_turn(
                debate_id = debate_id,
                user_argument=data.get("argument"),
                context=data.get("context",{})
            )

            await websocket.send_json(result)

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from debate {debate_id}")

        if __name__ == "__main__":
            uvicorn.run(
                "main.app",
                host="0.0.0.0",
                port=8000,
                reload=settings.DEBUG
            )