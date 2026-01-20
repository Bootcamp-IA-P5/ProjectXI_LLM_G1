import sys
import os
import pytest

# Setup path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from services.guardrails import ContentGuardrails, BiasDetector, SafetyLevel, ContentValidationError


class TestContentGuardrails:
    """Pruebas de validación de contenido"""
    
    @pytest.fixture
    def guardrails_moderate(self):
        return ContentGuardrails(safety_level=SafetyLevel.MODERATE)
    
    def test_contenido_muy_corto(self, guardrails_moderate):
        """Debe rechazar contenido muy corto"""
        resultado = guardrails_moderate.validate_content("Hola", "twitter")
        assert resultado["valid"] == False
        assert any("corto" in issue.lower() for issue in resultado["issues"])
    
    def test_twitter_limite_caracteres(self, guardrails_moderate):
        """Twitter debe rechazar > 280 caracteres"""
        contenido_largo = "a" * 300
        resultado = guardrails_moderate.validate_content(contenido_largo, "twitter")
        assert resultado["valid"] == False
    
    def test_contenido_valido(self, guardrails_moderate):
        """Debe aceptar contenido válido"""
        contenido = "Este es un contenido válido y de calidad para Twitter con información relevante y apropiada"
        resultado = guardrails_moderate.validate_content(contenido, "twitter")
        assert resultado["valid"] == True


class TestBiasDetection:
    """Pruebas de detección de sesgos"""
    
    @pytest.fixture
    def bias_detector(self):
        return BiasDetector()
    
    def test_sin_sesgos(self, bias_detector):
        """Debe validar contenido inclusivo"""
        contenido = "Los profesionales de todas las edades aportan perspectivas valiosas"
        resultado = bias_detector.analyze_bias(contenido)
        assert resultado["has_bias"] == False
        assert resultado["risk_level"] == "low"
    
    def test_recomendaciones_generadas(self, bias_detector):
        """Debe generar recomendaciones cuando hay sesgos"""
        contenido = "Los hombres son ingenieros y las mujeres son enfermeras"
        resultado = bias_detector.analyze_bias(contenido)
        assert len(resultado["recommendations"]) > 0