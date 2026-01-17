"""Tests for LLM Factory and Groq integration"""

import pytest
import sys
import os

# Add backend to path so we can import from backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from llm.llm_factory import LLMFactory


@pytest.fixture
def test_api_key():
    """Fixture for test API key"""
    return os.getenv("GROQ_API_KEY", "test_key")


def test_llm_factory_groq_client_creation(test_api_key):
    """Test that LLM Factory can create a Groq client"""
    if test_api_key == "test_key":
        pytest.skip("No real GROQ_API_KEY available, skipping integration test")
    
    try:
        client = LLMFactory.get_client(provider="groq", api_key=test_api_key)
        assert client is not None
    except Exception as e:
        pytest.fail(f"Failed to create Groq client: {e}")


def test_llm_factory_invalid_provider():
    """Test that LLM Factory raises error for invalid provider"""
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        LLMFactory.get_client(provider="invalid_provider")


def test_llm_factory_missing_api_key():
    """Test that LLM Factory raises error when API key is missing"""
    # Clear environment variable temporarily
    original_key = os.environ.pop("GROQ_API_KEY", None)
    
    try:
        with pytest.raises(ValueError, match="GROQ_API_KEY not configured"):
            LLMFactory.get_client(provider="groq")
    finally:
        # Restore original key if it existed
        if original_key:
            os.environ["GROQ_API_KEY"] = original_key


def test_llm_factory_default_provider(test_api_key):
    """Test that LLM Factory uses default provider from environment"""
    if test_api_key == "test_key":
        pytest.skip("No real GROQ_API_KEY available, skipping integration test")
    
    # Set default provider
    os.environ["LLM_PROVIDER"] = "groq"
    
    try:
        client = LLMFactory.get_client(api_key=test_api_key)
        assert client is not None
    except Exception as e:
        pytest.fail(f"Failed to create default client: {e}")


def test_llm_factory_groq_with_custom_model(test_api_key):
    """Test Groq client with custom model configuration"""
    if test_api_key == "test_key":
        pytest.skip("No real GROQ_API_KEY available, skipping integration test")
    
    try:
        client = LLMFactory.get_client(
            provider="groq",
            api_key=test_api_key,
            model="llama3-8b-8192"
        )
        assert client is not None
    except Exception as e:
        pytest.fail(f"Failed to create Groq client with custom model: {e}")
