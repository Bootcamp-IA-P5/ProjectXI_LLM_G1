from llm.groq_client import GroqClient
from llm.prompts import get_full_prompt
import logging

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Orquestador: coordina prompts + groq_client"""

    def __init__(self, groq_client: GroqClient):
        """Recibir cliente Groq (inyeccion de dependencia)"""
        self.groq_client = groq_client
        self.plataformas_soportadas = ["twitter", "blog", "instagram", "linkedin"]

    def generate_content(self, tema: str, plataforma: str, audiencia: str, informacion_adicional: str = "") -> str:
        """
        Generar contenido para una plataforma especifica
        
        Args: 
            tema: Tema del contenido
            plataforma: las mencionadas
            audiencia: a quien va dirigido
            informacion_adicional: info de la empresa o marca (opcional)
            
        Returns:
            Contenido generado
        
        Raises: 
            ValueError: Si parametros invalidos
            ConnectionError: Si falla la generacion
        """
        try: 
            # Validacion 1: Plataforma soportada
            if plataforma not in self.plataformas_soportadas:
                raise ValueError(f"Plataforma '{plataforma}' no soportada. Usa: {self.plataformas_soportadas}")
            
            # Validacion 2: Parametros no vacios
            if not tema.strip():
                raise ValueError(f"El tema no puede estar vacio")
            if not audiencia.strip():
                raise ValueError("La audiencia no puede estar vacia")
            
            logger.info(f"Generando contenido: {plataforma} - {tema}")
            
            # Paso 1: Obtener prompt final (combina SYSTEM + especifico)
            prompt_final = get_full_prompt(tema, audiencia, plataforma, informacion_adicional)
            
            # Paso 2: Generar con Groq
            contenido = self.groq_client.chat.completions.create(prompt_final)
            
            logger.info("✅ Contenido generado exitosamente")
            
            # Paso 3: Retornar resultado
            return contenido

        except (ValueError, ConnectionError) as e: 
            # Si son nuestras excepciones, solo loguear y relanzar
            logger.error(f"Error en generacion: {e}")
            raise

        except Exception as e:
            # Si es otra excepcion inesperada, loguear y convertir
            logger.error(f"Error inesperado: {e}")
            raise ConnectionError(f"Error al generar contenido: {e}")