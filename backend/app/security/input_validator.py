"""
Input Validation and Sanitization
Protects against injection attacks and malicious input
"""

import re
from typing import Any
import html
import logging

logger = logging.getLogger(__name__)

class InputValidator:
    """
    Validates and sanitizes user input
    """
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        
        # Limit length
        text = text[:max_length]
        
        # Remove potentially dangerous characters
        text = html.escape(text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def validate_topic(topic: str) -> bool:
        """Validate debate topic"""
        if not topic or len(topic) < 5:
            return False
        
        if len(topic) > 500:
            return False
        
        # Check for malicious patterns
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onclick='
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, topic, re.IGNORECASE):
                logger.warning(f"Dangerous pattern detected in topic: {pattern}")
                return False
        
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL"""
        if not url:
            return False
        
        # Basic URL validation
        url_pattern = r'^https?://'
        if not re.match(url_pattern, url):
            return False
        
        # Check for dangerous protocols
        dangerous_protocols = ['file://', 'ftp://', 'data:']
        for protocol in dangerous_protocols:
            if url.lower().startswith(protocol):
                return False
        
        return True
