from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
# from backend.agents.crew import run_crew  # TODO: Uncomment after crewai is installed
from ..services.image_generator import generate_image
# from rag.rag_system import RAGSystem  # Comentado temporalmente
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["generation"])

class GenerateRequest(BaseModel):
    tema: str
    plataforma: str
    audiencia: str
    informacion_adicional: str = "" 
    contexto_marca: str = ""

PLATFORM_SIZES = {
    "twitter": {"width": 1200, "height": 630},
    "instagram": {"width": 1080, "height": 1080},
    "blog": {"width": 1200, "height": 800},
    "linkedin": {"width": 1200, "height": 630}
}


@router.post("/generate")
def generate_content(request: GenerateRequest):
    """Endpoint de generación de contenido: tema + plataforma → contenido + imagen"""
    
    try:    
        logger.info(f"📝 Recibida request: tema={request.tema}, plataforma={request.plataforma}")
        
        # Crear prompt mejorado para Groq
        prompt = f"""Genera un contenido profesional y atractivo para {request.plataforma} sobre el tema: {request.tema}

Audiencia: {request.audiencia}
Información adicional: {request.informacion_adicional if request.informacion_adicional else 'Ninguna'}
Contexto de marca: {request.contexto_marca if request.contexto_marca else 'Ninguno'}

Requisitos:
- Contenido conciso pero informativo (3-4 párrafos)
- Atractivo y engaging para {request.audiencia}
- Optimizado para {request.plataforma}
- Incluye un llamado a la acción
- Tono profesional pero accesible
- Puntos clave destacados

Responde SOLO con el contenido, sin explicaciones adicionales."""
        
        logger.info(f"📬 Enviando prompt a Groq...")
        
        # Lazy import para evitar circular imports
        from ..app import groq_client
        
        # Usar groq_client para generar contenido real
        contenido = groq_client.generate(prompt)
        
        if not contenido or contenido.startswith("Error"):
            logger.warning(f"⚠️ Groq retornó un error o contenido vacío, usando placeholder")
            contenido = f"""Descubre todo sobre {request.tema}

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
        
        logger.info(f"✅ Contenido generado: {contenido[:50]}...")
        
        # Prompt para imagen más descriptivo basado en el contenido
        prompt_imagen = f"High quality professional image for {request.plataforma} about {request.tema}, modern design, appealing to {request.audiencia}, 4K quality"
        
        # Generar imagen con tamaño según plataforma
        size = PLATFORM_SIZES.get(request.plataforma.lower(), {"width": 1024, "height": 1024})
        logger.info(f"🖼️ Generando imagen con tamaño: {size}")
        
        image_url = generate_image(
            prompt_imagen, 
            width=size["width"], 
            height=size["height"]
        )
        logger.info(f"✅ Image URL generada: {image_url}")
            
        response = {
            "contenido": contenido, 
            "image_url": image_url,
            "status": "success"
        }
        logger.info(f"📤 Respuesta final generada exitosamente")
        return response
    
    except Exception as e:
        logger.error(f"❌ Error en generación de contenido: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/crew/generate")
def crew_generate(request: GenerateRequest):
    """Endpoint multiagente: Groq >> Gemini >> Imagen (alias para /api/generate)"""
    return generate_content(request)
    