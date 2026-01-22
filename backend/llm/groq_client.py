"""Groq API Client with Fallback"""
import logging
from langchain_groq import ChatGroq

logger = logging.getLogger(__name__)


class GroqClient:
    """Client for Groq API using LangChain with automatic model detection"""
    
    # Modelos disponibles en Groq (estos cambian frecuentemente, mantener actualizado)
    # Ver: https://console.groq.com/docs/models
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",  # Modelo más reciente
        "mixtral-8x7b-32768",  # Alternativa
    ]
    
    def __init__(self, api_key: str, model_name: str = None):
        """Initialize Groq client
        
        Args:
            api_key: Groq API key
            model_name: Model name (optional, auto-detects best model)
        """
        if not api_key:
            logger.error("❌ GROQ_API_KEY no está configurada")
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self._initialize_model()
        
    def _initialize_model(self):
        """Initialize the model, trying multiple options if needed"""
        models_to_try = [self.model_name] if self.model_name else self.AVAILABLE_MODELS
        
        for model in models_to_try:
            try:
                logger.info(f"🔧 Intentando inicializar con modelo: {model}")
                test_model = ChatGroq(
                    temperature=0.7,
                    model_name=model,
                    api_key=self.api_key,
                    timeout=10
                )
                # Prueba rápida de conexión
                test_response = test_model.invoke("Test")
                if test_response:
                    self.model = test_model
                    self.model_name = model
                    logger.info(f"✅ Modelo '{model}' inicializado correctamente")
                    return
            except Exception as e:
                logger.warning(f"⚠️ Modelo '{model}' no disponible: {str(e)[:100]}")
                continue
        
        if not self.model:
            logger.error("❌ No se pudo inicializar ningún modelo de Groq")
            raise RuntimeError("Failed to initialize any Groq model")
    
    def generate(self, prompt: str) -> str:
        """Generate text using Groq API
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text (empty string if failed)
        """
        try:
            if not prompt or not prompt.strip():
                logger.error("❌ Prompt vacío")
                return ""
            
            if not self.model:
                logger.error("❌ Modelo no inicializado")
                return ""
                
            logger.info(f"📬 Llamando a Groq API ({self.model})...")
            logger.info(f"📝 Prompt length: {len(prompt)} caracteres")
            
            response = self.model.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            if not content or not content.strip():
                logger.warning("⚠️ Groq retornó respuesta vacía")
                return ""
                
            logger.info(f"✅ Respuesta Groq ({len(content)} caracteres): {content[:80]}...")
            return content
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Error en Groq API: {error_msg[:200]}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()[:500]}")
            return ""



