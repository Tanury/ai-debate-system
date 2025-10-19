"""
Agent Package
Contains all debate agents with MCP support
"""

from app.agents.base_agent import BaseAgent, AgentMessage
from app.agents.keyword_extractor import KeywordExtractorAgent
from app.agents.argument_generator import ArgumentGeneratorAgent
from app.agents.counter_argument import CounterArgumentAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.agents.agent_coordinator import AgentCoordinator

__all__ = [
    'BaseAgent',
    'AgentMessage',
    'KeywordExtractorAgent',
    'ArgumentGeneratorAgent',
    'CounterArgumentAgent',
    'EvaluationAgent',
    'AgentCoordinator'
]