"""
Agent Coordinator
Implements Model Context Protocol (MCP) for multi-agent coordination
"""

from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent, AgentMessage
from app.agents.keyword_extractor import KeywordExtractorAgent
from app.agents.argument_generator import ArgumentGeneratorAgent
from app.agents.counter_argument import CounterArgumentAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.services.llm_service import LLMService
from app.services.information_retrieval import InformationRetrieval
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class AgentCoordinator:
    """
    Coordinates communication between agents using MCP
    Manages the debate workflow
    """
    
    def __init__(self):
        # Initialize services
        self.llm_service = LLMService()
        self.ir_service = InformationRetrieval()
        
        # Initialize agents
        self.agents: Dict[str, BaseAgent] = {
            "keyword_extractor": KeywordExtractorAgent(),
            "argument_generator": ArgumentGeneratorAgent(self.llm_service, self.ir_service),
            "counter_argument": CounterArgumentAgent(self.llm_service),
            "evaluation_agent": EvaluationAgent(self.llm_service)
        }
        
        self.debate_history: Dict[str, List[Dict[str, Any]]] = {}
        
    async def process_debate_turn(
        self, 
        debate_id: str,
        user_argument: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a complete debate turn through all agents
        """
        correlation_id = str(uuid.uuid4())
        topic = context.get("topic", "")

        debate_history = self.debate_history.get(debate_id, [])
        round_number = len(debate_history) + 1
        
        logger.info(f"Processing debate turn {round_number} for {debate_id}")
        
        # Step 1: Extract keywords from user argument
        keyword_message = AgentMessage(
            sender="coordinator",
            receiver="keyword_extractor",
            message_type="process_request",
            content={"text": user_argument, "max_keywords": 10},
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        keyword_response = await self.agents["keyword_extractor"].receive_message(keyword_message)
        keywords = keyword_response.content.get("keywords", [])
        
        # Step 2: Generate AI counter-argument with debate historry
        counter_message = AgentMessage(
            sender="coordinator",
            receiver="counter_argument",
            message_type="process_request",
            content={
                "opponent_argument": user_argument,
                "topic": topic,
                "keywords": keywords,
                "context": context,
                "debate_history": debate_history,
                "round_number": round_number
            },
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        counter_response = await self.agents["counter_argument"].receive_message(counter_message)
        ai_argument = counter_response.content.get("counter_argument", "")
        
        # Step 3: Evaluate both arguments
        eval_message = AgentMessage(
            sender="coordinator",
            receiver="evaluation_agent",
            message_type="process_request",
            content={
                "human_argument": user_argument,
                "ai_argument": ai_argument,
                "topic": topic,
                "round": round_number
            },
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        eval_response = await self.agents["evaluation_agent"].receive_message(eval_message)
        
        # Store in history
        turn_data = {
            "round_number": round_number,
            "human_argument": user_argument,
            "ai_argument": ai_argument,
            "keywords": keywords,
            "evaluation": eval_response.content,
            "timestamp": datetime.now().isoformat()
        }
        
        if debate_id not in self.debate_history:
            self.debate_history[debate_id] = []
        self.debate_history[debate_id].append(turn_data)
        
        # Prepare response
        return {
            "ai_argument": ai_argument,
            "keywords": keywords,
            "evaluation": eval_response.content,
            "round": round_number,
            "total_rounds": len(self.debate_history[debate_id]),
            "debate_context": {
                "previous_rounds": round_number - 1,
                "cumulative_scores": self._calculate_cumulative_scores(debate_id)
            },
            "agent_status": self.get_all_agent_status()
        }
    
    def _calculate_cumulative_scores(self, debate_id: str) -> Dict[str, float]:
        """Calculate cumulative scores across all rounds"""
        history = self.debate_history.get(debate_id, [])
        
        total_human = 0
        total_ai = 0
        
        for round_data in history:
            eval_data = round_data.get("evaluation", {})
            human_scores = eval_data.get("human_scores", {})
            ai_scores = eval_data.get("ai_scores", {})
            
            total_human += human_scores.get("total", 0)
            total_ai += ai_scores.get("total", 0)
        
        return {
            "human_total": total_human,
            "ai_total": total_ai,
            "rounds": len(history),
            "human_average": total_human / len(history) if history else 0,
            "ai_average": total_ai / len(history) if history else 0
        }
    
    def get_all_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            agent_id: agent.get_status()
            for agent_id, agent in self.agents.items()
        }
    
    def get_debate_history(self, debate_id: str) -> List[Dict[str, Any]]:
        """Retrieve debate history"""
        return self.debate_history.get(debate_id, [])
