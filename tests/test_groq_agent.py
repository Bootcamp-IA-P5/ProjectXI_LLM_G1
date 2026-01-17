"""Tests for Groq QA Agent"""

import pytest
import sys
import os

# Add backend to path so we can import from backend/agents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agents.groq_qa_agent import GroqQAAgent


@pytest.fixture
def agent_config():
    """Fixture for agent configuration"""
    return {
        "api_key": os.getenv("GROQ_API_KEY", "test_key"),
        "model": "mixtral-8x7b-32768"
    }


@pytest.fixture
def groq_agent(agent_config):
    """Fixture for GroqQAAgent instance"""
    return GroqQAAgent(config=agent_config)


def test_agent_initialization(groq_agent):
    """Test agent initialization"""
    assert groq_agent.name == "groq_qa_agent"
    assert groq_agent.model == "mixtral-8x7b-32768"


def test_agent_config_validation(groq_agent):
    """Test configuration validation"""
    assert groq_agent.validate_config() is True


def test_agent_config_validation_missing_key():
    """Test validation fails with missing API key"""
    agent = GroqQAAgent(config={})
    assert agent.validate_config() is False


@pytest.mark.asyncio
async def test_agent_process(groq_agent):
    """Test agent processing"""
    result = await groq_agent.process("What is AI?")
    assert isinstance(result, str)
    assert len(result) > 0
