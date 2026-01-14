"""Base Agent class - Abstract base for all agents"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseAgent(ABC):
    """Abstract base class for AI agents"""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent.

        Args:
            name: Agent name
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}

    @abstractmethod
    async def process(self, input_data: str) -> str:
        """
        Process input and generate response.

        Args:
            input_data: Input text to process

        Returns:
            Generated response
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate agent configuration."""
        pass
