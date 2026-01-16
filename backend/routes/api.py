from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
from agents.crew import run_crew
from services.image_generator import generate_image
from rag.rag_system import RAGSystem
import logging

# Instanciar RAG globalmente
rag_system = RAGSystem()

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


# @router.post("/generate")
# def generate_content(request: GenerateRequest):
    
#     try: 
#         # Usar factory en lugar de crear OllamaClient directamente
#         llm_client = get_llm_client(os.getenv("LLM_PROVIDER"))
#         generator = ContentGenerator(llm_client)
        
#         contenido = generator.generate_content(
#             tema = request.tema,
#             plataforma = request.plataforma,
#             audiencia = request.audiencia,
#             informacion_adicional = request.informacion_adicional
#         )
        
#         return {"contenido": contenido, "status": "success"}
    
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail = str(e))
    
#     except ConnectionError as e:
#         raise HTTPException(status_code=503, detail = str(e))
    
#     except Exception as e:
#         logger.error(f"Error generando contenido: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error interno del servidor")
    
@router.post("/crew/generate")
def crew_generate(request: GenerateRequest): # Pydantic model
    """Endpoint multiagente: Groq >> Gemini >> Imagen HF"""
    
    try:    
                    
        #Groq genera contenido (KAS)
        # contenido = groq_agent.generate(request.tema, request.plataforma..)
        contenido = f"Contenido sobre {request.tema} para {request.plataforma}"
        
        # Detectar si es cientifico para RAG
        temas_cientificos = ["inteligencia artificial", "ia", "clima", "cambio climático", 
                             "biomedicina", "astrofísica", "física cuántica", "medio ambiente"]
        es_cientifico = any(tema.lower() in request.tema.lower() for tema in temas_cientificos)
        
        # Si es cientifico, usar RAG
        contexto_cientifico = ""
        if es_cientifico:
            contexto_cientifico = rag_system.process_query(request.tema)
            if contexto_cientifico:
                logger.info("✅ RAG activado: Usando contexto científico")
            else:
                logger.warning("⚠️ RAG fallback: Sin papers disponibles")
                
        # Inyectar contexto en el prompt para Gemini
        contenido_con_contexto = contenido
        if contexto_cientifico:
            contenido_con_contexto = f"{contenido}\n\n{contexto_cientifico}"

        
        #Gemini refina prompt (ahora con contexto cientifico)
        prompt_refinado = run_crew (
            tema=request.tema,
            plataforma=request.plataforma,
            audiencia=request.audiencia,
            contenido_groq=contenido_con_contexto,
            contexto_marca=request.contexto_marca
        )
        
        # Backend genera imagen con tamaño segun plataforma
        size = PLATFORM_SIZES.get(request.plataforma, {"width": 1024, "height": 1024})
        image_url = generate_image(
            prompt_refinado, 
            width=size["width"], 
            height=size["height"])
            
            
        return {
            "contenido": contenido, 
            "image_url": image_url,
            "status": "success",
            "rag_activated": es_cientifico and bool(contexto_cientifico) # Opcional: avisar al frontend
        }
    
    except Exception as e:
        logger.error(f"Error en Crew generation: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    