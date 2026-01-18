"""Groq API Client"""
import logging
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)


class GroqClient:
    """Client for Groq API using LangChain"""
    
    def __init__(self, api_key: str):
        """Initialize Groq client
        
        Args:
            api_key: Groq API key
        """
        self.api_key = api_key
        self.model = ChatGroq(
            temperature=0.7,
            model_name="mixtral-8x7b-32768",
            api_key=api_key
        )
        logger.info("GroqClient initialized with mixtral-8x7b-32768")
    
    def generate(self, prompt: str) -> str:
        """Generate text using Groq API
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        try:
            logger.info("📬 Calling Groq API...")
            response = self.model.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            logger.info(f"✅ Groq response received: {content[:50]}...")
            return content
        except Exception as e:
            logger.error(f"❌ Error calling Groq API: {str(e)}")
            return f"Error generating content: {str(e)}"
