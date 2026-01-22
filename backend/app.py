from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv
import logging


load_dotenv()
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# Crear app FastAPI
# ============================================
app = FastAPI(
    title="ProjectXI LLM API",
    description="API para generar contenido con LLMs",
    version="1.0.0"
)
# ============================================
# Instanciar cliente LLM global
# ============================================
from llm.groq_client import GroqClient
from services.content_generator import ContentGenerator
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    logger.warning("⚠️ GROQ_API_KEY no encontrada en .env")

groq_client = GroqClient(api_key=groq_api_key)
content_generator = ContentGenerator(groq_client) 

logger.info("✅ Clientes LLM inicializados")

# ============================================
# CORS - permitir conexiones desde frontend
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "http://localhost:5001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("✅ CORS configurado")

# ============================================
# archivos estaticos de imagenes generadas
# ============================================
image_dir = Path(__file__).parent / "generated_images"
image_dir.mkdir(exist_ok=True)
app.mount("/generated_images", StaticFiles(directory=str(image_dir)), name="generated_images")

logger.info(f"✅ Directorio de imágenes: {image_dir}")

# ============================================
# Registrar rutas
# ============================================
from routes.api import router
app.include_router(router)

logger.info("✅ Rutas registradas")

# ============================================
# Endpoint raíz
# ============================================
@app.get("/")
def root():
    """Endpoint raíz de la API"""
    return {
        "message": "ProjectXI LLM API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check
@app.get("/health")
def health():
    """Endpoint para verificar que la API está viva"""
    return {"status": "ok"}

# ============================================
# Entry point
# ============================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)