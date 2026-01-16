# Decorador tool que toma analisis de imagen + style preferences. 
# Devuelve prompt optimizado para HF API
from crewai.tools import tool

@tool
def prompt_refinement_tool(image_analysis: str, style: str) -> str:
    """ 
    Toma analisis de imagen + preferencia de estilo
    Devuelve prompt optimizado para HF Stable Diffusion
    """
    return f"{image_analysis}. Estilo: {style}"