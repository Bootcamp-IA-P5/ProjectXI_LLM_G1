"""Tests for LLM Factory and Groq integration"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add backend to path so we can import from backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from llm.llm_factory import LLMFactory

# Check if we have a real API key for integration tests
HAS_GROQ_API_KEY = os.getenv("GROQ_API_KEY") is not None


# ============================================================================
# Unit Tests (using mocks - always run)
# ============================================================================

class TestLLMFactoryUnit:
    """Unit tests for LLM Factory using mocks"""
    
    def test_llm_factory_invalid_provider(self):
        """Test that LLM Factory raises error for invalid provider"""
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            LLMFactory.get_client(provider="invalid_provider")
    
    def test_llm_factory_missing_api_key(self, monkeypatch):
        """Test that LLM Factory raises error when API key is missing"""
        # Remove GROQ_API_KEY from environment
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="GROQ_API_KEY not configured"):
            LLMFactory.get_client(provider="groq")
    
    @patch('langchain_groq.ChatGroq')
    def test_llm_factory_creates_groq_client_with_correct_params(self, mock_chatgroq):
        """Test that LLM Factory creates Groq client with correct parameters"""
        # Setup
        mock_client = Mock()
        mock_chatgroq.return_value = mock_client
        test_api_key = "test_api_key_123"
        
        # Execute
        client = LLMFactory.get_client(
            provider="groq",
            api_key=test_api_key,
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=2048
        )
        
        # Verify
        assert client is not None
        mock_chatgroq.assert_called_once_with(
            api_key=test_api_key,
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=2048
        )
    
    @patch('langchain_groq.ChatGroq')
    def test_llm_factory_uses_default_groq_params(self, mock_chatgroq):
        """Test that LLM Factory uses default parameters when not specified"""
        # Setup
        mock_client = Mock()
        mock_chatgroq.return_value = mock_client
        test_api_key = "test_api_key_123"
        
        # Execute
        client = LLMFactory.get_client(provider="groq", api_key=test_api_key)
        
        # Verify
        assert client is not None
        mock_chatgroq.assert_called_once_with(
            api_key=test_api_key,
            model="mixtral-8x7b-32768",  # default model
            temperature=0.7,  # default temperature
            max_tokens=1024   # default max_tokens
        )
    
    @patch('langchain_groq.ChatGroq')
    def test_llm_factory_default_provider(self, mock_chatgroq, monkeypatch):
        """Test that LLM Factory uses default provider from environment"""
        # Setup
        mock_client = Mock()
        mock_chatgroq.return_value = mock_client
        test_api_key = "test_api_key_123"
        monkeypatch.setenv("LLM_PROVIDER", "groq")
        
        # Execute - no provider specified, should use env var
        client = LLMFactory.get_client(api_key=test_api_key)
        
        # Verify
        assert client is not None
        mock_chatgroq.assert_called_once()


# ============================================================================
# Integration Tests (require real API key - skip if not available)
# ============================================================================

@pytest.mark.skipif(not HAS_GROQ_API_KEY, reason="Requires GROQ_API_KEY")
class TestLLMFactoryIntegration:
    """Integration tests for LLM Factory with real API"""
    
    def test_llm_factory_groq_client_creation(self):
        """Test that LLM Factory can create a Groq client with real API key"""
        api_key = os.getenv("GROQ_API_KEY")
        
        try:
            client = LLMFactory.get_client(provider="groq", api_key=api_key)
            assert client is not None
        except Exception as e:
            pytest.fail(f"Failed to create Groq client: {e}")
    
    def test_llm_factory_groq_with_custom_model(self):
        """Test Groq client with custom model configuration"""
        api_key = os.getenv("GROQ_API_KEY")
        
        try:
            client = LLMFactory.get_client(
                provider="groq",
                api_key=api_key,
                model="llama3-8b-8192"
            )
            assert client is not None
        except Exception as e:
            pytest.fail(f"Failed to create Groq client with custom model: {e}")
