"""
API Tests
Integration tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "AI Debate System API"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_start_debate():
    """Test starting a debate"""
    response = client.post(
        "/api/v1/debate/start",
        json={
            "topic": "Climate change requires immediate action",
            "initial_stance": "supporting"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "debate_id" in data
    assert data["status"] == "active"

@pytest.mark.asyncio
async def test_submit_argument():
    """Test submitting an argument"""
    # First start a debate
    start_response = client.post(
        "/api/v1/debate/start",
        json={"topic": "Test topic"}
    )
    debate_id = start_response.json()["debate_id"]
    
    # Submit argument
    response = client.post(
        "/api/v1/debate/argument",
        json={
            "debate_id": debate_id,
            "argument": "This is my test argument",
            "round_number": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "ai_argument" in data
    assert "evaluation" in data

def test_agent_status():
    """Test agent status endpoint"""
    response = client.get("/api/v1/debate/agent-status")
    assert response.status_code == 200
    data = response.json()
    assert "keyword_extractor" in data
    assert "argument_generator" in data

@pytest.mark.asyncio
async def test_invalid_topic():
    """Test with invalid topic"""
    response = client.post(
        "/api/v1/debate/start",
        json={"topic": ""}
    )
    assert response.status_code == 400
