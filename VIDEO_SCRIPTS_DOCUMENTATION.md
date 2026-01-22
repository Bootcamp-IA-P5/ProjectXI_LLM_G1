# 🎬 Video Script Generation - Documentación

## Visión General

El sistema ahora puede generar **guiones completos y guías prácticas para crear videos** en YouTube, TikTok, Instagram Reels y YouTube Shorts. En lugar de generar videos directamente, la aplicación proporciona:

✅ **Guiones narrativos detallados**
✅ **Guías de coreografía paso a paso**
✅ **Recomendaciones musicales específicas**
✅ **Estructura de transiciones y efectos**
✅ **Timeline segundo a segundo**
✅ **Equipamiento y recursos necesarios**
✅ **Tips para viralizar**
✅ **Checklist de producción**

De esta manera, los usuarios tienen una **guía 100% funcional** lista para implementar, sin necesidad de generar videos automáticamente.

---

## 🚀 Endpoints Disponibles

### 1. Generar Script de Video Completo
**POST** `/api/video/script`

#### Descripción
Genera un guión completo y detallado para crear un video en la plataforma especificada.

#### Request Body
```json
{
  "tema": "Cómo hacer ejercicio en casa",
  "plataforma": "youtube",
  "audiencia": "personas principiantes sin experiencia en fitness",
  "estilo": "Tutorial",
  "idioma": "es",
  "duracion_minutos": 5,
  "informacion_adicional": "Enfoque en ejercicios sin equipamiento"
}
```

#### Parámetros

| Parámetro | Tipo | Requerido | Valores Aceptados | Descripción |
|-----------|------|-----------|-------------------|-------------|
| `tema` | string | ✅ | Cualquier tema | Tema principal del video |
| `plataforma` | string | ✅ | `youtube`, `youtube_shorts`, `tiktok`, `instagram_reels` | Plataforma destino |
| `audiencia` | string | ✅ | Descripción de audiencia | A quién va dirigido el video |
| `estilo` | string | ❌ | `Educativo`, `Entretenimiento`, `Tutorial`, `Lifestyle`, etc. | Estilo del contenido (default: "Educativo") |
| `idioma` | string | ❌ | `es`, `en`, `fr`, `it` | Idioma del guión (default: "es") |
| `duracion_minutos` | integer | ❌ | 0.15 - 60 | Duración deseada del video (default: 1) |
| `informacion_adicional` | string | ❌ | Cualquier texto | Contexto adicional |

#### Response
```json
{
  "status": "success",
  "plataforma": "youtube",
  "tema": "Cómo hacer ejercicio en casa",
  "audiencia": "personas principiantes sin experiencia en fitness",
  "estilo": "Tutorial",
  "idioma": "es",
  "duracion_minutos": 5,
  "guion": "1️⃣ CONCEPTO GENERAL\n[Contenido detallado del guión]..."
}
```

#### Secciones Incluidas en el Guión
1. **Concepto General** - Idea principal y gancho inicial
2. **Guión Narrativo** - Diálogos y narración palabra por palabra
3. **Estructura Visual y Coreografía** - Movimientos corporales paso a paso
4. **Recomendaciones Musicales** - Género, BPM, ejemplos de canciones
5. **Transiciones y Efectos** - Lista de transiciones específicas
6. **Equipamiento y Recursos** - Lo que necesitas para grabar
7. **Timeline Detallado** - Segundo a segundo qué hacer
8. **Tips para Viralizar** - Estrategias y hashtags
9. **Checklist de Producción** - Verificaciones pre/durante/post grabación

#### Ejemplos de Uso

**Ejemplo 1: Tutorial de TikTok**
```json
{
  "tema": "Receta de café con espuma",
  "plataforma": "tiktok",
  "audiencia": "amantes del café entre 18-35 años",
  "estilo": "Tutorial",
  "idioma": "es",
  "duracion_minutos": 0.5
}
```

**Ejemplo 2: Video motivacional YouTube**
```json
{
  "tema": "Cómo mantener la motivación en 2026",
  "plataforma": "youtube",
  "audiencia": "profesionales jóvenes",
  "estilo": "Motivacional",
  "idioma": "es",
  "duracion_minutos": 8
}
```

**Ejemplo 3: Instagram Reel de moda**
```json
{
  "tema": "Outfits tendencia para primavera",
  "plataforma": "instagram_reels",
  "audiencia": "mujeres jóvenes interesadas en moda",
  "estilo": "Lifestyle",
  "idioma": "es",
  "duracion_minutos": 0.75
}
```

---

### 2. Generar Guía de Coreografía
**POST** `/api/video/choreography`

#### Descripción
Genera una guía detallada de coreografía paso a paso para videos de baile.

#### Request Body
```json
{
  "tema": "Baile al ritmo de reggaeton",
  "audiencia": "principiantes que quieren aprender reggaeton",
  "nivel_dificultad": "Intermedio",
  "idioma": "es",
  "informacion_adicional": "Estilo urbano moderno"
}
```

#### Parámetros

| Parámetro | Tipo | Requerido | Valores Aceptados | Descripción |
|-----------|------|-----------|-------------------|-------------|
| `tema` | string | ✅ | Cualquier tema | Tema o nombre del baile |
| `audiencia` | string | ✅ | Descripción | A quién va dirigido |
| `nivel_dificultad` | string | ❌ | `Principiante`, `Intermedio`, `Avanzado` | Nivel de dificultad (default: "Intermedio") |
| `idioma` | string | ❌ | `es`, `en`, `fr`, `it` | Idioma (default: "es") |
| `informacion_adicional` | string | ❌ | Cualquier texto | Detalles adicionales |

#### Response
```json
{
  "status": "success",
  "tipo": "choreography",
  "tema": "Baile al ritmo de reggaeton",
  "nivel_dificultad": "Intermedio",
  "idioma": "es",
  "contenido": "1️⃣ VISIÓN GENERAL\n[Contenido de la coreografía]..."
}
```

#### Secciones Incluidas
1. **Visión General** - Concepto y música recomendada
2. **Pasos Básicos** - Movimientos fundamentales explicados
3. **Coreografía Paso a Paso** - Desglose temporal detallado
4. **Variaciones** - Versiones fácil/difícil
5. **Tips de Ejecución** - Errores a evitar, mejoras
6. **Formaciones** - Para 1, 2-3 o grupo de personas

---

### 3. Generar Guía de Música
**POST** `/api/video/music-guide`

#### Descripción
Genera recomendaciones de música específicas para el video.

#### Request Body
```json
{
  "tema": "Tutorial de meditación",
  "plataforma": "youtube",
  "genero": "Ambient",
  "idioma": "es"
}
```

#### Parámetros

| Parámetro | Tipo | Requerido | Valores Aceptados | Descripción |
|-----------|------|-----------|-------------------|-------------|
| `tema` | string | ✅ | Cualquier tema | Tema del video |
| `plataforma` | string | ✅ | `youtube`, `youtube_shorts`, `tiktok`, `instagram_reels` | Plataforma |
| `genero` | string | ❌ | Pop, Electrónico, Hip-Hop, Ambient, etc. | Género musical preferido (default: "Pop") |
| `idioma` | string | ❌ | `es`, `en`, `fr`, `it` | Idioma (default: "es") |

#### Response
```json
{
  "status": "success",
  "tipo": "music_guide",
  "tema": "Tutorial de meditación",
  "plataforma": "youtube",
  "genero": "Ambient",
  "idioma": "es",
  "contenido": "1️⃣ ANÁLISIS DEL TEMA\n[Recomendaciones de música]..."
}
```

#### Secciones Incluidas
1. **Análisis del Tema** - Emociones y BPM recomendado
2. **Top 5 Canciones** - Recomendaciones con links
3. **Alternativas sin Copyright** - Música libre
4. **Pistas de Audio Libres** - Soundtracks e instrumentales
5. **Timing y Sincronización** - Cómo sincronizar música y video

---

### 4. Obtener Plataformas Soportadas
**GET** `/api/video/platforms`

#### Descripción
Obtiene la lista de plataformas de video soportadas con sus características.

#### Response
```json
{
  "platforms": [
    {
      "id": "youtube",
      "nombre": "YouTube",
      "duracion_minutos": {"min": 2, "max": 60},
      "formato": "Horizontal (16:9)",
      "descripcion": "Videos largos y detallados"
    },
    {
      "id": "youtube_shorts",
      "nombre": "YouTube Shorts",
      "duracion_minutos": {"min": 0.15, "max": 1},
      "formato": "Vertical (9:16)",
      "descripcion": "Videos cortos rápidos y dinámicos"
    },
    {
      "id": "tiktok",
      "nombre": "TikTok",
      "duracion_minutos": {"min": 0.15, "max": 10},
      "formato": "Vertical (9:16)",
      "descripcion": "Contenido viral, muy dinámico"
    },
    {
      "id": "instagram_reels",
      "nombre": "Instagram Reels",
      "duracion_minutos": {"min": 0.15, "max": 3},
      "formato": "Vertical (9:16)",
      "descripcion": "Contenido visualmente atractivo"
    }
  ]
}
```

---

### 5. Obtener Estilos Disponibles
**GET** `/api/video/styles`

#### Descripción
Obtiene la lista de estilos de video disponibles.

#### Response
```json
{
  "estilos": [
    "Educativo",
    "Entretenimiento",
    "Tutorial",
    "Lifestyle",
    "Motivacional",
    "Comedy",
    "Drama",
    "Reviews",
    "Vlogs",
    "Trailers"
  ]
}
```

---

## 🧪 Ejemplos de Uso Completo

### Flujo 1: Crear un Tutorial Completo para YouTube

```bash
# 1. Obtener plataformas disponibles
curl -X GET "http://localhost:5001/api/video/platforms"

# 2. Generar script principal
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Cómo crear un portfolio web como desarrollador",
    "plataforma": "youtube",
    "audiencia": "desarrolladores principiantes",
    "estilo": "Tutorial",
    "idioma": "es",
    "duracion_minutos": 10,
    "informacion_adicional": "Enfoque en HTML, CSS y JavaScript básico"
  }'

# 3. Generar guía musical
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Cómo crear un portfolio web como desarrollador",
    "plataforma": "youtube",
    "genero": "Electrónico",
    "idioma": "es"
  }'
```

### Flujo 2: Crear un TikTok de Baile

```bash
# 1. Generar script
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile viral tendencia 2026",
    "plataforma": "tiktok",
    "audiencia": "jóvenes entre 13-25 años",
    "estilo": "Entretenimiento",
    "idioma": "es",
    "duracion_minutos": 0.5
  }'

# 2. Generar coreografía detallada
curl -X POST "http://localhost:5001/api/video/choreography" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile viral tendencia 2026",
    "audiencia": "jóvenes entre 13-25 años",
    "nivel_dificultad": "Principiante",
    "idioma": "es"
  }'

# 3. Generar recomendaciones de música
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile viral tendencia 2026",
    "plataforma": "tiktok",
    "genero": "Pop",
    "idioma": "es"
  }'
```

### Flujo 3: Instagram Reel de Receta

```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Receta rápida de brownies de chocolate",
    "plataforma": "instagram_reels",
    "audiencia": "amantes de la repostería, rango 20-40 años",
    "estilo": "Tutorial",
    "idioma": "es",
    "duracion_minutos": 1,
    "informacion_adicional": "Receta sin harina, apta para celíacos"
  }'
```

---

## 📱 Integración Frontend

### Componente React Ejemplo

```jsx
import React, { useState } from 'react';

export function VideoScriptGenerator() {
  const [tema, setTema] = useState('');
  const [plataforma, setPlataforma] = useState('youtube');
  const [audiencia, setAudiencia] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleGenerateScript = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/video/script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tema,
          plataforma,
          audiencia,
          estilo: 'Educativo',
          idioma: 'es',
          duracion_minutos: 5
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Tema del video"
        value={tema}
        onChange={(e) => setTema(e.target.value)}
      />
      <select value={plataforma} onChange={(e) => setPlataforma(e.target.value)}>
        <option value="youtube">YouTube</option>
        <option value="youtube_shorts">YouTube Shorts</option>
        <option value="tiktok">TikTok</option>
        <option value="instagram_reels">Instagram Reels</option>
      </select>
      <input
        type="text"
        placeholder="Describe tu audiencia"
        value={audiencia}
        onChange={(e) => setAudiencia(e.target.value)}
      />
      <button onClick={handleGenerateScript} disabled={loading}>
        {loading ? 'Generando...' : 'Generar Guión'}
      </button>

      {result && (
        <div>
          <h3>Guión Generado:</h3>
          <pre>{result.guion}</pre>
        </div>
      )}
    </div>
  );
}
```

---

## ✨ Características Clave

### 1. **Guiones Completos**
- Narrativa profesional
- Estructura clara y fácil de seguir
- Adaptado a la plataforma específica

### 2. **Coreografía Detallada**
- Pasos explicados paso a paso
- Variaciones de dificultad
- Formaciones de grupo

### 3. **Guías Musicales**
- Recomendaciones de canciones reales
- Música libre de copyright
- Tips de sincronización

### 4. **Timeline Preciso**
- Segundo a segundo qué hacer
- Timing exacto
- Indicaciones de transiciones

### 5. **Equipamiento y Recursos**
- Qué necesitas para grabar
- Recomendaciones de software
- Configuración técnica

### 6. **Viralizacion**
- Tips basados en la plataforma
- Hashtags específicos
- Mejores horas para publicar

---

## 🔧 Configuración Técnica

### Plataformas Soportadas

| Plataforma | Min Duración | Max Duración | Formato | Enfoque |
|-----------|-------------|-------------|---------|---------|
| YouTube | 2 min | 60 min | 16:9 | Contenido detallado |
| YouTube Shorts | 15 seg | 1 min | 9:16 | Rápido y dinámico |
| TikTok | 15 seg | 10 min | 9:16 | Viral y trending |
| Instagram Reels | 15 seg | 3 min | 9:16 | Visualmente atractivo |

### Idiomas Soportados
- 🇪🇸 Castellano (es)
- 🇬🇧 English (en)
- 🇫🇷 Français (fr)
- 🇮🇹 Italiano (it)

---

## 🎯 Casos de Uso

1. **Educadores**: Crear cursos en video sin necesidad de grabar
2. **Influencers**: Generar ideas de contenido viral
3. **Marcas**: Crear campañas de video estructuradas
4. **Creadores**: Acelerar el proceso de ideación
5. **Agencias**: Plantillas reutilizables para clientes

---

## ⚠️ Limitaciones y Consideraciones

- El sistema genera **guías, no videos**
- Se requiere ejecutar/implementar manualmente el guión
- La calidad depende del LLM utilizado (Groq/Gemini)
- Los tiempos son estimaciones, pueden variar en práctica

---

## 📚 Referencias

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Groq API](https://console.groq.com/)
- [Google Gemini API](https://ai.google.dev/)
