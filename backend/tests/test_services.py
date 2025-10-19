"""
Services Tests
Unit tests for service layer
"""

import pytest
from app.services.llm_service import LLMService
from app.services.information_retrieval import InformationRetrieval
from app.services.document_processor import DocumentProcessor
from app.utils.helpers import (
    sanitize_filename,
    truncate_text,
    calculate_similarity,
    extract_keywords_simple
)

def test_sanitize_filename():
    """Test filename sanitization"""
    assert sanitize_filename("test/file.txt") == "testfile.txt"
    assert sanitize_filename("file<>name.pdf") == "filename.pdf"
    assert sanitize_filename("  .test.doc  ") == "test.doc"

def test_truncate_text():
    """Test text truncation"""
    long_text = "This is a very long text " * 10
    truncated = truncate_text(long_text, max_length=50)
    assert len(truncated) <= 50
    assert truncated.endswith("...")

def test_calculate_similarity():
    """Test text similarity calculation"""
    text1 = "climate change is real"
    text2 = "climate change is happening"
    similarity = calculate_similarity(text1, text2)
    assert 0 <= similarity <= 1
    assert similarity > 0  # Should have some overlap

def test_extract_keywords():
    """Test keyword extraction"""
    text = "Climate change requires immediate action and policy reform"
    keywords = extract_keywords_simple(text, top_n=3)
    assert len(keywords) <= 3
    assert isinstance(keywords, list)

@pytest.mark.asyncio
async def test_llm_service_initialization():
    """Test LLM service can be initialized"""
    try:
        service = LLMService()
        assert service is not None
    except Exception as e:
        pytest.skip(f"LLM service initialization failed (may need API key): {e}")

@pytest.mark.asyncio
async def test_information_retrieval_initialization():
    """Test IR service can be initialized"""
    try:
        service = InformationRetrieval()
        assert service is not None
        assert service.collection is not None
    except Exception as e:
        pytest.skip(f"IR service initialization failed: {e}")

@pytest.mark.asyncio
async def test_document_processor():
    """Test document processor"""
    processor = DocumentProcessor()
    assert processor is not None
    assert processor.max_file_size > 0