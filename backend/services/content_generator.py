from llm.groq_client import GroqClient
from llm.prompts import get_full_prompt
import logging
from services.news_service import NewsService
from services.guardrails import ContentGuardrails, SafetyLevel, ContentValidationError


logger = logging.getLogger(__name__)

class ContentGenerator:
    """Orquestador: coordina prompts + groq_client"""

    def __init__(self, groq_client: GroqClient):
        """Recibir cliente Groq (inyeccion de dependencia)"""
        self.groq_client = groq_client
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
        """
        try: 
            # 1. VALIDACIÓN DE IDIOMA
            # Comprobamos si el código de idioma enviado por el frontend existe en nuestro diccionario
            if idioma not in self.idiomas_soportados:
                raise ValueError(f"Idioma '{idioma}' no soportado.")
        
        # Manejo de la excepción en caso de que el idioma no sea soportado
        except ValueError as e:
            print(f"Error: {e}")
            
            nombre_idioma = self.idiomas_soportados[idioma]
            
            # 2. SELECCIÓN DEL PROMPT (Inyectando el idioma y la info extra)
            # Pasamos todos los parámetros a get_full_prompt para construir la instrucción final
            prompt_final = get_full_prompt(
                tema=tema, 
                audiencia=audiencia, 
                plataforma=plataforma, 
                informacion_adicional=informacion_adicional, 
                idioma=nombre_idioma
            )
            
            # 3. GENERACIÓN CON OLLAMA
            # El cliente de Ollama recibe el prompt ya traducido y configurado
            contenido = self.ollama_client.generate(prompt_final)
            
            return contenido
class ContentGenerator:
    """Orquestador: coordina prompts + ollama_client"""

    def __init__(self, ollama_client: OllamaClient):
        self.ollama_client = ollama_client
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
        """
        try: 
            # 1. VALIDACIÓN DE IDIOMA
            # Comprobamos si el código de idioma enviado por el frontend existe en nuestro diccionario
            if idioma not in self.idiomas_soportados:
                raise ValueError(f"Idioma '{idioma}' no soportado.")
            
            nombre_idioma = self.idiomas_soportados[idioma]
            
            # 2. SELECCIÓN DEL PROMPT (Inyectando el idioma y la info extra)
            # Pasamos todos los parámetros a get_full_prompt para construir la instrucción final
            prompt_final = get_full_prompt(
                tema=tema, 
                audiencia=audiencia, 
                plataforma=plataforma, 
                informacion_adicional=informacion_adicional, 
                idioma=nombre_idioma
            )
            
            # Paso 1: Obtener prompt final (combina SYSTEM + especifico)
            prompt_final = get_full_prompt(tema, audiencia, plataforma, informacion_adicional)
            
            # Paso 2: Generar con Groq
            contenido = self.groq_client.chat.completions.create(prompt_final)
            
            return contenido

        except Exception as e:
            logger.error(f"Error en el generador: {e}")
            raise

        except (ValueError, ConnectionError) as e: 
            # Si son nuestras excepciones, solo loguear y relanzar
            logger.error(f"Error en generacion: {e}")
            raise

        except Exception as e:
            # Si es otra excepcion inesperada, loguear y convertir
            logger.error(f"Error inesperado: {e}")
            raise ConnectionError(f"Error al generar contenido: {e}")
        
        class ContentGenerator:
    def __init__(self, groq_client: GroqClient):
        self.groq_client = groq_client
        self.guardrails = ContentGuardrails(safety_level=SafetyLevel.MODERATE)
        self.plataformas_soportadas = ["twitter", "blog", "instagram", "linkedin"]
        self.idiomas_soportados = {
            "es": "Castellano", 
            "en": "English", 
            "fr": "Français", 
            "it": "Italiano"
        }
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.MODERATE):
        self.safety_level = safety_level
        self.max_length = 10000
        self.min_length = 10
        self.bias_detector = BiasDetector()  # ← AGREGAR
    
    def generate_content(self, tema: str, plataforma: str, audiencia: str, 
                        informacion_adicional: str = "", idioma: str = "es") -> str:
        """Generar con validación de guardrails"""
        
        # Validar entrada
        if plataforma not in self.plataformas_soportadas:
            raise ValueError(f"Plataforma '{plataforma}' no soportada")
        
        if idioma not in self.idiomas_soportados:
            raise ValueError(f"Idioma '{idioma}' no soportado")
        
        # Construir prompt
        nombre_idioma = self.idiomas_soportados[idioma]
        prompt_final = get_full_prompt(
            tema=tema,
            audiencia=audiencia,
            plataforma=plataforma,
            informacion_adicional=informacion_adicional,
            idioma=nombre_idioma
        )
        
        # Generar con Groq
        contenido = self.groq_client.generate(prompt_final)
        
        # **APLICAR GUARDRAILS**
        validacion = self.guardrails.validate_content(contenido, plataforma)
        
        if not validacion["valid"]:
            logger.warning(f"Contenido rechazado. Problemas: {validacion['issues']}")
            raise ContentValidationError(
                f"El contenido no cumple estándares: {', '.join(validacion['issues'])}"
            )
        
        logger.info(f"Contenido validado exitosamente para {plataforma}")
        return validacion["cleaned_content"]
    
        def generate_content(self, tema: str, plataforma: str, audiencia: str, 
                            informacion_adicional: str = "", idioma: str = "es") -> dict:
            """
            Generar contenido con validación de guardrails y análisis de sesgos
            
            Returns:
                {
                    "contenido": str,
                    "validado": bool,
                    "bias_report": dict,
                    "issues": list
                }
            """
        try:
            # 1. VALIDAR ENTRADA
            if plataforma not in self.plataformas_soportadas:
                raise ValueError(f"Plataforma '{plataforma}' no soportada")
            
            if idioma not in self.idiomas_soportados:
                raise ValueError(f"Idioma '{idioma}' no soportado")
            
            # 2. CONSTRUIR PROMPT
            nombre_idioma = self.idiomas_soportados[idioma]
            prompt_final = self.get_full_prompt(
                tema=tema,
                audiencia=audiencia,
                plataforma=plataforma,
                informacion_adicional=informacion_adicional,
                idioma=nombre_idioma
            )
            
            # 3. GENERAR CON GROQ
            logger.info(f"Generando contenido para {plataforma}...")
            contenido = self.groq_client.generate(prompt_final)
            
            # 4. APLICAR GUARDRAILS (validación básica)
            logger.info("Aplicando guardrails...")
            validacion = self.guardrails.validate_content(contenido, plataforma)
            
            if not validacion["valid"]:
                logger.warning(f"Contenido rechazado. Problemas: {validacion['issues']}")
                raise ContentValidationError(
                    f"El contenido no cumple estándares: {', '.join(validacion['issues'])}"
                )
            
            # 5. ANALIZAR SESGOS
            logger.info("Analizando sesgos...")
            bias_report = validacion.get("bias_report", {})
            
            if bias_report.get("has_bias"):
                logger.warning(f"Sesgos detectados: {bias_report['bias_types']}")
            
            # 6. RETORNAR RESULTADO COMPLETO
            logger.info(f"✓ Contenido validado exitosamente para {plataforma}")
            
            return {
                "contenido": validacion["cleaned_content"],
                "validado": True,
                "bias_report": bias_report,
                "issues": [],
                "status": "success"
            }
        
        except ContentValidationError as e:
            logger.error(f"Error de validación: {str(e)}")
            return {
                "contenido": None,
                "validado": False,
                "bias_report": None,
                "issues": [str(e)],
                "status": "validation_error"
            }
        
        except ValueError as e:
            logger.error(f"Error de entrada: {str(e)}")
            return {
                "contenido": None,
                "validado": False,
                "bias_report": None,
                "issues": [str(e)],
                "status": "input_error"
            }
        
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return {
                "contenido": None,
                "validado": False,
                "bias_report": None,
                "issues": [f"Error generando contenido: {str(e)}"],
                "status": "error"
            }