"""Content generation service using LLM Factory pattern"""

import logging
from llm.prompts import get_full_prompt
from services.news_service import NewsService

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Orquestador: coordina prompts + llm_client usando Factory pattern"""

    def __init__(self, llm_client):
        """
        Recibir cliente LLM (inyeccion de dependencia desde Factory)
        
        Args:
            llm_client: Cliente LLM (Groq, Gemini, u Ollama)
        """
        self.llm_client = llm_client
        self.news_service = NewsService()
        self.plataformas_soportadas = ["twitter", "blog", "instagram", "linkedin"]
        # Mapeo de códigos a nombres para que el LLM lo entienda mejor
        self.idiomas_soportados = {
            "es": "Castellano", 
            "en": "English", 
            "fr": "Français", 
            "it": "Italiano"
        }

    def generate_content(self, tema: str, plataforma: str, audiencia: str, 
                         informacion_adicional: str = "", idioma: str = "es") -> str:
        """
        Generar contenido multilingüe y personalizado
        
        Args:
            tema: Tema del contenido
            plataforma: Plataforma de destino
            audiencia: Audiencia objetivo
            informacion_adicional: Información extra opcional
            idioma: Código de idioma (es, en, fr, it)
            
        Returns:
            Contenido generado
            
        Raises:
            ValueError: Si idioma no soportado
            ConnectionError: Si falla la generación
        """
        try: 
            # 1. VALIDACIÓN DE IDIOMA
            if idioma not in self.idiomas_soportados:
                raise ValueError(f"Idioma '{idioma}' no soportado.")
            
            nombre_idioma = self.idiomas_soportados[idioma]
            
            # 2. SELECCIÓN DEL PROMPT
            prompt_final = get_full_prompt(
                tema=tema, 
                audiencia=audiencia, 
                plataforma=plataforma, 
                informacion_adicional=informacion_adicional, 
                idioma=nombre_idioma
            )
            
            # 3. GENERACIÓN CON LLM
            # For LangChain clients (Groq)
            if hasattr(self.llm_client, 'invoke'):
                response = self.llm_client.invoke(prompt_final)
                contenido = response.content if hasattr(response, 'content') else str(response)
            # For Ollama client
            elif hasattr(self.llm_client, 'generate'):
                contenido = self.llm_client.generate(prompt_final)
            else:
                raise ValueError("Cliente LLM no compatible")
            
            return contenido

        except (ValueError, ConnectionError) as e: 
            logger.error(f"Error en generacion: {e}")
            raise

        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise ConnectionError(f"Error al generar contenido: {e}")

    def generate_news_content(self, tema: str, plataforma: str, audiencia: str, idioma: str = "es") -> str:
        """
        Generar contenido con contexto de noticias actuales (RAG)
        
        Args:
            tema: Tema del contenido
            plataforma: Plataforma de destino
            audiencia: Audiencia objetivo
            idioma: Código de idioma
            
        Returns:
            Contenido generado con contexto de noticias
        """
        try:
            # 1. Obtener noticias en el idioma seleccionado (RAG)
            noticias_frescas = self.news_service.get_financial_news(tema, idioma)
            
            # 2. Obtener el nombre completo del idioma
            nombre_idioma = self.idiomas_soportados.get(idioma, "Castellano")
            
            # 3. Construir el Prompt Maestro (Multilingüe + Noticias)
            prompt_final = f"""
INSTRUCCIÓN DE IDIOMA: Debes escribir exclusivamente en {nombre_idioma}.

CONTEXTO ACTUAL (NOTICIAS):
{noticias_frescas}

TAREA:
Actúa como un analista financiero experto. Crea un post para {plataforma} 
dirigido a una audiencia de {audiencia}. 
Usa los datos de las noticias anteriores para que el contenido sea actual.
"""
            
            # 4. Generar con LLM
            if hasattr(self.llm_client, 'invoke'):
                response = self.llm_client.invoke(prompt_final)
                contenido = response.content if hasattr(response, 'content') else str(response)
            elif hasattr(self.llm_client, 'generate'):
                contenido = self.llm_client.generate(prompt_final)
            else:
                raise ValueError("Cliente LLM no compatible")
            
            return contenido
            
        except Exception as e:
            logger.error(f"Error en generate_news_content: {e}")
            raise