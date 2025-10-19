"""
Debate API Routes
Main endpoints for debate functionality
"""

from fastapi import APIRouter, HTTPException, WebSocket, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.agents.agent_coordinator import AgentCoordinator
from app.security.input_validator import InputValidator
from app.security.rate_limiter import RateLimiter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
validator = InputValidator()
rate_limiter = RateLimiter()

class DebateRequest(BaseModel):
    topic: str
    initial_stance: Optional[str] = "supporting"

class ArgumentRequest(BaseModel):
    debate_id: str
    argument: str
    round_number: int

class DebateResponse(BaseModel):
    debate_id: str
    status: str
    message: str

@router.post("/start", response_model=DebateResponse)
async def start_debate(request: DebateRequest):
    """Start a new debate"""
    
    # Validate topic
    if not validator.validate_topic(request.topic):
        raise HTTPException(status_code=400, detail="Invalid topic")
    
    # Sanitize input
    topic = validator.sanitize_text(request.topic)
    
    # Generate debate ID
    import uuid
    debate_id = str(uuid.uuid4())
    
    logger.info(f"Starting new debate: {debate_id} on topic: {topic}")
    
    return DebateResponse(
        debate_id=debate_id,
        status="active",
        message=f"Debate started on: {topic}"
    )

@router.post("/argument")
async def submit_argument(request: ArgumentRequest, coordinator: AgentCoordinator = Depends()):
    """Submit an argument and get AI response"""
    
    # Validate and sanitize
    if not validator.sanitize_text(request.argument):
        raise HTTPException(status_code=400, detail="Invalid argument")
    
    # Check rate limit
    if not await rate_limiter.check_rate_limit(request.debate_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Process through coordinator
    result = await coordinator.process_debate_turn(
        debate_id=request.debate_id,
        user_argument=request.argument,
        context={"round": request.round_number}
    )
    
    return result

@router.get("/history/{debate_id}")
async def get_debate_history(debate_id: str, coordinator: AgentCoordinator = Depends()):
    """Get debate history"""
    history = coordinator.get_debate_history(debate_id)
    return {"debate_id": debate_id, "history": history}

@router.get("/agent-status")
async def get_agent_status(coordinator: AgentCoordinator = Depends()):
    """Get status of all agents"""
    return coordinator.get_all_agent_status()