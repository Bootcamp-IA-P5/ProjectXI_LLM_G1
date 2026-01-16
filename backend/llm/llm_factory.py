import os

def get_llm_client(LLM_PROVIDDER):
    if LLM_PROVIDDER == "Groq":
        from llm.groq_client import GroqClient
        grok_key = os.getenv("GROQ_API_KEY")
        if not grok_key:
            raise ValueError("GROQ_API_KEY no está configurada en las variables de entorno")
    return GroqClient