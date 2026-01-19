from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
# from backend.agents.crew import run_crew  # TODO: Uncomment after crewai is installed
from ..services.image_generator import generate_image
from ..llm.prompts import get_full_prompt
# from rag.rag_system import RAGSystem  # Comentado temporalmente
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["generation"])

class GenerateRequest(BaseModel):
    tema: str
    plataforma: str
    audiencia: str
    informacion_adicional: str = "" 
    contexto_marca: str = ""
    idioma: str = "Castellano"

PLATFORM_SIZES = {
    "twitter": {"width": 1200, "height": 630},
    "instagram": {"width": 1080, "height": 1080},
    "blog": {"width": 1200, "height": 800},
    "linkedin": {"width": 1200, "height": 630}
}

# Diccionario para refinar prompts de imagen según plataforma y tema
IMAGE_PROMPT_TEMPLATES = {
    "instagram": "Beautiful, highly detailed Instagram post about {tema}, professional photography, modern aesthetic, vibrant colors, 4K quality, appealing to {audiencia}",
    "twitter": "Minimalist, eye-catching Twitter/X header image about {tema}, professional design, modern style, 4K quality, suitable for {audiencia}",
    "linkedin": "Professional corporate image about {tema}, clean design, business-oriented, high quality photography, 4K resolution, suitable for professionals in {audiencia}",
    "blog": "Comprehensive, detailed blog header image about {tema}, professional photography, informative visual, 4K quality, engaging for {audiencia}"
}


@router.post("/generate")
def generate_content(request: GenerateRequest):
    """Endpoint de generación de contenido: tema + plataforma → contenido + imagen"""
    
    try:    
        logger.info(f"📝 Recibida request: tema={request.tema}, plataforma={request.plataforma}, audiencia={request.audiencia}")
        
        # Validar plataforma
        if request.plataforma.lower() not in PLATFORM_SIZES:
            raise ValueError(f"Plataforma '{request.plataforma}' no válida. Usa: {list(PLATFORM_SIZES.keys())}")
        
        # Usar la función get_full_prompt para generar un prompt bien estructurado
        prompt_contenido = get_full_prompt(
            tema=request.tema,
            plataforma=request.plataforma,
            audiencia=request.audiencia,
            informacion_adicional=request.informacion_adicional,
            idioma=request.idioma
        )
        
        logger.info(f"📬 Prompt generado: {prompt_contenido[:100]}...")
        logger.info(f"📬 Enviando prompt a Groq...")
        
        # Lazy import para evitar circular imports
        from ..app import groq_client
        
        logger.info(f"🔍 Groq client status: {groq_client}")
        logger.info(f"🔍 Groq client api_key exists: {bool(groq_client.api_key)}")
        logger.info(f"🔍 Groq model: {groq_client.model_name}")
        
        # Usar groq_client para generar contenido real
        logger.info("⏳ Esperando respuesta de Groq...")
        contenido = groq_client.generate(prompt_contenido)
        
        logger.info(f"🔍 Respuesta Groq: '{contenido[:100] if contenido else 'VACÍO'}'")
        logger.info(f"🔍 Largo: {len(contenido) if contenido else 0} caracteres")
        
        # Si Groq falló, intentar con Gemini
        if not contenido or contenido.strip() == "":
            logger.warning(f"⚠️ Groq no generó contenido. Intentando fallback con Gemini...")
            try:
                import google.generativeai as genai
                google_key = os.getenv("GOOGLE_API_KEY")
                if google_key:
                    genai.configure(api_key=google_key)
                    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                    response = gemini_model.generate_content(prompt_contenido)
                    contenido = response.text if response else ""
                    logger.info(f"✅ Gemini generó contenido ({len(contenido)} caracteres)")
                else:
                    logger.warning("⚠️ GOOGLE_API_KEY no configurada, usando placeholder")
            except Exception as e:
                logger.warning(f"⚠️ Error con Gemini fallback: {str(e)[:100]}")
        
        # Si aún no hay contenido, usar placeholder
        if not contenido or contenido.strip() == "":
            logger.warning(f"⚠️ No se generó contenido. Usando placeholder")
            contenido = f"""📌 Descubre todo sobre {request.tema}

En el mundo digital actual, {request.tema.lower()} se ha convertido en un elemento fundamental. 
Nuestro equipo de expertos te presenta una guía completa para que aproveches al máximo 
el potencial de {request.tema.lower()} en tu estrategia de {request.plataforma}.

✨ Características principales:
• Información detallada y práctica
• Estrategias comprobadas
• Ejemplos de implementación
• Resultados medibles

Dirigido especialmente a {request.audiencia}.
¡Descubre cómo transformar tu negocio hoy!"""
        else:
            logger.info(f"✅ Contenido válido recibido ({len(contenido)} caracteres)")
        
        # Generar prompt mejorado para imagen basado en la plataforma y tema
        template_imagen = IMAGE_PROMPT_TEMPLATES.get(
            request.plataforma.lower(),
            "High quality professional image for {tema}, modern design, appealing to {audiencia}, 4K quality"
        )
        
        prompt_imagen = template_imagen.format(
            tema=request.tema,
            audiencia=request.audiencia
        )
        
        # Mejorar el prompt de imagen con más contexto
        if request.informacion_adicional:
            prompt_imagen += f", brand context: {request.informacion_adicional[:100]}"
        
        # Generar imagen con tamaño según plataforma
        size = PLATFORM_SIZES.get(request.plataforma.lower(), {"width": 1024, "height": 1024})
        logger.info(f"🖼️ Generando imagen con tamaño {size['width']}x{size['height']}")
        logger.info(f"🎨 Prompt imagen: {prompt_imagen}")
        
        try:
            image_url = generate_image(
                prompt_imagen, 
                width=size["width"], 
                height=size["height"]
            )
            logger.info(f"✅ Image URL generada: {image_url}")
            
            # Convertir URL relativa a absoluta si es necesario
            if image_url.startswith('/'):
                # Usar variable de entorno para URL base, default a localhost:8000
                base_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                image_url = f"{base_url}{image_url}"
                logger.info(f"✅ URL convertida a absoluta: {image_url}")
                
        except Exception as e:
            logger.error(f"❌ Error generando imagen: {str(e)}")
            # Si falla la imagen, usar placeholder
            image_url = f"https://via.placeholder.com/{size['width']}x{size['height']}?text={request.tema.replace(' ', '+')}"
            logger.info(f"✅ Usando imagen placeholder: {image_url}")
            
        response = {
            "contenido": contenido, 
            "image_url": image_url,
            "status": "success",
            "metadata": {
                "tema": request.tema,
                "plataforma": request.plataforma,
                "audiencia": request.audiencia,
                "idioma": request.idioma
            }
        }
        logger.info(f"📤 Respuesta final generada exitosamente")
        return response
    
    except ValueError as e:
        logger.error(f"❌ Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error en generación de contenido: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/crew/generate")
def crew_generate(request: GenerateRequest):
    """Endpoint multiagente: Groq >> Gemini >> Imagen (alias para /api/generate)"""
    return generate_content(request)
    