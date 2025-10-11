"""
Counter-Argument Generator Agent
Generates counter-arguments by identifying weaknesses and providing rebuttals
"""

from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class CounterArgumentAgent(BaseAgent):
    """
    Generates counter-arguments and rebuttals
    """
    
    def __init__(self, llm_service: LLMService):
        super().__init__(agent_id="counter_argument", name="Counter-Argument Generator")
        self.capabilities = ["counter_argument_generation", "weakness_identification", "rebuttal_creation"]
        self.llm_service = llm_service
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate counter-argument to opponent's argument
        """
        self.state = "processing"
        logger.info(f"{self.name} generating counter-argument")
        
        opponent_argument = input_data.get("opponent_argument", "")
        topic = input_data.get("topic", "")
        keywords = input_data.get("keywords", [])
        context = input_data.get("context", {})
        #new
        debate_history = input_data.get("debate_history", [])
        round_number = input_data.get("round",1)
        
        # Identify weaknesses
        weaknesses = await self._identify_weaknesses(opponent_argument)
        
        # Generate counter-argument
        counter_arg = await self._generate_counter_with_llm(
            opponent_argument=opponent_argument,
            topic=topic,
            keywords=keywords,
            weaknesses=weaknesses,
            context=context,
            debate_history=debate_history,
            round_number=round_number
        )
        
        result = {
            "counter_argument": counter_arg,
            "identified_weaknesses": weaknesses,
            "strategy": self._determine_strategy(counter_arg),
            "round": round_number,
            "agent": self.agent_id
        }
        
        self.state = "idle"
        #return result = "idle"
        return result
    
    
    async def _identify_weaknesses(self, argument: str) -> List[str]:
        """Identify logical weaknesses in opponent's argument"""
        
        prompt = f"""Analyze the following argument and identify its weaknesses:

Argument: {argument}

List specific weaknesses such as:
- Logical fallacies
- Unsupported claims
- Missing evidence
- Oversimplifications
- Contradictions

For each weakness, provide a SPECIFIC critique (not generic statements). Examples:
- "Fails to account for economic impact on developing nations"
- "Relies on outdated 2015 data; recent 2023 studies show opposite trend"
- "Assumes technological solutions exist at scale, which they don't"

Weaknesses (list 2-3 key ones):"""
        

        response = await self.llm_service.generate(
            prompt=prompt,
            max_tokens=250,
            temperature=0.7
        )
        
        weaknesses = [w.strip() for w in response.split('\n') if w.strip() and len(w.strip()) > 20]#not w.strip().startswith('Weaknesses')]
        return weaknesses[:3]
    
    async def _generate_counter_with_llm(
        self,
        opponent_argument: str,
        topic: str,
        keywords: List[str],
        weaknesses: List[str],
        context: Dict[str, Any],
        debate_history: List[Dict[str, Any]] = None,
        round_number: int=1
    ) -> str:
        """Generate counter-argument using LLM with debate history context"""
        
        #weaknesses_text = "\n".join([f"- {w}" for w in weaknesses]) if weaknesses else "General counterpoints"
        
        #prompt = f"""You are in a debate. Generate a strong counter-argument to the opponent's position.

        # Build context from debate history
        history_context = ""
        if debate_history and len(debate_history) > 0:
            history_context = "\n\nPrevious rounds of this debate:\n"
            for i, round_data in enumerate(debate_history, 1):
                human_arg = round_data.get("human_argument", "")
                ai_arg = round_data.get("ai_argument", "")
                history_context += f"\nRound {i}:\n"
                history_context += f"Human: {human_arg[:200]}...\n"
                history_context += f"You (AI): {ai_arg[:200]}...\n"
        
        # Craft round-specific instructions
        if round_number == 1:
            round_instruction = "This is the opening round. Present your main counter-argument with strong foundational points."
        elif round_number == 2:
            round_instruction = "This is round 2. Address their rebuttal directly and reinforce your position with new evidence or angles."
        else:
            round_instruction = f"This is round {round_number}. Synthesize previous arguments, address unresolved contradictions, and strengthen your case."
        
        prompt = f"""You are an expert debater in round {round_number} of a formal debate. You must present the OPPOSING viewpoint with context from previous rounds.

Topic: {topic}
{round_instruction}

{history_context}

Opponent's Latest Argument (Round {round_number}):
"{opponent_argument}"

Identified Weaknesses:
{chr(10).join([f"- {w}" for w in weaknesses]) if weaknesses else "- General logical gaps"}

Your task: Generate a counter-argument that:
1. DIRECTLY RESPONDS to their latest points (don't just repeat your previous arguments)
2. References or builds upon what was said in previous rounds if applicable
3. Takes the opposite stance with 2-3 NEW specific reasons
4. Includes concrete examples, data, or cases (name countries, studies, statistics)
5. Addresses their strongest point before attacking weaknesses
6. Shows how your position is stronger after {round_number} round(s) of debate

CRITICAL: Your response must acknowledge what they just said and explain why it's wrong, not just state your position again.

Your Counter-Argument (4-6 sentences with specific details):"""

        counter_arg = await self.llm_service.generate(
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            system_prompt=f"You are a skilled debater in round {round_number}. Build upon previous rounds and directly engage with opponent's arguments. Never repeat yourself - each round should introduce new angles and evidence."
        )
        
        return counter_arg.strip()
    
    def _determine_strategy(self, counter_arg: str) -> str:
        """Determine the strategy used in counter-argument"""
        counter_lower = counter_arg.lower()
        
        strategies = []
        if any(word in counter_lower for word in ['however', 'although', 'while']):
            strategies.append("concession_refutation")
        if any(word in counter_lower for word in ['evidence', 'research', 'data']):
            strategies.append("evidence_based")
        if any(word in counter_lower for word in ['logic', 'reasoning', 'fallacy']):
            strategies.append("logical_analysis")
            
        return ", ".join(strategies) if strategies else "direct_rebuttal"