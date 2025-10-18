"""
Keyword Extractor Agent 
extracts key terms, entities and concepts from arguments
Uses NLP techniques -> TF-IDF, Named Entity Recognition
"""

from typing import Dict, Any, List
from collections import Counter
import re
from app.agents.base_agent import BaseAgent
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

logger = logging.getLogger(__name__)

class KeywordExtractorAgent(BaseAgent):
    """
    Agent responsible for extracting keywords and key concepts
    """
    
    def __init__(self):
        super().__init__(agent_id="keyword_extractor", name="Keyword Extractor")
        self.capabilities = ["keyword_extraction", "entity_recognition", "concept_identification"]
        self.stop_words = set(stopwords.words('english'))
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract keywords from input text
        """
        self.state = "processing"
        logger.info(f"{self.name} processing input")
        
        text = input_data.get("text", "")
        max_keywords = input_data.get("max_keywords", 10)
        
        # Extract keywords using multiple methods
        keywords_tfidf = self._extract_tfidf_keywords(text, max_keywords)
        keywords_frequency = self._extract_frequency_keywords(text, max_keywords)
        entities = self._extract_entities(text)
        
        # Combine and rank
        combined_keywords = self._combine_keywords(
            keywords_tfidf, 
            keywords_frequency, 
            entities
        )
        
        result = {
            "keywords": combined_keywords[:max_keywords],
            "entities": entities,
            "keyword_count": len(combined_keywords),
            "agent": self.agent_id
        }
        
        self.state = "idle"
        return result
    
    def _extract_tfidf_keywords(self, text: str, max_keywords: int) -> List[str]:
        """Extract keywords using TF-IDF approach"""
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words and len(w) > 3]
        
        # Simple frequency-based scoring (TF component)
        word_freq = Counter(words)
        return [word for word, _ in word_freq.most_common(max_keywords)]
    
    def _extract_frequency_keywords(self, text: str, max_keywords: int) -> List[str]:
        """Extract keywords based on frequency"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        words = [w for w in words if w not in self.stop_words]
        
        word_freq = Counter(words)
        return [word for word, _ in word_freq.most_common(max_keywords)]
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities"""
        # Simple entity extraction (can be enhanced with spaCy or transformers)
        entities = []
        
        # Capitalized words (potential entities)
        potential_entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        for entity in set(potential_entities):
            entities.append({
                "text": entity,
                "type": "ENTITY"
            })
        
        return entities
    
    def _combine_keywords(self, *keyword_lists) -> List[str]:
        """Combine multiple keyword lists with ranking"""
        keyword_scores = Counter()
        
        for keywords in keyword_lists:
            if isinstance(keywords, list) and keywords:
                for i, keyword in enumerate(keywords):
                    if isinstance(keyword, dict):
                        keyword = keyword.get('text', '')
                    score = len(keywords) - i
                    keyword_scores[keyword.lower()] += score
        
        return [kw for kw, _ in keyword_scores.most_common()]