import pytest
from app.security.input_validator import InputValidator
from app.security.content_filter import ContentFilter
from app.security.rate_limiter import RateLimiter

def test_sanitize_text():
    validator = InputValidator()
    
    # Test XSS protection
    dangerous_input = "<script>alert('XSS')</script>"
    safe_output = validator.sanitize_text(dangerous_input)
    assert "<script>" not in safe_output
    
    # Test length limiting
    long_text = "a" * 20000
    limited = validator.sanitize_text(long_text, max_length=1000)
    assert len(limited) <= 1000

def test_validate_topic():
    validator = InputValidator()
    
    # Valid topic
    assert validator.validate_topic("Climate change is real")
    
    # Too short
    assert not validator.validate_topic("Hi")
    
    # Dangerous pattern
    assert not validator.validate_topic("<script>alert('bad')</script>")

def test_validate_url():
    validator = InputValidator()
    
    assert validator.validate_url("https://example.com")
    assert validator.validate_url("http://example.com/page")
    assert not validator.validate_url("file:///etc/passwd")
    assert not validator.validate_url("javascript:alert('xss')")

def test_content_filter():
    filter = ContentFilter()
    
    safe_content = "This is a normal debate argument about economics."
    assert filter.is_safe(safe_content)
    
    filtered = filter.filter_content(safe_content)
    assert filtered == safe_content

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(max_requests=5, window_seconds=10)
    
    # First 5 requests should pass
    for i in range(5):
        assert await limiter.check_rate_limit("test_user")
    
    # 6th request should fail
    assert not await limiter.check_rate_limit("test_user")