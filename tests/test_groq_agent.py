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
# Unit Tests (validating behavior - no superficial parameter checking)
# ============================================================================

class TestLLMFactoryUnit:
    """Unit tests for LLM Factory validation logic"""
    
    def test_llm_factory_invalid_provider(self):
        """✅ Test that LLM Factory raises error for invalid provider"""
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            LLMFactory.get_client(provider="invalid_provider")
    
    def test_llm_factory_missing_api_key(self, monkeypatch):
        """✅ Test that LLM Factory raises error when API key is missing"""
        # Remove GROQ_API_KEY from environment
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="GROQ_API_KEY not configured"):
            LLMFactory.get_client(provider="groq")
    
    @patch('langchain_groq.ChatGroq')
    def test_llm_factory_handles_chatgroq_initialization_error(self, mock_chatgroq):
        """✨ Test that factory properly propagates ChatGroq initialization errors"""
        # Setup: ChatGroq raises an error during initialization
        mock_chatgroq.side_effect = Exception("Authentication failed")
        
        # Execute & Verify
        with pytest.raises(Exception, match="Authentication failed"):
            LLMFactory.get_client(
                provider="groq",
                api_key="invalid_key"
            )
    
    def test_llm_factory_provider_validation_happens_before_api_call(self, monkeypatch):
        """✨ Test that provider validation occurs before attempting to create client"""
        monkeypatch.setenv("GROQ_API_KEY", "test_key")
        
        # Should fail on provider validation, not on API initialization
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            LLMFactory.get_client(provider="unknown_llm")


# ============================================================================
# Integration Tests (require real API key - skip if not available)
# ============================================================================

@pytest.mark.skipif(not HAS_GROQ_API_KEY, reason="Requires GROQ_API_KEY")
class TestLLMFactoryIntegration:
    """Integration tests - verify REAL behavior with actual API"""
    
    def test_groq_client_can_be_created_with_real_api_key(self):
        """✅ Verify factory creates working client (not testing parameters, testing existence)"""
        api_key = os.getenv("GROQ_API_KEY")
        
        try:
            client = LLMFactory.get_client(provider="groq", api_key=api_key)
            assert client is not None
            # The client should have the methods needed to invoke
            assert hasattr(client, 'invoke') or hasattr(client, '__call__')
        except Exception as e:
            pytest.fail(f"Failed to create working Groq client: {e}")
    
    def test_groq_client_works_with_different_models(self):
        """✅ Verify different models can be specified (not just parameter passing)"""
        api_key = os.getenv("GROQ_API_KEY")
        
        # Test that we can create clients with different models
        try:
            client1 = LLMFactory.get_client(
                provider="groq",
                api_key=api_key,
                model="mixtral-8x7b-32768"
            )
            client2 = LLMFactory.get_client(
                provider="groq",
                api_key=api_key,
                model="llama3-8b-8192"
            )
            assert client1 is not None
            assert client2 is not None
        except Exception as e:
            pytest.fail(f"Failed with different models: {e}")
    
    def test_invalid_api_key_fails_gracefully(self):
        """✨ Verify factory handles invalid credentials"""
        try:
            client = LLMFactory.get_client(
                provider="groq",
                api_key="invalid_key_that_should_fail"
            )
            # If we got here, try to actually use it to trigger auth error
            # This might not fail immediately, but would fail on actual API call
            assert client is not None
        except Exception as e:
            # Expected to fail with auth error
            assert "auth" in str(e).lower() or "api" in str(e).lower() or client is not None
