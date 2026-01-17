"""
Factory pattern for LLM client instantiation.
Provides centralized creation and configuration of LLM clients.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory for creating and managing LLM clients"""
    
    _clients = {}
    
    @staticmethod
    def get_client(provider: str = None, **kwargs):
        """
        Get an LLM client instance based on provider.
        
        Args:
            provider: LLM provider name ('groq', 'gemini', 'ollama')
                     If None, uses LLM_PROVIDER from environment
            **kwargs: Additional arguments to pass to client
        
        Returns:
            Configured LLM client instance
            
        Raises:
            ValueError: If provider not found or configuration invalid
        """
        provider = provider or os.getenv("LLM_PROVIDER", "groq").lower()
        
        if provider == "groq":
            return LLMFactory._get_groq_client(**kwargs)
        elif provider == "gemini":
            return LLMFactory._get_gemini_client(**kwargs)
        elif provider == "ollama":
            return LLMFactory._get_ollama_client(**kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    @staticmethod
    def _get_groq_client(**kwargs):
        """Initialize and return a Groq client"""
        from langchain_groq import ChatGroq
        
        api_key = kwargs.get("api_key") or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not configured in environment variables")
        
        model = kwargs.get("model", "mixtral-8x7b-32768")
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 1024)
        
        logger.info(f"Creating Groq client with model: {model}")
        
        return ChatGroq(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    @staticmethod
    def _get_gemini_client(**kwargs):
        """Initialize and return a Google Gemini client"""
        import google.generativeai as genai
        
        api_key = kwargs.get("api_key") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured in environment variables")
        
        model = kwargs.get("model", "gemini-pro")
        
        logger.info(f"Creating Gemini client with model: {model}")
        
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(model)
    
    @staticmethod
    def _get_ollama_client(**kwargs):
        """Initialize and return an Ollama client"""
        from llm.ollama_client import OllamaClient
        
        base_url = kwargs.get("base_url") or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = kwargs.get("model", "mistral")
        
        logger.info(f"Creating Ollama client with model: {model}")
        
        return OllamaClient(base_url=base_url, model=model)
    
    @staticmethod
    def get_model_name(provider: str = None) -> str:
        """
        Get the default model name for a provider.
        
        Args:
            provider: LLM provider name
        
        Returns:
            Default model name for the provider
        """
        provider = provider or os.getenv("LLM_PROVIDER", "groq").lower()
        
        models = {
            "groq": "mixtral-8x7b-32768",
            "gemini": "gemini-pro",
            "ollama": "mistral"
        }
        
        return models.get(provider, "unknown")


# Backward compatibility - simple functions
def get_llm_client(provider: str = None, **kwargs):
    """
    Get LLM client (wrapper for LLMFactory.get_client).
    
    Args:
        provider: LLM provider name
        **kwargs: Additional configuration
    
    Returns:
        Configured LLM client
    """
    return LLMFactory.get_client(provider, **kwargs)


def get_model_name(provider: str = None) -> str:
    """
    Get model name for provider (wrapper for LLMFactory.get_model_name).
    
    Args:
        provider: LLM provider name
    
    Returns:
        Model name
    """
    return LLMFactory.get_model_name(provider)