# Rol "Refina prompt de generacion de imagen desde el contenido"
# Modelo gemini 2.5 flash
from crewai import Agent
from tools.prompt_refinement_tool import prompt_refinement_tool
import os

gemini_agent = Agent(
    role="Refine image generation prompt from content",
    goal="Refine prompts for image generation based on content analysis",
    backstory="Expert at visual storytelling",
    tools=[prompt_refinement_tool],
    llm=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
)