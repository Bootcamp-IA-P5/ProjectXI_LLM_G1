# Orquestador que instancia Crew() con gemini_agent, define Task para analisis visual.
# Metodo principal run_crew (user_input) que devuelve resultado
from crewai import Crew, Task
from agents.gemini_agent import gemini_agent
import logging

logger = logging.getLogger(__name__)

def run_crew (tema: str, plataforma: str, audiencia: str, contenido_groq: str = None, contexto_marca: str = ""):
    """
    Ejecuta el crew multiagente
    -Gemini refina prompt para imagen (si se requiere)
    -Image generator crea la imagen
    """
    try: 
        logger.info("🤖 Iniciando CrewAI...")
        #Task 1: gemini refina prompt (basado en contenido de Groq)
        task_gemini = Task (
            description=f"Refina prompt para generar imagen sobre {tema} para {plataforma}. Contexto de marca: {contexto_marca} ",
            agent = gemini_agent,
                expected_output="Prompt optimizado para generación de imagen (máx 150 palabras)"
        )
        
        crew = Crew(
            agents=[gemini_agent],
            tasks=[task_gemini],
            verbose = True
        )

        # Ejecutar
        logger.info("⏳ Ejecutando crew...")
        result = crew.kickoff(inputs={
            "tema": tema,
            "plataforma": plataforma,
            "audiencia": audiencia,
            "content": contenido_groq or f"Contenido sobre {tema}",
            "contexto_marca": contexto_marca
        })
        
        # Extraer resultado
        prompt_refinado = result.raw if hasattr(result, 'raw') else str(result)
        logger.info(f"✅ CrewAI completado: {prompt_refinado[:80]}...")
        
        return prompt_refinado
            
    except Exception as e:
        logger.error(f"❌ Error en CrewAI: {str(e)}")
        # Fallback: retornar prompt básico
        return f"High quality {plataforma} image about {tema}, professional design, 4K quality, suitable for {audiencia}"