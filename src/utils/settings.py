"""Settings module - Configuration and environment variables"""

import os
from typing import Optional

from dotenv import load_dotenv


class Settings:
    """Application settings loaded from environment variables"""

    def __init__(self, env_file: Optional[str] = None):
        """
        Load settings from .env file or environment variables.

        Args:
            env_file: Path to .env file (default: .env in project root)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

    @property
    def groq_api_key(self) -> str:
        """Get Groq API key"""
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY not set in environment")
        return key

    @property
    def groq_model(self) -> str:
        """Get Groq model name"""
        return os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

    @property
    def debug(self) -> bool:
        """Get debug mode"""
        return os.getenv("DEBUG", "false").lower() == "true"

    @property
    def log_level(self) -> str:
        """Get log level"""
        return os.getenv("LOG_LEVEL", "INFO")

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found

        Returns:
            Environment variable value or default
        """
        return os.getenv(key, default)
