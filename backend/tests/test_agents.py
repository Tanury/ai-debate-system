
import pytest
from app.agents.keyword_extractor import KeywordExtractorAgent
from app.agents.argument_generator import ArgumentGeneratorAgent
from app.agents.counter_argument import CounterArgumentAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.services.llm_service import LLMService
from app.services.information_retrieval import InformationRetrieval

@pytest.fixture
def keyword_agent():
    return KeywordExtractorAgent()

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def ir_service():
    return InformationRetrieval()

@pytest.mark.asyncio
async def test_keyword_extraction(keyword_agent):
    input_data = {
        "text": "Climate change is a significant global challenge that requires immediate action.",
        "max_keywords": 5
    }
    
    result = await keyword_agent.process(input_data)
    
    assert "keywords" in result
    assert len(result["keywords"]) <= 5
    assert result["agent"] == "keyword_extractor"

@pytest.mark.asyncio
async def test_argument_generator(llm_service, ir_service):
    agent = ArgumentGeneratorAgent(llm_service, ir_service)
    
    input_data = {
        "topic": "Renewable energy is essential",
        "keywords": ["climate", "energy", "renewable"],
        "stance": "supporting"
    }
    
    result = await agent.process(input_data)
    
    assert "argument" in result
    assert len(result["argument"]) > 0
    assert "structure" in result

@pytest.mark.asyncio
async def test_counter_argument(llm_service):
    agent = CounterArgumentAgent(llm_service)
    
    input_data = {
        "opponent_argument": "Renewable energy is too expensive to implement.",
        "topic": "Renewable energy",
        "keywords": ["cost", "renewable", "energy"]
    }
    
    result = await agent.process(input_data)
    
    assert "counter_argument" in result
    assert len(result["counter_argument"]) > 0
    assert "identified_weaknesses" in result

@pytest.mark.asyncio
async def test_evaluation_agent(llm_service):
    agent = EvaluationAgent(llm_service)
    
    input_data = {
        "human_argument": "Renewable energy reduces carbon emissions significantly.",
        "ai_argument": "However, the initial investment costs are prohibitive.",
        "topic": "Renewable energy"
    }
    
    result = await agent.process(input_data)
    
    assert "human_scores" in result
    assert "ai_scores" in result
    assert "round_winner" in result
    assert result["round_winner"] in ["human", "ai", "tie"]
