from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (para que frontend pueda llamar desde localhost:3000)
app.add_middleware (
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosForm(BaseModel):
    tema: str
    plataforma: str
    audiencia: str
    infoAdicional: Optional[str] = None # Opcional

@app.post("/api/generate")
async def generate_content(datos: DatosForm):
    print("✅ ENDPOINT LLAMADO")  # ← Para saber si llega
    print(f"Tema: {datos.tema}")
    print(f"Plataforma: {datos.plataforma}")
    print(f"Audiencia: {datos.audiencia}")
    
    #Recibir datos (objeto con los atributos)
    print(datos.tema)
    print(datos.audiencia)
    print(datos.plataforma)
    print(datos.infoAdicional)
    
    #validar
    if not datos.tema or datos.tema.strip() == "":
        raise HTTPException(status_code=400, detail="El tema no puede estar vacio")
    
    if not datos.audiencia or datos.audiencia.strip() == "":
        raise HTTPException(status_code=400, detail="La audiencia no puede estar vacia")
    
    if not datos.plataforma or datos.plataforma.strip() == "":
        raise HTTPException(status_code=400, detail="La plataforma no puede estar vacia")

    # Mock response (sin LLM aún)
    contenido_mock = f"Tweet para {datos.plataforma} dirigido a {datos.audiencia} sobre {datos.tema}"
    
    return {
        "contenido": contenido_mock,
        "status": "success"
    }