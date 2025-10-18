"""
Helper Utilities
Common utility functions used across the application
"""

import uuid
import re
from datetime import datetime
from typing import List, Optional
import hashlib

def generate_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove dangerous characters
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove path separators and dangerous characters
    filename = re.sub(r'[/\\:*?"<>|]', '', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:250] + ('.' + ext if ext else '')
    return filename

def format_timestamp(dt: datetime = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime to string
    
    Args:
        dt: Datetime object (default: now)
        format_str: Format string
        
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_str)

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to specified length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity score between two texts
    Uses word overlap as a basic metric
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union) if union else 0.0

def hash_text(text: str) -> str:
    """
    Generate hash of text for deduplication
    
    Args:
        text: Text to hash
        
    Returns:
        SHA256 hash string
    """
    return hashlib.sha256(text.encode()).hexdigest()

def extract_keywords_simple(text: str, top_n: int = 5) -> List[str]:
    """
    Simple keyword extraction using word frequency
    
    Args:
        text: Input text
        top_n: Number of top keywords to return
        
    Returns:
        List of keywords
    """
    # Remove punctuation and convert to lowercase
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'said'}
    words = [w for w in words if w not in stop_words]
    
    # Count frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top N
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:top_n]]

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

def clean_whitespace(text: str) -> str:
    """
    Clean excessive whitespace from text
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with double newline
    text = re.sub(r'\n+', '\n\n', text)
    return text.strip()
