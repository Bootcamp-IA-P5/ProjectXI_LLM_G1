# Llama a Hugging Face API con prompt, input texto prompt output URL/bytes imagen
from huggingface_hub import InferenceClient
import os
import logging
import glob
import time
from datetime import datetime
from uuid import uuid4
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

#Crear directorio para imagenes, si no existe
os.makedirs("generated_images", exist_ok=True)

# Metodo para eliminar imagenes de mas de 7 dias
def cleanup_old_images(days: int=7):
    try:
        cutoff_time= time.time() - (days * 86400)
        for filepath in glob.glob("generated_images/*.png"):
            os.remove(filepath)
            logger.info(f"Imagen eliminada: {filepath}")
    except Exception as e:
        logger.warning(f"Error limpiando imágenes antiguas: {str(e)}")


def generate_image(prompt: str, width: int = 1024, height: int = 1024) -> str:
    """ 
    Genera imagen from prompt using Hugging Face Stable Diffusion
    
    Args: 
        prompt: Image generation prompt
        width & height:
    
    Returns:
        Image URL from HF or placeholder
    """
    
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    
    # Si no hay token, retornar un placeholder
    if not hf_token:
        logger.warning("HUGGINGFACE_API_TOKEN no configurado. Retornando placeholder de imagen.")
        return f"https://via.placeholder.com/{width}x{height}?text={prompt[:30].replace(' ', '+')}"
    
    #Limpiar imagenes antiguas antes de generar
    cleanup_old_images()
    
    try:
        # Instanciar cliente de HF
        client = InferenceClient(api_key=hf_token)        
        
        # Generar imagen
        image = client.text_to_image(
            prompt=prompt,
            model=os.getenv("HF_MODEL", "stabilityai/stable-diffusion-xl-base-1.0"),
            height=height,
            width=width
        )
        
        # Generar nombre unico
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}.png"
        filepath = os.path.join("generated_images", filename)

        # Guardar imagen
        image.save(filepath)
        logger.info(f"Imagen guardada: {filepath}")
        
        # Devolver ruta para acceso HTTP
        return f"/generated_images/{filename}"
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error generando imagen en HF: {error_msg}")
        
        # Errores específicos de HF para debugging
        if "401" in error_msg or "Unauthorized" in error_msg:
            raise Exception("HF_AUTH_ERROR: Token inválido o expirado")
        elif "429" in error_msg or "rate" in error_msg.lower():
            raise Exception("HF_RATE_LIMIT: Cuota de API excedida")
        elif "timeout" in error_msg.lower() or "time out" in error_msg.lower():
            raise Exception("HF_TIMEOUT: Servidor de HF no responde")
        elif "model" in error_msg.lower() or "not found" in error_msg.lower():
            raise Exception("HF_MODEL_ERROR: Modelo no disponible")
        else:
            raise Exception(f"HF_ERROR: {error_msg}")
    