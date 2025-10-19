"""
LLM Service with Ollama Support
Handles integration with Ollama (local), OpenAI, and Anthropic
"""

from typing import Optional, Dict, Any, List
import httpx
import json
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for LLM integration with multiple providers including Ollama
    """
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()  # 'ollama', 'openai', 'anthropic'
        self.ollama_url = settings.OLLAMA_URL
        self.model = settings.LLM_MODEL
        
        logger.info(f"LLM Service initialized with provider: {self.provider}, model: {self.model}")
        
        # Only import paid APIs if needed
        if self.provider == 'openai':
            import openai
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == 'anthropic':
            from anthropic import Anthropic
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        else:
            self.client = None  # Ollama uses HTTP requests
    
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
            if self.provider == 'ollama':
                return await self._generate_ollama(prompt, max_tokens, temperature, system_prompt)
            elif self.provider == 'openai':
                return await self._generate_openai(prompt, max_tokens, temperature, system_prompt)
            elif self.provider == 'anthropic':
                return await self._generate_anthropic(prompt, max_tokens, temperature, system_prompt)
            else:
                return await self._generate_fallback(prompt)
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return "I apologize, but I'm having trouble generating a response right now."
    
    async def _generate_ollama(
        self, 
        prompt: str, 
        max_tokens: int,
        temperature: float,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using Ollama (local, free!)"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
                
                # Add system prompt if provided
                if system_prompt:
                    payload["system"] = system_prompt
                
                response = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "")
                else:
                    logger.error(f"Ollama error: {response.status_code} - {response.text}")
                    return "Error generating response from Ollama."
                    
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return "Response generation timed out. Please try again."
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return f"Error: {str(e)}"
    
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
            model=self.model,
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
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "You are a skilled debater.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    async def _generate_fallback(self, prompt: str) -> str:
        """Fallback generation for testing without any LLM"""
        return f"[Simulated response to: {prompt[:100]}...]"
    
    async def embed(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        try:
            if self.provider == 'ollama':
                # Use Ollama's embedding endpoint
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.ollama_url}/api/embeddings",
                        json={
                            "model": "nomic-embed-text",  # Ollama embedding model
                            "prompt": text
                        }
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return result.get("embedding", [])
                    
            elif self.provider == 'openai':
                response = self.client.embeddings.create(
                    model=settings.EMBEDDING_MODEL,
                    input=text
                )
                return response.data[0].embedding
            
            # Fallback: simple hash-based embedding
            return [float(hash(text[i:i+10]) % 1000) / 1000 for i in range(0, min(len(text), 1000), 10)]
            
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return [0.0] * 768  # Return zero vector (smaller for Ollama)
