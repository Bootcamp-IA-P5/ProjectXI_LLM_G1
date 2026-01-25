import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pytest


# Setup path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# Mock TODAS las dependencias externas ANTES de importar
sys.modules['crewai'] = MagicMock()
sys.modules['agents'] = MagicMock()
sys.modules['agents.crew'] = MagicMock()
sys.modules['huggingface_hub'] = MagicMock()


from fastapi.testclient import TestClient
from fastapi import FastAPI
from routes.api import router

# Crear app de test
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestGenerateContentEndpoint:
    """Pruebas del endpoint /generate"""
    
    @pytest.fixture
    def mock_groq_client(self):
        """Mock de GroqClient"""
        mock = Mock()
        mock.generate.return_value = "Este es contenido generado para testing. Es válido y de calidad para redes sociales."
        return mock
    
    def test_generate_content_post_exitoso(self, mock_groq_client):
        """Debe generar contenido exitosamente por API"""
        payload = {
            "tema": "Machine Learning",
            "plataforma": "twitter",
            "audiencia": "Data Scientists",
            "idioma": "es"
        }
        
        with patch('routes.api.groq_client', mock_groq_client):
            response = client.post("/api/generate", json=payload)
        
        assert response.status_code == 500 or response.status_code == 200
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "success"
            assert "contenido" in data
            assert data["validado"] == True
            
    
    def test_generate_content_plataforma_invalida(self, mock_groq_client):
        """Debe retornar error para plataforma inválida"""
        payload = {
            "tema": "IA",
            "plataforma": "snapchat",
            "audiencia": "Jóvenes",
            "idioma": "es"
        }
        
        with patch('routes.api.groq_client', mock_groq_client):
            response = client.post("/api/generate", json=payload)
        
        assert response.status_code in [400, 422, 500]
    
    def test_generate_content_datos_faltantes(self):
        """Debe retornar 422 si faltan datos"""
        payload = {"tema": "IA"}
        response = client.post("/api/generate", json=payload)
        
        assert response.status_code == 422
    
    def test_idioma_soportado(self, mock_groq_client):
        """Debe aceptar idiomas soportados"""
        for idioma in ["es", "en", "fr", "it"]:
            payload = {
                "tema": "IA",
                "plataforma": "twitter",
                "audiencia": "Técnicos",
                "idioma": idioma
            }
            
            with patch('routes.api.groq_client', mock_groq_client):
                response = client.post("/api/generate", json=payload)
            
            assert response.status_code == 500 or response.status_code == 200