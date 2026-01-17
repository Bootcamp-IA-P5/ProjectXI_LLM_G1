1029# ProjectXI LLM - Content Generation with AI

**Generación de contenido inteligente con múltiples proveedores LLM y generación de imágenes.**

---

## 🎯 Descripción General

ProjectXI es una aplicación full-stack que genera contenido personalizado para diferentes plataformas (Twitter, Instagram, LinkedIn, etc.) utilizando:

- **Backend**: FastAPI + Agentes de IA (Groq, Gemini)
- **Frontend**: React con diseño profesional y responsivo
- **LLM Providers**: Groq, Google Gemini, Ollama
- **Image Generation**: Hugging Face

---

## ✨ Características Principales

```
✅ Generación de contenido multiagente
✅ Soporte para múltiples plataformas (6 opciones)
✅ Generación automática de imágenes
✅ Validación robusta de formularios
✅ Interfaz moderna y responsiva
✅ API REST bien documentada
✅ Orquestación de agentes con CrewAI
✅ Patrón Factory para gestión de LLMs
```

---

## 📁 Estructura del Proyecto

```
ProjectXI_LLM_G1/
├── backend/                    # API FastAPI
│   ├── agents/                # Agentes IA
│   ├── llm/                   # Clientes LLM
│   ├── routes/                # Endpoints API
│   ├── services/              # Servicios de negocio
│   ├── tools/                 # Herramientas IA
│   ├── app.py                # Aplicación principal
│   └── Dockerfile
│
├── frontend/                   # Aplicación React
│   ├── src/
│   │   ├── components/        # Componentes React
│   │   ├── services/          # Servicios HTTP
│   │   ├── styles/            # Estilos CSS
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
│
├── tests/                      # Suite de pruebas
├── docker-compose.yml         # Orquestación Docker
├── requirements.txt           # Dependencias Python
├── README.md                  # Este archivo
├── FRONTEND.md                # Documentación frontend
└── CAMBIOS_REALIZADOS.md      # Resumen de refactoring
```

---

## 🚀 Quick Start

### Requisitos
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose (opcional)
- API Keys: Groq, Gemini, Hugging Face

### Instalación Local

#### 1. Backend
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

#### 2. Frontend
```bash
cd frontend
npm install
```

#### 3. Ejecutar
```bash
# Terminal 1 - Backend
python backend/app.py
# API disponible en http://localhost:5000

# Terminal 2 - Frontend
cd frontend
npm start
# Frontend disponible en http://localhost:3000
```

### Instalación con Docker
```bash
docker-compose up
# Backend: http://localhost:5002
# Frontend: http://localhost:3001
```

---

## 🔑 Variables de Entorno

```bash
# LLM Providers
GROQ_API_KEY=tu_clave_groq
GEMINI_API_KEY=tu_clave_gemini
LLM_PROVIDER=groq              # Provider por defecto

# Ollama (si usas local)
OLLAMA_BASE_URL=http://localhost:11434

# API Configuration
BACKEND_PORT=5000
```

Ver `.env.example` para todas las opciones.

---

## 📚 Documentación

### Frontend
Documentación completa en [FRONTEND.md](FRONTEND.md):
- Guía de colores y diseño
- Componentes y funcionalidades
- Personalización de estilos
- Responsividad

### Backend
Ver comentarios en el código:
- `backend/app.py` - Configuración principal
- `backend/routes/api.py` - Endpoints disponibles
- `backend/agents/` - Agentes IA
- `backend/llm/` - Configuración de LLMs

### Cambios y Refactoring
Ver [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md):
- Archivos eliminados y por qué
- Documentación consolidada
- Código completado y revisado
- Estructura final del proyecto

---

## 🔌 API Endpoints

### Health Check
```
GET /health
```

### Generación de Contenido
```
POST /api/crew/generate
Content-Type: application/json

{
  "tema": "Inteligencia Artificial",
  "plataforma": "twitter",
  "audiencia": "Desarrolladores",
  "informacion_adicional": "Enfocado en LLMs"
}
```

**Respuesta:**
```json
{
  "contenido": "Contenido generado por Groq...",
  "image_url": "URL de la imagen generada",
  "status": "success"
}
```

---

## 🧠 Arquitectura de Agentes

### Flujo de Generación
```
Frontend (Usuario)
    ↓
  FastAPI (Backend)
    ↓
  [Groq Agent] ← Genera contenido inicial
    ↓
  [Gemini Agent] ← Refina prompt para imagen
    ↓
  [HF Image Generator] ← Genera imagen
    ↓
  Frontend ← Muestra resultado
```

### Providers Disponibles
| Provider | Modelo | Uso |
|----------|--------|-----|
| **Groq** | mixtral-8x7b-32768 | Generación rápida de contenido |
| **Gemini** | gemini-pro | Refinamiento de prompts |
| **Ollama** | mistral | Local (desarrollo) |

---

## 🛠️ Desarrollo

### Agregar Nuevo Agente
1. Crear archivo en `backend/agents/`
2. Heredar de clase base si existe
3. Implementar interfaz necesaria
4. Registrar en `backend/agents/crew.py`

### Agregar Nuevo Endpoint
1. Crear función en `backend/routes/api.py`
2. Documentar con docstring
3. Validar entrada con Pydantic
4. Retornar respuesta tipada

### Personalizar Frontend
Ver [FRONTEND.md](FRONTEND.md) sección "Personalización".

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest tests/ --cov=backend

# Test específico
pytest tests/test_groq_agent.py -v
```

---

## 🐛 Solución de Problemas

### Error: "API key not found"
```
✓ Verificar .env tiene las keys configuradas
✓ Verificar que los archivos .env no están en .gitignore
✓ Reiniciar la aplicación después de cambiar .env
```

### Error: "Failed to connect to backend"
```
✓ Verificar que backend está corriendo en puerto 5000
✓ Revisar CORS en backend/app.py
✓ Verificar que frontend apunta a URL correcta
```

### Estilos CSS no se ven en frontend
```
✓ Limpiar caché: Ctrl+Shift+R en navegador
✓ Reiniciar npm: npm start
✓ Verificar imports en componentes
```

---

## 📊 Performance

### Optimizaciones implementadas
- ✅ Variables CSS centralizadas
- ✅ Lazy loading de componentes
- ✅ Caché de peticiones HTTP
- ✅ Compresión de imágenes generadas
- ✅ Rate limiting en API

---

## 🔐 Seguridad

```
✅ API keys en variables de entorno
✅ CORS configurado restrictivamente
✅ Validación de entrada con Pydantic
✅ Rate limiting en endpoints
✅ Sanitización de contenido
```

---

## 📦 Dependencias Principales

### Backend
```
fastapi==0.111.0
langchain==0.2.14
langchain-groq==0.1.6
crewai[google-genai]>=0.30.0
google-generativeai>=0.3.0
```

### Frontend
```
react==18.2.0
react-dom==18.2.0
react-scripts==5.0.1
```

Ver `requirements.txt` y `frontend/package.json` para lista completa.

---

## 🤝 Contribuir

1. Crear rama desde `dev`: `git checkout -b feature/nombre`
2. Hacer cambios y commits significativos
3. Push a rama: `git push origin feature/nombre`
4. Crear Pull Request contra `dev`
5. Pasar revisión de código

---

## 📝 Cambios Recientes

**Enero 17, 2026** - Refactoring y limpieza del repositorio:
- ✅ Eliminadas carpetas `src/` y `deprecated/` duplicadas
- ✅ Consolidada documentación en `FRONTEND.md`
- ✅ Revisado y confirmado código faltante funcional
- ✅ Actualizado estructura del proyecto
- ✅ Documentado en `CAMBIOS_REALIZADOS.md`

Ver [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md) para detalles completos.

---

## 📞 Soporte

Para más información:
- 📖 [FRONTEND.md](FRONTEND.md) - Documentación frontend
- 📋 [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md) - Refactoring realizado
- 💬 Revisar código comentado en archivos específicos
- 🐛 Consultar logs de error en consola

---

## 📄 Licencia

Proyecto educativo - Bootcamp IA 2026

---

**✨ ProjectXI LLM - Generación de contenido con IA**

*Rama: `feature/groq-agent-mvp`*  
*Última actualización: Enero 17, 2026*
