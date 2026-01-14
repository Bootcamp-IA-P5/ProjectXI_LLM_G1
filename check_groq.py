from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=128,
    stop_sequences=None,
)

resp = llm.invoke("Dime un saludo breve en español.")
print(resp.content)