import logging
from enum import Enum
from typing import List, Dict

logger = logging.getLogger(__name__)

class SafetyLevel(Enum):
    """Niveles de seguridad para validación de contenido"""
    STRICT = "strict"
    MODERATE = "moderate"
    PERMISSIVE = "permissive"

class ContentValidationError(Exception):
    """Excepción para validaciones fallidas"""
    pass

class ContentGuardrails:
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.MODERATE):
        self.safety_level = safety_level
        self.bias_detector = BiasDetector()

    def validate_content(self, contenido: str, plataforma: str) -> Dict:
        """
        Valida el contenido según longitud, plataforma y sesgos.
        Devuelve dict con keys: valid (bool), issues (List[str])
        """
        issues = []

        # Validación de longitud según plataforma
        if plataforma.lower() == "twitter" and len(contenido) > 280:
            issues.append("Contenido excede límite de 280 caracteres")
        if len(contenido.strip()) < 10:
            issues.append("Contenido demasiado corto")
        #validar otras plataformas

        # Detectar sesgos
        bias_result = self.bias_detector.analyze_bias(contenido)
        if bias_result["has_bias"]:
            issues.append("Se detectaron posibles sesgos")

        valid = len(issues) == 0
        return {"valid": valid, "issues": issues}

class BiasDetector:
    """Detecta sesgos potenciales en contenido generado"""
    
    def __init__(self):
        self.gender_bias_patterns = {
            "masculine_stereotypes": ["ingeniero", "jefe", "director", "programador", "ceo"],
            "feminine_stereotypes": ["enfermera", "secretaria", "ama de casa", "delicada"]
        }
        self.age_bias_patterns = {
            "ageism": ["viejo", "anciano", "joven inexperto", "lento"]
        }
        self.racial_bias_patterns = {
            "stereotypes": ["exótico", "auténtico", "primitivo"]
        }
        self.ability_bias_patterns = {
            "ableist_language": ["discapacitado", "sufre de", "víctima"]
        }

    def analyze_bias(self, contenido: str) -> Dict:
        contenido_lower = contenido.lower()
        biases_found = {
            "gender": self._detect_gender_bias(contenido_lower),
            "age": self._detect_age_bias(contenido_lower),
            "racial": self._detect_racial_bias(contenido_lower),
            "ability": self._detect_ability_bias(contenido_lower)
        }
        
        total_biases = sum(len(b) for b in biases_found.values())
        
        return {
            "has_bias": total_biases > 0,
            "bias_types": {k: v for k, v in biases_found.items() if v},
            "risk_level": "high" if total_biases > 2 else "medium" if total_biases > 0 else "low",
            "total_biases_detected": total_biases,
            "recommendations": self._generate_recommendations(biases_found)
        }

    def _detect_gender_bias(self, text: str) -> List[Dict]:
        sesgos = []
        if any(term in text for term in self.gender_bias_patterns["masculine_stereotypes"]):
            sesgos.append({"type": "gender_bias", "message": "Estereotipo masculino detectado"})
        return sesgos

    def _detect_age_bias(self, text: str) -> List[Dict]:
        return [{"type": "ageism"}] if any(t in text for t in self.age_bias_patterns["ageism"]) else []

    def _detect_racial_bias(self, text: str) -> List[Dict]:
        return [{"type": "racial"}] if any(t in text for t in self.racial_bias_patterns["stereotypes"]) else []

    def _detect_ability_bias(self, text: str) -> List[Dict]:
        return [{"type": "ability"}] if any(t in text for t in self.ability_bias_patterns["ableist_language"]) else []

    def _generate_recommendations(self, biases: Dict) -> List[str]:
        recs = []
        if biases["gender"]: recs.append("Usar lenguaje inclusivo")
        if biases["age"]: recs.append("No usar estereotipos de edad")
        if biases["racial"]: recs.append("No usar estereotipos raciales")
        if biases["ability"]: recs.append("No usar lenguaje capacitista")
        return recs