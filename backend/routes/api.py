from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
# from backend.agents.crew import run_crew  # TODO: Uncomment after crewai is installed - chromadb version conflict
from ..services.image_generator import generate_image
from ..services.video_script_generator import VideoScriptGenerator
from ..llm.prompts import get_full_prompt
# from ..rag.rag_system import RAGSystem  # TODO: Fix import path and dependencies
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


class VideoScriptRequest(BaseModel):
    tema: str
    plataforma: str  # youtube, tiktok, youtube_shorts, instagram_reels
    audiencia: str
    estilo: str = "Educativo"  # Educativo, Entretenimiento, Tutorial, Lifestyle, etc.
    idioma: str = "es"  # es, en, fr, it
    duracion_minutos: int = 1
    informacion_adicional: str = ""


class ChoreographyRequest(BaseModel):
    tema: str
    audiencia: str
    nivel_dificultad: str = "Intermedio"  # Principiante, Intermedio, Avanzado
    idioma: str = "es"
    informacion_adicional: str = ""


class MusicGuideRequest(BaseModel):
    tema: str
    plataforma: str
    genero: str = "Pop"
    idioma: str = "es"

PLATFORM_SIZES = {
    "twitter": {"width": 1200, "height": 630},
    "instagram": {"width": 1080, "height": 1080},
    "blog": {"width": 1200, "height": 800},
    "linkedin": {"width": 1200, "height": 630},
    "tiktok": {"width": 1080, "height": 1920},
    "youtube": {"width": 1280, "height": 720}
}

# Diccionario para refinar prompts de imagen según plataforma y tema
IMAGE_PROMPT_TEMPLATES = {
    "instagram": "Beautiful, highly detailed Instagram post about {tema}, professional photography, modern aesthetic, vibrant colors, 4K quality, appealing to {audiencia}",
    "twitter": "Minimalist, eye-catching Twitter/X header image about {tema}, professional design, modern style, 4K quality, suitable for {audiencia}",
    "linkedin": "Professional corporate image about {tema}, clean design, business-oriented, high quality photography, 4K resolution, suitable for professionals in {audiencia}",
    "blog": "Comprehensive, detailed blog header image about {tema}, professional photography, informative visual, 4K quality, engaging for {audiencia}",
    "tiktok": "Vibrant, eye-catching TikTok thumbnail about {tema}, trendy design, vertical format optimized, engaging visual for Gen Z audience interested in {audiencia}",
    "youtube": "Professional YouTube thumbnail about {tema}, bold typography, high contrast colors, clickable design, 4K quality, suitable for viewers interested in {audiencia}"
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
                # Usar variable de entorno para URL base, default a localhost:5001 (puerto del backend)
                base_url = os.getenv("BACKEND_URL", "http://localhost:5001")
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


# ========== ENDPOINTS DE VIDEO SCRIPTS ==========

@router.post("/video/script")
def generate_video_script(request: VideoScriptRequest):
    """Generar guión completo para video (YouTube, TikTok, Instagram Reels, YouTube Shorts)
    
    Incluye:
    - Concepto general y gancho inicial
    - Guión narrativo
    - Coreografía y movimientos
    - Recomendaciones musicales
    - Transiciones y efectos
    - Equipamiento necesario
    - Timeline detallado
    - Tips para viralizar
    - Checklist de producción
    """
    try:
        logger.info(f"🎬 Generando script de video: {request.plataforma} - {request.tema}")
        
        # Validar plataformas permitidas
        plataformas_video = ["youtube", "tiktok", "youtube_shorts", "instagram_reels"]
        if request.plataforma not in plataformas_video:
            raise ValueError(
                f"Plataforma '{request.plataforma}' no válida para videos. "
                f"Usa: {plataformas_video}"
            )
        
        # Lazy import para evitar circular imports
        from ..app import groq_client
        
        # Instanciar generador de scripts
        video_gen = VideoScriptGenerator(groq_client)
        
        # Generar guión
        resultado = video_gen.generate_video_script(
            tema=request.tema,
            plataforma=request.plataforma,
            audiencia=request.audiencia,
            estilo=request.estilo,
            idioma=request.idioma,
            duracion_minutos=request.duracion_minutos,
            informacion_adicional=request.informacion_adicional
        )
        
        logger.info(f"✅ Script generado exitosamente")
        return resultado
        
    except ValueError as e:
        logger.error(f"❌ Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        logger.error(f"❌ Error de conexión LLM: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error generando script: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/video/choreography")
def generate_choreography(request: ChoreographyRequest):
    """Generar guía de coreografía paso a paso para videos de baile
    
    Incluye:
    - Visión general del concepto
    - Pasos básicos explicados
    - Coreografía detallada segundo a segundo
    - Variaciones (fácil/difícil)
    - Tips de ejecución
    - Formaciones de grupo
    """
    try:
        logger.info(f"🕺 Generando coreografía: {request.tema}")
        
        from ..app import groq_client
        
        video_gen = VideoScriptGenerator(groq_client)
        
        resultado = video_gen.generate_choreography_guide(
            tema=request.tema,
            audiencia=request.audiencia,
            nivel_dificultad=request.nivel_dificultad,
            idioma=request.idioma,
            informacion_adicional=request.informacion_adicional
        )
        
        logger.info(f"✅ Coreografía generada exitosamente")
        return resultado
        
    except ConnectionError as e:
        logger.error(f"❌ Error de conexión LLM: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error generando coreografía: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/video/music-guide")
def generate_music_guide(request: MusicGuideRequest):
    """Generar guía de recomendaciones musicales para video
    
    Incluye:
    - Análisis del tema y emociones
    - Top 5 canciones recomendadas con links
    - Alternativas sin copyright
    - Soundtracks y efectos de sonido
    - Tips de sincronización
    """
    try:
        logger.info(f"🎵 Generando guía musical: {request.tema}")
        
        from ..app import groq_client
        
        video_gen = VideoScriptGenerator(groq_client)
        
        resultado = video_gen.generate_music_guide(
            tema=request.tema,
            plataforma=request.plataforma,
            genero=request.genero,
            idioma=request.idioma
        )
        
        logger.info(f"✅ Guía musical generada exitosamente")
        return resultado
        
    except ConnectionError as e:
        logger.error(f"❌ Error de conexión LLM: {str(e)}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error generando guía musical: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/video/platforms")
def get_supported_video_platforms():
    """Obtener lista de plataformas de video soportadas"""
    return {
        "platforms": [
            {
                "id": "youtube",
                "nombre": "YouTube",
                "duracion_minutos": {"min": 2, "max": 60},
                "formato": "Horizontal (16:9)",
                "descripcion": "Videos largos y detallados"
            },
            {
                "id": "youtube_shorts",
                "nombre": "YouTube Shorts",
                "duracion_minutos": {"min": 0.15, "max": 1},
                "formato": "Vertical (9:16)",
                "descripcion": "Videos cortos rápidos y dinámicos"
            },
            {
                "id": "tiktok",
                "nombre": "TikTok",
                "duracion_minutos": {"min": 0.15, "max": 10},
                "formato": "Vertical (9:16)",
                "descripcion": "Contenido viral, muy dinámico"
            },
            {
                "id": "instagram_reels",
                "nombre": "Instagram Reels",
                "duracion_minutos": {"min": 0.15, "max": 3},
                "formato": "Vertical (9:16)",
                "descripcion": "Contenido visualmente atractivo"
            }
        ]
    }


@router.get("/video/styles")
def get_video_styles():
    """Obtener estilos de video disponibles"""
    return {
        "estilos": [
            "Educativo",
            "Entretenimiento",
            "Tutorial",
            "Lifestyle",
            "Motivacional",
            "Comedy",
            "Drama",
            "Reviews",
            "Vlogs",
            "Trailers"
        ]
    }


@router.post("/generate-video-script")
def generate_video_script(request: GenerateRequest):
    """
    Endpoint para generar guiones de video con coreografía, música, transiciones, etc.
    Soporta YouTube, TikTok y YouTube Shorts
    """
    try:
        logger.info(f"📹 Generando guion de video para: tema={request.tema}, plataforma={request.plataforma}")
        
        # Validar que sea una plataforma de video
        video_platforms = ["tiktok", "youtube", "youtube_shorts"]
        if request.plataforma.lower() not in video_platforms:
            raise ValueError(f"Plataforma '{request.plataforma}' no es válida para videos. Usa: {video_platforms}")
        
        # Lazy import
        from ..services.video_script_generator import VideoScriptGenerator
        from ..app import groq_client
        
        video_generator = VideoScriptGenerator(llm_client=groq_client)
        
        # Generar el guion de video completo
        video_script = video_generator.generate_video_script(
            tema=request.tema,
            plataforma=request.plataforma,
            audiencia=request.audiencia,
            idioma=request.idioma,
            informacion_adicional=request.informacion_adicional
        )
        
        logger.info(f"✅ Guion de video generado exitosamente")
        
        return {
            "status": "success",
            "video_script": video_script,
            "metadata": {
                "tema": request.tema,
                "plataforma": request.plataforma,
                "audiencia": request.audiencia,
                "idioma": request.idioma,
                "tipo": "guion_de_video_completo"
            }
        }
        
    except ValueError as e:
        logger.error(f"❌ Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error generando guion de video: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generando guion de video: {str(e)}")
