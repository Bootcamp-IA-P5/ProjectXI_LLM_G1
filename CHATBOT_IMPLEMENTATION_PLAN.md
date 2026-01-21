# 📋 Plan de Implementación: Módulo Chatbot Conversacional

**Fecha creación:** 19 de Enero 2026  
**Estado:** Planificación  
**Prioridad:** Media  
**Estimado:** 4-6 horas de desarrollo

---

## 📌 Resumen Ejecutivo

Implementar un módulo de chat conversacional que permita a los usuarios interactuar iterativamente con la IA, refinar contenido generado, hacer preguntas de seguimiento, y mantener contexto de la conversación.

**Ventajas principales:**
- Mejor UX con interacción iterativa
- Mayor retención de usuarios (chat es "sticky")
- Posibilidad de refinar contenido sin empezar de cero
- Diferenciación vs generadores simples

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
├─────────────────────────────────────────────────────────────┤
│  ContentForm (existente) │ ChatBot (nuevo)                   │
│                                                              │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ Generador Rápido │    │ Chat Conversacional          │  │
│  │ - Form           │    │ - Message History            │  │
│  │ - Output         │    │ - Input + Send               │  │
│  └──────────────────┘    │ - Context Management         │  │
│                          └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕ (HTTP)
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
├─────────────────────────────────────────────────────────────┤
│  /api/generate (existente) │ /api/chat (nuevo)              │
│                                                              │
│  POST /api/generate                                         │
│  └─ tema, plataforma, audiencia → contenido + imagen       │
│                                                              │
│  POST /api/chat                                             │
│  └─ mensaje, historial → respuesta + imagen (opcional)     │
│                                                              │
│  GroqClient + Gemini Fallback                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Fase 1: Frontend - Crear Componente ChatBot

### 1.1 Crear archivo: `frontend/src/components/ChatBot.jsx`

**Responsabilidades:**
- Mostrar historial de mensajes
- Input para enviar nuevos mensajes
- Gestionar estado de conversación
- Mostrar imágenes generadas (si aplica)

**Estructura de estado necesaria:**

```javascript
// Estados a gestionar:
const [messages, setMessages] = useState([]); // Historial
const [inputValue, setInputValue] = useState(""); // Texto actual
const [loading, setLoading] = useState(false); // Loading state
const [error, setError] = useState(""); // Errores
const [sessionId, setSessionId] = useState(generateId()); // Session única

// Estructura de mensaje:
/*
{
  id: "msg_12345",
  role: "user" | "assistant",
  content: "texto del mensaje",
  image_url?: "http://...", // opcional, solo en respuestas
  timestamp: Date,
  loading?: boolean // para mostrar spinner
}
*/
```

**Componentes internos a crear:**

```jsx
// Componentes sub:
- <MessageList /> - Lista de mensajes con scroll automático
- <MessageItem /> - Mensaje individual con imagen y contenido
- <ChatInput /> - Input + botón enviar
- <LoadingIndicator /> - Spinner mientras espera respuesta
```

### 1.2 Crear archivo: `frontend/src/components/MessageItem.jsx`

**Props:**
```javascript
{
  message: {
    id: string,
    role: "user" | "assistant",
    content: string,
    image_url?: string,
    timestamp: Date
  }
}
```

**Funcionalidades:**
- Diferenciar estilo entre usuario (derecha, azul) y asistente (izquierda, gris)
- Mostrar imagen si existe
- Timestamp formateado
- Opción de copiar texto (copy button)
- Opción de descargar imagen (download button)

### 1.3 Crear archivo: `frontend/src/components/ChatInput.jsx`

**Props:**
```javascript
{
  value: string,
  onChange: (text) => void,
  onSend: (text) => void,
  disabled: boolean,
  placeholder: string
}
```

**Funcionalidades:**
- Input text multiline
- Botón Send
- Ctrl+Enter para enviar (UX mejorada)
- Auto-clear después de enviar
- Disable durante loading

### 1.4 Crear estilos: `frontend/src/styles/ChatBot.css`

**Componentes a estilizar:**
```css
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-secondary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  animation: slideIn 0.3s ease-out;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 1rem;
  border-radius: 12px;
  word-wrap: break-word;
}

.message.user .message-bubble {
  background: var(--primary-color);
  color: white;
}

.message.assistant .message-bubble {
  background: var(--bg-tertiary);
  color: var(--text-color);
}

.message-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 0.5rem;
  cursor: pointer;
}

.chat-input-area {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 0.75rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  resize: none;
  max-height: 120px;
  font-family: inherit;
  font-size: 0.95rem;
}

.send-button {
  padding: 0.75rem 1.5rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.send-button:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 1.5 Actualizar `frontend/src/App.jsx`

**Cambios:**
```javascript
// Agregar nuevo estado para mostrar ChatBot
const [showChatMode, setShowChatMode] = useState(false);

// Agregar toggle button en header
<button className="mode-toggle" onClick={() => setShowChatMode(!showChatMode)}>
  {showChatMode ? "📝 Generador" : "💬 Chat"}
</button>

// Condicional render
{showChatMode ? (
  <ChatBot />
) : (
  <div className="content-wrapper">
    {/* modo generador existente */}
  </div>
)}
```

### 1.6 Crear servicio: `frontend/src/services/chatService.js`

```javascript
export async function sendChatMessage(message, sessionId, chatHistory = []) {
  const url = 'http://localhost:5001/api/chat';

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        session_id: sessionId,
        chat_history: chatHistory, // historial anterior
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Error del servidor");
    }

    const result = await response.json();
    return result;

  } catch (error) {
    console.error("❌ ERROR EN CHAT SERVICE:", error);
    throw error;
  }
}
```

---

## 🛠️ Fase 2: Backend - Crear Endpoint Chat

### 2.1 Actualizar `backend/routes/api.py`

**Agregar nuevo modelo Pydantic:**

```python
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    """Estructura de un mensaje en el chat"""
    role: str  # "user" o "assistant"
    content: str
    timestamp: Optional[str] = None
    image_url: Optional[str] = None

class ChatRequest(BaseModel):
    """Request para endpoint /api/chat"""
    message: str  # mensaje actual del usuario
    session_id: str  # ID de sesión para tracking
    chat_history: List[ChatMessage] = []  # historial previo
    generate_image: bool = True  # si generar imagen o no
```

### 2.2 Crear nuevo endpoint `/api/chat`

**Ubicación:** En `backend/routes/api.py` después del endpoint `/generate`

```python
@router.post("/chat")
def chat_generate(request: ChatRequest):
    """
    Endpoint de chat conversacional
    
    Recibe:
    - message: el mensaje actual del usuario
    - session_id: para agrupar conversación
    - chat_history: historial anterior (para contexto)
    - generate_image: si generar imagen (True/False)
    
    Devuelve:
    - response: respuesta del asistente
    - image_url: imagen generada (si aplica)
    - session_id: para mantener tracking
    """
    
    try:
        logger.info(f"💬 Chat recibido - Session: {request.session_id}")
        logger.info(f"📝 Mensaje: {request.message[:100]}...")
        
        # Validar mensaje no vacío
        if not request.message or request.message.strip() == "":
            raise ValueError("El mensaje no puede estar vacío")
        
        # Construir contexto del chat (incluir historial)
        context_messages = []
        
        # Agregar historial previo como contexto
        for msg in request.chat_history:
            context_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Agregar mensaje actual
        context_messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Construir prompt con contexto
        system_prompt = """Eres un asistente de generación de contenido experto.
        Tu tarea es:
        1. Responder preguntas sobre contenido
        2. Refinar contenido generado anteriormente
        3. Ofrecer mejoras y sugerencias
        4. Mantener coherencia con la conversación anterior
        
        Sé amable, profesional y conciso."""
        
        # Lazy import
        from ..app import groq_client
        
        logger.info("⏳ Enviando a Groq con contexto...")
        
        # Usar groq_client para generar respuesta
        # Nota: groq_client.generate() recibe string simple, así que concatenamos
        full_prompt = system_prompt + "\n\n" + request.message
        response_text = groq_client.generate(full_prompt)
        
        logger.info(f"✅ Respuesta Groq: {response_text[:100]}...")
        
        # Si el usuario pidió imagen, generar
        image_url = None
        if request.generate_image:
            try:
                # Usar el mensaje actual para generar prompt de imagen
                image_prompt = f"Create a professional image for: {request.message}"
                image_url = generate_image(image_prompt, width=1024, height=1024)
                logger.info(f"🖼️ Imagen generada: {image_url}")
            except Exception as e:
                logger.warning(f"⚠️ Error generando imagen: {str(e)}")
                image_url = None
        
        # Construir respuesta
        response = {
            "response": response_text,
            "image_url": image_url,
            "session_id": request.session_id,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"📤 Chat response generado")
        return response
    
    except ValueError as e:
        logger.error(f"❌ Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error en chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

### 2.3 Agregar función helper en `backend/services/`

**Archivo:** `backend/services/chat_manager.py` (nuevo)

```python
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class ChatSessionManager:
    """Gestor de sesiones de chat"""
    
    def __init__(self):
        # En producción usar Redis o DB
        self.sessions = {}
    
    def create_session(self, session_id: str):
        """Crear nueva sesión"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "created_at": datetime.now(),
                "messages": [],
                "metadata": {}
            }
            logger.info(f"✅ Nueva sesión creada: {session_id}")
    
    def add_message(self, session_id: str, role: str, content: str, image_url: str = None):
        """Agregar mensaje a sesión"""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = {
            "role": role,
            "content": content,
            "image_url": image_url,
            "timestamp": datetime.now().isoformat()
        }
        
        self.sessions[session_id]["messages"].append(message)
        logger.info(f"📝 Mensaje agregado a sesión {session_id}")
    
    def get_session_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Obtener historial de sesión"""
        if session_id not in self.sessions:
            return []
        
        messages = self.sessions[session_id]["messages"]
        return messages[-limit:]  # Últimos 10 mensajes
    
    def clear_session(self, session_id: str):
        """Limpiar sesión"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"🗑️ Sesión eliminada: {session_id}")

# Instancia global
chat_manager = ChatSessionManager()
```

---

## 📊 Fase 3: Integración Frontend-Backend

### 3.1 Implementar ChatBot.jsx completo

```javascript
import { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/chatService';
import MessageItem from './MessageItem';
import ChatInput from './ChatInput';
import '../styles/ChatBot.css';

function generateSessionId() {
  return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

export default function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sessionId] = useState(() => generateSessionId());
  const messagesEndRef = useRef(null);

  // Auto-scroll a último mensaje
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  async function handleSendMessage(text) {
    if (!text.trim()) return;

    // Agregar mensaje del usuario
    const userMessage = {
      id: 'msg_' + Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setLoading(true);
    setError("");

    try {
      // Enviar a backend
      const response = await sendChatMessage(
        text,
        sessionId,
        messages.map(m => ({
          role: m.role,
          content: m.content,
          image_url: m.image_url
        }))
      );

      // Agregar respuesta del asistente
      const assistantMessage = {
        id: 'msg_' + Date.now(),
        role: 'assistant',
        content: response.response,
        image_url: response.image_url,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (err) {
      console.error("Error:", err);
      setError(err.message || "Error desconocido");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>💬 Chat Conversacional</h2>
        <p className="session-id">Sesión: {sessionId}</p>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty-state">
            <p>Inicia una conversación con el asistente IA</p>
          </div>
        ) : (
          messages.map(msg => (
            <MessageItem key={msg.id} message={msg} />
          ))
        )}
        {loading && (
          <div className="message assistant">
            <div className="loading-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && (
        <div className="chat-error">
          <span>❌ {error}</span>
          <button onClick={() => setError("")}>✕</button>
        </div>
      )}

      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSendMessage}
        disabled={loading}
        placeholder="Escribe tu pregunta o instrucción..."
      />
    </div>
  );
}
```

---

## 🔄 Fase 4: Testing & Validación

### 4.1 Test manual del flujo completo

**Pasos:**
1. Abre el navegador en http://localhost:3000
2. Cambia a modo Chat (botón toggle)
3. Envía primer mensaje: "Ayúdame a generar contenido sobre machine learning"
4. Espera respuesta
5. Envía seguimiento: "Hazlo más técnico"
6. Verifica que el contexto se mantiene
7. Solicita imagen: "Genera una imagen para este contenido"

### 4.2 Test backend directo

```bash
# Test con curl
curl -X POST http://localhost:5001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, quiero contenido sobre IA",
    "session_id": "test_session_1",
    "chat_history": [],
    "generate_image": true
  }'
```

### 4.3 Verificar logs

```bash
# Tail de logs del backend
tail -f logs/backend.log

# Buscar en logs
grep "Chat recibido" logs/backend.log
```

---

## 🚀 Fase 5: Deployment & Consideraciones

### 5.1 Variables de entorno necesarias

```bash
# Asegurar que existan en .env
GROQ_API_KEY=<tu_key>
GOOGLE_API_KEY=<tu_key>
REPLICATE_API_TOKEN=<tu_key>
BACKEND_URL=http://localhost:5001
```

### 5.2 Mejoras futuras

#### Corto plazo (Semana 1):
- [ ] Persistencia de sesiones (guardar en BD)
- [ ] Exportar conversación a PDF
- [ ] Listar historial de sesiones anteriores
- [ ] Búsqueda en chat history

#### Mediano plazo (Semana 2-3):
- [ ] Agregar RAG (Retrieval Augmented Generation)
- [ ] Context window management (limitar tokens)
- [ ] Typing indicator más realista
- [ ] Voice input/output
- [ ] Compartir conversaciones

#### Largo plazo (Mes 2):
- [ ] Multi-agent orchestration
- [ ] Fine-tuning de modelos
- [ ] Análisis de conversaciones
- [ ] Recomendaciones inteligentes
- [ ] Integración con bases de datos de documentos

### 5.3 Consideraciones técnicas importantes

**Token Management:**
```python
# Groq tiene límites de tokens por minuto
# Implementar rate limiting:
from functools import wraps
from datetime import datetime, timedelta

def rate_limit(max_requests=10, window=60):
    """Limitar requests por ventana de tiempo"""
    requests = {}
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = datetime.now()
            key = str(args) + str(kwargs)
            
            if key not in requests:
                requests[key] = []
            
            requests[key] = [
                req for req in requests[key]
                if now - req < timedelta(seconds=window)
            ]
            
            if len(requests[key]) >= max_requests:
                raise Exception("Rate limit exceeded")
            
            requests[key].append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

**Memory Management:**
```python
# Chat history puede crecer mucho
# Implementar cleanup:
from datetime import datetime, timedelta

def cleanup_old_sessions(max_age_hours=24):
    """Limpiar sesiones antiguas"""
    now = datetime.now()
    
    sessions_to_delete = []
    for session_id, session in chat_manager.sessions.items():
        age = now - session["created_at"]
        if age > timedelta(hours=max_age_hours):
            sessions_to_delete.append(session_id)
    
    for session_id in sessions_to_delete:
        chat_manager.clear_session(session_id)
        logger.info(f"Sesión antigua eliminada: {session_id}")
```

---

## 📝 Checklist de Implementación

### Frontend
- [ ] Crear `ChatBot.jsx` con estado y lógica
- [ ] Crear `MessageItem.jsx` para renderizar mensajes
- [ ] Crear `ChatInput.jsx` para input de usuario
- [ ] Crear `chatService.js` con función `sendChatMessage()`
- [ ] Crear `ChatBot.css` con estilos
- [ ] Agregar toggle button en `App.jsx`
- [ ] Integrar modo chat en layout principal
- [ ] Probar renderizado de mensajes
- [ ] Probar scroll automático
- [ ] Probar envío de mensajes

### Backend
- [ ] Crear modelos Pydantic (`ChatMessage`, `ChatRequest`)
- [ ] Implementar endpoint `/api/chat` en `api.py`
- [ ] Crear `chat_manager.py` para gestionar sesiones
- [ ] Agregar logging detallado
- [ ] Implementar manejo de errores
- [ ] Probar endpoint con curl
- [ ] Verificar respuestas del Groq
- [ ] Implementar generación de imágenes (opcional)
- [ ] Agregar validaciones

### Testing
- [ ] Test manual: flujo completo
- [ ] Test: mensaje sin contexto
- [ ] Test: mensaje con contexto anterior
- [ ] Test: generación de imagen
- [ ] Test: error handling
- [ ] Test: session management
- [ ] Verificar logs en ambos lados

### Documentación
- [ ] Actualizar README con nuevo endpoint
- [ ] Documentar estructura de datos
- [ ] Crear ejemplos de API calls
- [ ] Documentar variables de entorno

---

## 📚 Referencias & Recursos

### Documentación oficial
- FastAPI: https://fastapi.tiangolo.com/
- React Hooks: https://react.dev/reference/react
- Groq API: https://console.groq.com/docs

### Ejemplos útiles

**Gestionar multiple requests:**
```javascript
// Frontend - Debounce para evitar spam
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);
  
  return debouncedValue;
}
```

**Persistencia en localStorage:**
```javascript
// Guardar messages
useEffect(() => {
  localStorage.setItem(`chat_${sessionId}`, JSON.stringify(messages));
}, [messages, sessionId]);

// Cargar messages
useEffect(() => {
  const saved = localStorage.getItem(`chat_${sessionId}`);
  if (saved) setMessages(JSON.parse(saved));
}, [sessionId]);
```

---

## 🎓 Notas de Aprendizaje

### Conceptos clave
1. **Session Management**: Agrupar mensajes relacionados
2. **Context Window**: No todos los LLMs soportan contexto infinito
3. **Streaming**: Para mejor UX, considerar respuestas en stream
4. **Rate Limiting**: Proteger API de abuso
5. **Persistent Storage**: Para historial duradero

### Posibles problemas y soluciones

| Problema | Causa | Solución |
|----------|-------|----------|
| Respuestas lentas | Token limit de Groq | Reducir historial, usar streaming |
| Pérdida de contexto | Session ID incorrecto | Validar session_id en cada request |
| Errores CORS | Frontend en puerto diferente | Configurar CORS en FastAPI |
| Imagen no carga | URL relativa vs absoluta | Verificar base URL en backend |
| Chat desorganizado | Sin scroll automático | Implementar useRef + scrollIntoView |

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs del backend**: `tail -f logs/`
2. **Revisar console del navegador**: F12 → Console
3. **Probar endpoint directamente**: `curl` o Postman
4. **Verificar variables de entorno**: `echo $GROQ_API_KEY`
5. **Buscar en documentación**: Links en Referencias

---

**Última actualización:** 19 de Enero 2026  
**Versión del plan:** 1.0
