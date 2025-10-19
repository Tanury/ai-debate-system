"""
Rate Limiting
Prevents abuse and ensures fair usage
"""

from typing import Dict
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Token bucket rate limiter
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if request is within rate limit
        Returns True if allowed, False if rate limit exceeded
        """
        async with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds)
            
            # Remove old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                logger.warning(f"Rate limit exceeded for {identifier}")
                return False
            
            # Add current request
            self.requests[identifier].append(now)
            return True
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests for identifier"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)
        
        valid_requests = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]
        
        return max(0, self.max_requests - len(valid_requests))