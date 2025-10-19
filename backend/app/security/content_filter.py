"""
Content Moderation and Filtering
Implements responsible AI practices
"""

from typing import List
import re
import logging

logger = logging.getLogger(__name__)

class ContentFilter:
    """
    Filters inappropriate and harmful content
    """
    
    def __init__(self):
        # Inappropriate content patterns
        self.blocked_patterns = [
            r'\b(violence|harmful|illegal)\b',
            # Add more patterns as needed
        ]
        
        # Topics requiring extra caution
        self.sensitive_topics = [
            'suicide', 'self-harm', 'terrorism', 'illegal drugs',
            'weapon making', 'hacking', 'fraud'
        ]
    
    def is_safe(self, content: str) -> bool:
        """Check if content is safe"""
        content_lower = content.lower()
        
        # Check for explicitly blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, content_lower):
                logger.warning(f"Blocked pattern found: {pattern}")
                return False
        
        # Check for sensitive topics (log but allow with warning)
        for topic in self.sensitive_topics:
            if topic in content_lower:
                logger.info(f"Sensitive topic detected: {topic}")
        
        return True
    
    def filter_content(self, content: str) -> str:
        """Filter and sanitize content"""
        if not self.is_safe(content):
            return "[Content filtered for safety]"
        
        return content