# Rol "Refina prompt de generacion de imagen desde el contenido"
# Modelo gemini 2.5 flash
from crewai import Agent
from tools.prompt_refinement_tool import prompt_refinement_tool
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

try:
    # USAR CUALQUIERA DE ESTAS VARIABLES
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("⚠️ GOOGLE_API_KEY/GEMINI_API_KEY no configurada. CrewAI desactivado.")
        gemini_llm= None
    else:
    # Crear instancia del LLM correctamente
        gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=api_key,
            temperature=0.3,
        )
        logger.info("✅ Gemini LLM inicializado")

    gemini_agent = Agent(
        role="Image Prompt Optimizer",
        goal="Refine and optimize image generation prompts based on content context",
        backstory="Expert at creating detailed, vivid image descriptions that align with content topics",
        tools=[prompt_refinement_tool],
        llm=gemini_llm,
        verbose=True
    ) if gemini_llm else None 

except Exception as e:
    logger.error(f"❌ Error inicializando Gemini Agent: {str(e)}")
    gemini_agent = None