"""Groq QA Agent - Question Answering agent using Groq API"""

from typing import Any, Dict, Optional
import asyncio

from groq import Groq

from .base_agent import BaseAgent


class GroqQAAgent(BaseAgent):
    """Agent for Question Answering using Groq API"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Groq QA Agent.

        Args:
            config: Configuration with Groq API key and model settings
        """
        super().__init__(name="groq_qa_agent", config=config)
        
        if self.validate_config():
            self.client = Groq(api_key=self.config.get("api_key"))
        else:
            self.client = None
            
        self.model = self.config.get("model", "mixtral-8x7b-32768")

    async def process(self, input_data: str) -> str:
        """
        Process question and return answer from Groq.

        Args:
            input_data: Question or prompt

        Returns:
            Answer from Groq API
        """
        if not self.validate_config():
            raise ValueError("Invalid Groq configuration")

        if not self.client:
            raise RuntimeError("Groq client not initialized")

        # Run blocking call in executor to avoid blocking event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self._call_groq,
            input_data
        )
        
        return response

    def _call_groq(self, prompt: str) -> str:
        """
        Synchronous call to Groq API.

        Args:
            prompt: The prompt to send to Groq

        Returns:
            The response from Groq
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            raise RuntimeError(f"Error calling Groq API: {str(e)}")

    def validate_config(self) -> bool:
        """Validate Groq configuration."""
        required_keys = ["api_key"]
        return all(key in self.config for key in required_keys)
