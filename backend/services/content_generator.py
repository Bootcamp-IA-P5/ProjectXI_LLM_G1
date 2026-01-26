"""Content generation service using LLM Factory pattern"""

import logging
from llm.prompts import get_full_prompt
from .news_service import NewsService

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Orquestador: coordina prompts + llm_client usando Factory pattern
    
    Note: To create an llm_client, use:
        from llm.llm_factory import LLMFactory
        client = LLMFactory.get_client(provider='groq')
        generator = ContentGenerator(client)
    """

    def __init__(self, llm_client):
        """Recibir cliente Groq (inyeccion de dependencia)"""
        self.llm_client = llm_client
        self.plataformas_soportadas = ["twitter", "blog", "instagram", "linkedin", "tiktok", "youtube"]
        # Mapeo de códigos a nombres para que el LLM lo entienda mejor
        self.idiomas_soportados = {
            "es": "Castellano", 
            "en": "English", 
            "fr": "Français", 
            "it": "Italiano"
        }
        self.news_service = NewsService() # Instanciamos el servicio

    def generate_content(self, tema: str, plataforma: str, audiencia: str, 
                         informacion_adicional: str = "", idioma: str = "es") -> str:
        """
        Generar contenido multilingüe y personalizado
        """
        # 1. VALIDACIÓN DE IDIOMA
        if idioma not in self.idiomas_soportados:
            raise ValueError(f"Idioma '{idioma}' no soportado. Usa: {list(self.idiomas_soportados.keys())}")

        if plataforma not in self.plataformas_soportadas:
            raise ValueError(f"Plataforma '{plataforma}' no soportada. Usa: {self.plataformas_soportadas}")
        
        try:     
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
            contenido = self.llm_client.generate(prompt_final)
            
            return contenido
        
        except ValueError as e:
            logger.error(f"Error de validación: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generando contenido: {e}")
            raise ConnectionError(f"Error al generar contenido: {e}")
        
    def generate_news_content(self, tema: str, plataforma: str, audiencia: str, idioma: str = "es"):
        # 1. Obtener noticias en el idioma seleccionado (RAG)
        noticias_frescas = self.news_service.get_financial_news(tema, idioma)
        
        # 2. Obtener el nombre completo del idioma (ej: "Français")
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
        # Generar contenido con contexto de noticias actuales (RAG)
        
        # 4. Generar con llm
        return self.llm_client.generate(prompt_final)