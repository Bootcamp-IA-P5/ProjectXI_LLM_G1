import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Cliente para comunicarse con Ollama"""
    
    def __init__(self, base_url: str, model: str):
        """
        Inicializar cliente y verificar conexión
        
        Args:
            base_url: URL de Ollama
            model: Modelo a usar
            
        Raises:
            ConnectionError: Si Ollama no está disponible
        """
        self.base_url = base_url
        self.model = model
        self._validate_connection() # Self dice "usa el metodo de ESTA clase"
    
    def _validate_connection(self) -> None:
        """ 
        Verificar que Ollama está disponible
        
        Raises:
            ConnectionError: Si no puede conectar
        """
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200: # Si falla HTTP
                raise ConnectionError ("Ollama no disponible, el servidor respondió pero con error")
            logger.info(f"Conexión con Ollama establecida")
        except requests.RequestException as e: # Si falla la conexion misma
            raise ConnectionError(f"No se pudo conectar (quizá red caida, etc): {e}") 
            
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generar contenido con Ollama
        
        Args:
            prompt: Texto a procesar
            temperature: Creatividad (0-1)
            max_tokens: Maximo de tokens a generar
        
        Returns:
            Texto generado
            
        Raises:
            ValueError: Si prompt vacio
            ConnectionError: Si falla la generacion
        """
        
        self._validate_prompt(prompt)
        
        try: 
            response = requests.post(
                f"{self.base_url}/api/generate",
                json = {"model": self.model, "prompt": prompt, "temperature": temperature},
                stream = False # Importatnte para Ollama
            )
            if response.status_code != 200: raise ConnectionError("Fallo en generacion")
        
            result= self._parse_response(response.json()) # Guardar en variable
            return result
            
        except requests.RequestException as e:
            raise ConnectionError(f"Error al generar: {e}")
    
    def _validate_prompt(self, prompt: str) -> None:
        """
        Validar que el prompt es valido
        
        Raises:
            ValueError: Si prompt está vacio o es invalido
        """
        if (len(prompt.strip()) == 0):    
            raise ValueError ("El prompt no puede estar vacio")
    
    def _parse_response(self, response: dict) -> str: 
        """
        Extraer texto de respuesta de Ollama
        
        Args:
            response: Response dict de Ollama
        
        Returns:
            Texto generado
        
        Raises: 
            ValueError: Si respuesta invalida
        """
        if "response" not in response:
            raise ValueError("Respuesta invalida de Ollama")
        return response["response"]
        pass
    