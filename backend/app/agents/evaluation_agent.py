"""
Evaluation Agent
Evaluates arguments and provides scoring based on multiple criteria
"""

from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class EvaluationAgent(BaseAgent):
    """
    Evaluates debate arguments and provides scores and feedback
    """
    
    def __init__(self, llm_service: LLMService):
        super().__init__(agent_id="evaluation_agent", name="Evaluation Agent")
        self.capabilities = ["argument_evaluation", "scoring", "feedback_generation"]
        self.llm_service = llm_service
        self.criteria = [
            "logical_coherence",
            "evidence_quality",
            "persuasiveness",
            "clarity",
            "relevance"
        ]
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate arguments from both sides
        """
        self.state = "processing"
        logger.info(f"{self.name} evaluating arguments")
        
        human_arg = input_data.get("human_argument", "")
        ai_arg = input_data.get("ai_argument", "")
        topic = input_data.get("topic", "")
        round_number = input_data.get("round", 1)
        
        # Evaluate both arguments
        human_scores = await self._evaluate_argument(human_arg, "human", topic)
        ai_scores = await self._evaluate_argument(ai_arg, "ai", topic)
        
        # Generate comparative feedback
        feedback = await self._generate_feedback(human_arg, ai_arg, human_scores, ai_scores)
        
        # Determine round winner
        winner = self._determine_winner(human_scores, ai_scores)
        
        result = {
            "human_scores": human_scores,
            "ai_scores": ai_scores,
            "feedback": feedback,
            "round_winner": winner,
            "round": round_number,
            "agent": self.agent_id
        }
        
        self.state = "idle"
        return result
    
    async def _evaluate_argument(self, argument: str, participant: str, topic: str) -> Dict[str, float]:
        """Evaluate a single argument across multiple criteria"""
        
        scores = {}
        
        # Logical Coherence
        scores['logical_coherence'] = self._score_logical_coherence(argument)
        
        # Evidence Quality
        scores['evidence_quality'] = self._score_evidence(argument)
        
        # Persuasiveness
        scores['persuasiveness'] = await self._score_persuasiveness(argument, topic)
        
        # Clarity
        scores['clarity'] = self._score_clarity(argument)
        
        # Relevance
        scores['relevance'] = self._score_relevance(argument, topic)
        
        # Calculate total
        scores['total'] = sum(scores.values()) / len(self.criteria)
        
        return scores
    
    def _score_logical_coherence(self, argument: str) -> float:
        """Score logical coherence (0-10)"""
        score = 5.0
        
        # Check for logical connectors
        logical_words = ['therefore', 'thus', 'hence', 'because', 'since', 'consequently']
        score += sum(1 for word in logical_words if word in argument.lower()) * 0.5
        
        # Check for contradictions
        contradiction_words = ['but', 'however', 'although']
        score += min(sum(1 for word in contradiction_words if word in argument.lower()) * 0.3, 1.5)
        
        return min(score, 10.0)
    
    def _score_evidence(self, argument: str) -> float:
        """Score evidence quality (0-10)"""
        score = 3.0
        
        evidence_words = ['research', 'study', 'data', 'evidence', 'statistics', 'findings', 'survey']
        score += sum(1 for word in evidence_words if word in argument.lower()) * 0.8
        
        # Check for citations or references
        if any(marker in argument for marker in ['(', 'according to', 'states that']):
            score += 2.0
            
        return min(score, 10.0)
    
    async def _score_persuasiveness(self, argument: str, topic: str) -> float:
        """Score persuasiveness using LLM (0-10)"""
        
        prompt = f"""Rate the persuasiveness of this argument on a scale of 0-10.

Topic: {topic}
Argument: {argument}

Consider:
- Emotional appeal
- Logical strength
- Use of examples
- Overall impact

Score (0-10):"""

        try:
            response = await self.llm_service.generate(
                prompt=prompt,
                max_tokens=10,
                temperature=0.3
            )
            score = float(response.strip().split()[0])
            return min(max(score, 0), 10)
        except:
            return 5.0
    
    def _score_clarity(self, argument: str) -> float:
        """Score clarity (0-10)"""
        score = 5.0
        
        # Check sentence length
        sentences = [s for s in argument.split('.') if s.strip()]
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if 15 <= avg_sentence_length <= 25:
            score += 2.0
        elif avg_sentence_length > 35:
            score -= 1.0
            
        # Check for clear structure
        if len(sentences) >= 3:
            score += 1.0
            
        return min(score, 10.0)
    
    def _score_relevance(self, argument: str, topic: str) -> float:
        """Score relevance to topic (0-10)"""
        score = 5.0
        
        topic_words = set(topic.lower().split())
        argument_words = set(argument.lower().split())
        
        overlap = len(topic_words & argument_words)
        score += overlap * 0.5
        
        return min(score, 10.0)
    
    async def _generate_feedback(
        self, 
        human_arg: str, 
        ai_arg: str, 
        human_scores: Dict[str, float],
        ai_scores: Dict[str, float]
    ) -> str:
        """Generate comparative feedback"""
        
        prompt = f"""Provide brief, constructive feedback on these debate arguments.

Human Argument:
{human_arg}
Score: {human_scores['total']:.1f}/10

AI Argument:
{ai_arg}
Score: {ai_scores['total']:.1f}/10

Provide 2-3 sentences of feedback highlighting strengths and areas for improvement:"""

        feedback = await self.llm_service.generate(
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        
        return feedback.strip()
    
    def _determine_winner(self, human_scores: Dict[str, float], ai_scores: Dict[str, float]) -> str:
        """Determine round winner"""
        if human_scores['total'] > ai_scores['total'] + 0.5:
            return "human"
        elif ai_scores['total'] > human_scores['total'] + 0.5:
            return "ai"
        else:
            return "tie"
