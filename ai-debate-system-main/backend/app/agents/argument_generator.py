"""
Argument Generator Agent
Generates arguments based on retrieved information and keywords
"""

from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
from app.services.information_retrieval import InformationRetrieval
import logging

logger = logging.getLogger(__name__)

class ArgumentGeneratorAgent(BaseAgent):
    """
    Generates structured arguments using LLM and retrieved information
    """
    
    def __init__(self, llm_service: LLMService, ir_service: InformationRetrieval):
        super().__init__(agent_id="argument_generator", name="Argument Generator")
        self.capabilities = ["argument_generation", "evidence_synthesis", "logical_structuring"]
        self.llm_service = llm_service
        self.ir_service = ir_service
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an argument based on topic and keywords
        """
        self.state = "processing"
        logger.info(f"{self.name} generating argument")
        
        topic = input_data.get("topic", "")
        keywords = input_data.get("keywords", [])
        stance = input_data.get("stance", "supporting")
        context = input_data.get("context", {})
        
        # Retrieve relevant information
        retrieved_info = await self.ir_service.retrieve(
            query=topic,
            keywords=keywords,
            max_results=5
        )
        
        # Generate argument using LLM
        argument = await self._generate_argument_with_llm(
            topic=topic,
            keywords=keywords,
            stance=stance,
            evidence=retrieved_info,
            context=context
        )
        
        result = {
            "argument": argument,
            "evidence_used": retrieved_info,
            "structure": self._analyze_argument_structure(argument),
            "agent": self.agent_id
        }
        
        self.state = "idle"
        return result
    
    async def _generate_argument_with_llm(
        self, 
        topic: str, 
        keywords: List[str], 
        stance: str,
        evidence: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> str:
        """Generate argument using LLM"""
        
        # Construct evidence context
        evidence_text = "\n".join([
            f"- {item['content'][:200]}" 
            for item in evidence[:3]
        ]) if evidence else "No specific evidence available."
        
        prompt = f"""You are participating in a formal debate. Generate a strong, logical argument.

Topic: {topic}
Stance: {stance}
Key Concepts: {', '.join(keywords[:5])}

Relevant Evidence:
{evidence_text}

Generate a well-structured argument that:
1. Has a clear thesis statement
2. Provides logical reasoning
3. Uses evidence effectively
4. Addresses potential counterpoints
5. Is persuasive and coherent

Argument:"""

        argument = await self.llm_service.generate(
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        
        return argument.strip()
    
    def _analyze_argument_structure(self, argument: str) -> Dict[str, Any]:
        """Analyze the structure of generated argument"""
        sentences = [s.strip() for s in argument.split('.') if s.strip()]
        
        return {
            "sentence_count": len(sentences),
            "word_count": len(argument.split()),
            "has_evidence": any(word in argument.lower() for word in ['research', 'study', 'data', 'evidence']),
            "has_reasoning": any(word in argument.lower() for word in ['because', 'therefore', 'thus', 'hence'])
        }