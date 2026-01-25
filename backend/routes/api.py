from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
from typing import Optional
import logging
import os
from pathlib import Path
from services.image_generator import generate_image
from llm.prompts import get_full_prompt

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["generation"])
groq_client = None  # Inicializar groq_client como None
class GenerateRequest(BaseModel):
    tema: str
    plataforma: str
    audiencia: str
    informacion_adicional: str = "" 
    contexto_marca: str = ""
    idioma: str = "es"

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
        
        # ✅ En lugar de importar desde app, usar directamente
        from llm.groq_client import GroqClient
        import os

        groq_api_key = os.getenv("GROQ_API_KEY")
        groq_client = GroqClient(api_key=groq_api_key)
        
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
                base_url = os.getenv("BACKEND_URL", "http://localhost:5000")
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
    """
    ✅ ENDPOINT MULTIAGENTE COMPLETO
    Groq (contenido) → CrewAI/Gemini (refina prompt imagen) → HF (genera imagen)
    """
    try:
        logger.info(f"🤖 CrewAI Request: {request.tema}")
        
        # PASO 1: Generar contenido con Groq (igual que en /generate)
        from llm.groq_client import GroqClient
        groq_api_key = os.getenv("GROQ_API_KEY")
        groq_client = GroqClient(api_key=groq_api_key)
        
        prompt_contenido = get_full_prompt(
            tema=request.tema,
            plataforma=request.plataforma,
            audiencia=request.audiencia,
            informacion_adicional=request.informacion_adicional,
            idioma=request.idioma
        )
        
        contenido = groq_client.generate(prompt_contenido)
        logger.info(f"✅ Contenido Groq: {len(contenido)} caracteres")
        
        # PASO 2: Usar CrewAI para refinar prompt de imagen
        prompt_imagen_refinado = None
        try:
            from agents.crew import run_crew
            
            if run_crew:  # Si CrewAI está disponible
                logger.info("🤖 Ejecutando CrewAI para refinar prompt...")
                prompt_imagen_refinado = run_crew(
                    tema=request.tema,
                    plataforma=request.plataforma,
                    audiencia=request.audiencia,
                    contenido_groq=contenido,
                    contexto_marca=request.informacion_adicional
                )
                logger.info(f"✅ Prompt refinado por CrewAI")
            else:
                logger.warning("⚠️ CrewAI no disponible")
                
        except Exception as crew_error:
            logger.error(f"❌ Error en CrewAI: {str(crew_error)}, usando fallback")
        
        # Si CrewAI falló, usar template estándar
        if not prompt_imagen_refinado:
            template_imagen = IMAGE_PROMPT_TEMPLATES.get(
                request.plataforma.lower(),
                f"High quality image about {request.tema}"
            )
            prompt_imagen_refinado = template_imagen.format(
                tema=request.tema,
                audiencia=request.audiencia
            )
        
        # PASO 3: Generar imagen con prompt refinado
        size = PLATFORM_SIZES.get(request.plataforma.lower(), {"width": 1024, "height": 1024})
        
        try:
            image_url = generate_image(
                prompt_imagen_refinado,
                width=size["width"],
                height=size["height"]
            )
            logger.info(f"✅ Imagen generada: {image_url}")
        except Exception as e:
            logger.warning(f"⚠️ Error imagen: {str(e)}, usando placeholder")
            image_url = f"https://via.placeholder.com/{size['width']}x{size['height']}?text={request.tema[:30]}"
        
        # Convertir URL si es relativa
        if image_url.startswith('/'):
            base_url = os.getenv("BACKEND_URL", "http://localhost:5000")
            image_url = f"{base_url}{image_url}"
        
        # RESPUESTA FINAL CON METADATA DE CREW
        return {
            "contenido": contenido,
            "image_url": image_url,
            "status": "success",
            "execution_type": "multiagent_crew",  # ✅ ESTO ES LA CLAVE
            "metadata": {
                "tema": request.tema,
                "plataforma": request.plataforma,
                "audiencia": request.audiencia,
                "idioma": request.idioma,
                "crew_executed": True,
                "image_prompt_refined": True
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Error en crew_generate: {str(e)}")
        # FALLBACK: usar generación simple
        logger.info("⚠️ Fallback a /api/generate...")
        return generate_content(request)
    

@router.post("/generate-scientific")
def generate_scientific(request: GenerateRequest):
    """
    RAG Endpoint: Contenido científico fundamentado en papers académicos
    Reutiliza generate_content + contexto RAG
    """

    try:
        logger.info(f"🔬 Recibida request científica: {request.tema}")

        # Importar RAG
        from rag.rag_system import RAGSystem
        rag_system = RAGSystem ()
        logger.info("✅ RAGSystem inicializado")

        # Procesar query con RAG
        logger.info(f"⏳ Procesando query con RAG: {request.tema}")
        rag_context = rag_system.process_query(
            query=request.tema,
            use_graph_rag=True
        )
        logger.info(f"✅ RAG context obtenido ({len(rag_context)} caracteres)")

        # Crear prompt mejorado con contexto RAG
        rag_instruction = f"""

🔬 CONTEXTO CIENTÍFICO (fundamentado en papers académicos):
{rag_context}

Usa este contexto académico para fundamentar tu respuesta. 
Mantén rigor científico pero hazlo accesible para {request.audiencia}.
"""

        # Reutilizar información_adicional existente
        if request.informacion_adicional:
            request.informacion_adicional += "\n\n" + rag_instruction
        else:
            request.informacion_adicional = rag_instruction
        
        # Llamar a generate_content existente (evita duplicación)
        logger.info("📤 Llamando a generate_content con contexto RAG")
        response = generate_content(request)
        
        # Agregar metadata RAG
        response["metadata"]["execution_type"] = "rag"
        response["metadata"]["rag_context_length"] = len(rag_context)
        response["metadata"]["has_scientific_context"] = True
        
        logger.info("✅ Respuesta científica generada exitosamente")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error en RAG: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error RAG: {str(e)}")