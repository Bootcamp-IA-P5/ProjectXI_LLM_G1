import sys
import os
import pytest
from unittest.mock import Mock

# Agregar backend al path CORRECTAMENTE
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

print(f"✓ Path agregado: {backend_path}")


@pytest.fixture(scope="session")
def test_config():
    """Configuración global de tests"""
    return {
        "timeout": 10,
        "debug": True
    }


@pytest.fixture
def mock_crewai():
    """Mock de crewai para evitar dependencias externas"""
    mock = Mock()
    mock.Crew = Mock()
    mock.Task = Mock()
    return mock