from fastapi import APIRouter, HTTPException
from pydantic import BaseModel # Para validar JSON
import os
from dotenv import load_dotenv
import logging

from llm.ollama_client import OllamaClient
from services.content_generator import ContentGenerator

logger = logging.getLogger(__name__)
load_dotenv()

router = APIRouter(prefix="/api", tags=["generation"])

class GenerateRequest(BaseModel):
    tema: str
    plataforma: str
    audiencia: str
    informacion_adicional: str = "" 
    
@router.post("/generate")
def generate_content(request: GenerateRequest):
        
    # Paso 1 Obtener variables, FUERA DEL TRY
    base_url = os.getenv("OLLAMA_BASE_URL")
    model = os.getenv("OLLAMA_MODEL")
    
    if not base_url or not model:
        raise ValueError("Variables de entorno no configuradas")
    
    try: 
        # Paso 2 Crear instancias
        # Crear OllamaClient (con variables de .env)
        # DENTRO DEL TRY YA QUE PUEDE FALLAR (ej si no recibe model)
        ollama_client = OllamaClient(base_url, model)
        generator = ContentGenerator(ollama_client)

        # Paso 3: generar
        contenido = generator.generate_content(
        tema = request.tema,
        plataforma = request.plataforma,
        audiencia = request.audiencia,
        informacion_adicional = request.informacion_adicional
        )
        # Paso 4: Retornar exito
        return {"contenido": contenido, "status": "success"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail = str(e))
    
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail = str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")