# Rol "Refina prompt de generacion de imagen desde el contenido"
# Modelo gemini 2.5 flash
from crewai import Agent
from tools.prompt_refinement_tool import prompt_refinement_tool
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Crear instancia del LLM correctamente
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
)

gemini_agent = Agent(
    role="Refine image generation prompt from content",
    goal="Refine prompts for image generation based on content analysis, ensuring the image description matches the content provided",
    backstory="Expert at visual storytelling and creating coherent visual representations that align with written content",
    tools=[prompt_refinement_tool],
    llm=gemini_llm,
    verbose=True
)