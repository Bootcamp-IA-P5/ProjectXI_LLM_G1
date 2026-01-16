from crewai.tools import tool
from llm.gemini_client import Client
import os

@tool
def image_analysis_tool(image_path: str) -> str:
    """
    Analiza una imagen usando el cliente Gemini
    
    Args:
        image_path: Ruta a la imagen
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    gemini_client = Client(api_key, "gemini-2.5-flash")
    
    return gemini_client.analyze_image(image_path, "Describe this image for visual content generation")