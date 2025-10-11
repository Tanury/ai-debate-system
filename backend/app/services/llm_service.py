"""
LLM Service
Handles integration with OpenAI, Anthropic, and other LLM providers
"""

from typing import Optional, Dict, Any, List
import openai
from anthropic import Anthropic
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for LLM integration with multiple providers
    """
    
    def __init__(self):
        self.provider = settings.LLM_MODEL.split('-')[0] if '-' in settings.LLM_MODEL else 'openai'
        
        if self.provider == 'gpt' or self.provider == 'openai':
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == 'claude' or self.provider == 'anthropic':
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def generate(
        self, 
        prompt: str, 
        max_tokens: int = 500,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using the configured LLM
        """
        try:
            if self.provider in ['gpt', 'openai']:
                return await self._generate_openai(prompt, max_tokens, temperature, system_prompt)
            elif self.provider in ['claude', 'anthropic']:
                return await self._generate_anthropic(prompt, max_tokens, temperature, system_prompt)
            else:
                return await self._generate_fallback(prompt)
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "I apologize, but I'm having trouble generating a response right now."
    
    async def _generate_openai(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using OpenAI GPT models"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using Anthropic Claude models"""
        response = self.client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "You are a skilled debater.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_fallback(self, prompt: str) -> str:
        """Fallback generation for testing without API keys"""
        return f"[Simulated response to: {prompt[:100]}...]"
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            if self.provider in ['gpt', 'openai']:
                response = self.client.embeddings.create(
                    model=settings.EMBEDDING_MODEL,
                    input=text
                )
                return response.data[0].embedding
            else:
                # Fallback: simple hash-based embedding
                return [float(hash(text[i:i+10]) % 1000) / 1000 for i in range(0, min(len(text), 1000), 10)]
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return [0.0] * 1536  # Return zero vector