# Orquestador que instancia Crew() con gemini_agent, define Task para analisis visual.
# Metodo principal run_crew (user_input) que devuelve resultado
from crewai import Crew, Task
from agents.gemini_agent import gemini_agent
    
def run_crew (tema: str, plataforma: str, audiencia: str, contenido_groq: str = None):
    """
    Ejecuta el crew multiagente
    -Gemini refina prompt para imagen (si se requiere)
    -Image generator crea la imagen
    """
    
    #Task 1: gemini refina prompt (basado en contenido de Groq)
    task_gemini = Task (
        description=f"Refina prompt para generar imagen sobre {tema} para {plataforma}",
        agent = gemini_agent,
        expected_output="Prompt optimizado para Hugging Face"
    )
    
    crew = Crew(
        agents=[gemini_agent],
        tasks=[task_gemini],
        verbose = True
    )
    
    result = crew.kickoff(inputs={
        "tema": tema,
        "plataforma": plataforma,
        "audiencia": audiencia,
        "content": contenido_groq
    })
    
    prompt_refinado = result.raw
    
    return prompt_refinado