# 📺 Casos de Uso - Generador de Guiones de Video

Este documento contiene ejemplos prácticos de cómo usar el sistema de generación de guiones de video para diferentes tipos de contenido.

---

## 📚 Caso 1: Tutorial Completo para YouTube

### Objetivo
Crear un tutorial educativo sobre "Cómo crear una API REST con Python y FastAPI" de 10 minutos de duración.

### Pasos

#### 1. Obtener Información de Plataformas
```bash
curl -X GET "http://localhost:5001/api/video/platforms"
```

#### 2. Generar Script Principal
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Cómo crear una API REST con Python y FastAPI",
    "plataforma": "youtube",
    "audiencia": "desarrolladores principiantes que quieren aprender backend",
    "estilo": "Tutorial",
    "idioma": "es",
    "duracion_minutos": 10,
    "informacion_adicional": "Enfoque en conceptos básicos, endpoints CRUD, base de datos SQLite"
  }'
```

#### 3. Generar Guía Musical
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Cómo crear una API REST con Python y FastAPI",
    "plataforma": "youtube",
    "genero": "Electrónico",
    "idioma": "es"
  }'
```

#### 4. Implementar
El usuario recibe:
- ✅ Guión palabra por palabra
- ✅ Timeline segundo a segundo
- ✅ Recomendaciones musicales con links
- ✅ Equipamiento necesario
- ✅ Transiciones recomendadas

### Resultado Esperado
Un tutorial profesional completamente planeado que el creador solo necesita grabar y editar.

---

## 💃 Caso 2: Video de Baile para TikTok

### Objetivo
Crear un video de baile viral para TikTok de 30 segundos siguiendo una tendencia de reggaeton.

### Pasos

#### 1. Generar Script Base
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile reggaeton viral trending 2026",
    "plataforma": "tiktok",
    "audiencia": "jóvenes entre 13-25 años amantes del reggaeton",
    "estilo": "Entretenimiento",
    "idioma": "es",
    "duracion_minutos": 0.5,
    "informacion_adicional": "Movimientos sensuales, caderas, brazos fluidos, trending sounds"
  }'
```

#### 2. Generar Coreografía Detallada
```bash
curl -X POST "http://localhost:5001/api/video/choreography" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile reggaeton viral trending 2026",
    "audiencia": "jóvenes entre 13-25 años",
    "nivel_dificultad": "Principiante",
    "idioma": "es",
    "informacion_adicional": "Pasos simples que cualquiera pueda replicar, movimientos de cadera enfatizados"
  }'
```

#### 3. Generar Recomendaciones de Música
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Baile reggaeton viral",
    "plataforma": "tiktok",
    "genero": "Reggaeton",
    "idioma": "es"
  }'
```

#### 4. Implementar
El usuario recibe:
- ✅ Pasos de baile explicados paso a paso
- ✅ Formaciones (para 1, 2, o grupo)
- ✅ Canciones trending que funcionan bien en TikTok
- ✅ Música libre de copyright alternativa
- ✅ Tips para que el video sea viral

### Resultado Esperado
Un video de baile viral profesional en 30 segundos con coreografía fácil de replicar.

---

## 🍰 Caso 3: Reel de Receta para Instagram

### Objetivo
Crear un Instagram Reel de receta rápida de "Brownies sin harina" de 45 segundos.

### Pasos

#### 1. Generar Script
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Receta rápida de brownies sin harina y gluten free",
    "plataforma": "instagram_reels",
    "audiencia": "mujeres 25-45 años, amantes de la repostería, celíacas",
    "estilo": "Tutorial",
    "idioma": "es",
    "duracion_minutos": 0.75,
    "informacion_adicional": "ASMR de mezcla, 5 ingredientes, listo en 20 minutos, apta para personas con intolerancia al gluten"
  }'
```

#### 2. Generar Guía de Música
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Receta de brownies sin harina",
    "plataforma": "instagram_reels",
    "genero": "Ambient",
    "idioma": "es"
  }'
```

#### 3. Implementar
El usuario recibe:
- ✅ Narración o pasos en pantalla
- ✅ Ángulos de cámara recomendados
- ✅ Transiciones suaves (típicas de Reels)
- ✅ Música ambiental relajante
- ✅ Hashtags específicos (#RecetaGlutenFree #Brownies #Reels)
- ✅ Mejores horas para publicar

### Resultado Esperado
Un Reel profesional de receta que genera engagement y es fácil de seguir.

---

## 📱 Caso 4: YouTube Short Motivacional

### Objetivo
Crear un YouTube Short de 1 minuto con un mensaje motivacional sobre productividad.

### Pasos

#### 1. Generar Script
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "5 hábitos de productividad que cambiaron mi vida en 2026",
    "plataforma": "youtube_shorts",
    "audiencia": "profesionales jóvenes, emprendedores, estudiantes",
    "estilo": "Motivacional",
    "idioma": "es",
    "duracion_minutos": 1,
    "informacion_adicional": "Gancho fuerte en primeros 2 segundos, datos inspiradores, call to action claro"
  }'
```

#### 2. Generar Música
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "5 hábitos de productividad",
    "plataforma": "youtube_shorts",
    "genero": "Motivacional",
    "idioma": "es"
  }'
```

#### 3. Implementar
El usuario recibe:
- ✅ Gancho inicial impactante (primeros 3 segundos críticos)
- ✅ 5 hábitos específicos con explicaciones breves
- ✅ Transiciones dinámicas y rápidas
- ✅ Música motivacional
- ✅ CTA (Call To Action) claro
- ✅ Emojis y textos en pantalla sugeridos

### Resultado Esperado
Un Short impactante y viral que genera engagement inmediato.

---

## 🏋️ Caso 5: Workout Tutorial para YouTube

### Objetivo
Crear un tutorial de entrenamiento casero de 5 minutos para principiantes.

### Pasos

#### 1. Generar Script
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Rutina de ejercicio casero sin equipamiento para principiantes",
    "plataforma": "youtube",
    "audiencia": "principiantes sin experiencia, sin acceso a gimnasio, buscan resultados rápidos",
    "estilo": "Tutorial",
    "idioma": "es",
    "duracion_minutos": 5,
    "informacion_adicional": "15 minutos de duración, baja intensidad, apta para todas las edades, énfasis en forma correcta"
  }'
```

#### 2. Generar Coreografía (movimientos)
```bash
curl -X POST "http://localhost:5001/api/video/choreography" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Rutina de ejercicio casero para principiantes",
    "audiencia": "principiantes de todas las edades",
    "nivel_dificultad": "Principiante",
    "idioma": "es",
    "informacion_adicional": "Enfoque en forma correcta, seguridad, progresión lenta, sin lesiones"
  }'
```

#### 3. Generar Música
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Rutina de ejercicio casero",
    "plataforma": "youtube",
    "genero": "Pop Energético",
    "idioma": "es"
  }'
```

#### 4. Implementar
El usuario recibe:
- ✅ Estructura: calentamiento, ejercicios, enfriamiento
- ✅ Cada ejercicio explicado detalladamente
- ✅ Repeticiones y duración recomendadas
- ✅ Variaciones para diferentes niveles
- ✅ Música energética
- ✅ Timing para cada sección

### Resultado Esperado
Un tutorial de fitness completo y profesional.

---

## 🎮 Caso 6: Gamers - Análisis de Juego

### Objetivo
Crear un video de análisis de juego para YouTube de 8 minutos.

### Pasos

#### 1. Generar Script
```bash
curl -X POST "http://localhost:5001/api/video/script" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Análisis completo: El mejor juego indie de 2026",
    "plataforma": "youtube",
    "audiencia": "gamers de 18-35 años, interesados en juegos indie",
    "estilo": "Reviews",
    "idioma": "es",
    "duracion_minutos": 8,
    "informacion_adicional": "Cobertura: gráficos, historia, jugabilidad, precio, pros y contras, recomendación final"
  }'
```

#### 2. Generar Música
```bash
curl -X POST "http://localhost:5001/api/video/music-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "tema": "Análisis de videojuego",
    "plataforma": "youtube",
    "genero": "Electrónico",
    "idioma": "es"
  }'
```

#### 3. Implementar
El usuario recibe:
- ✅ Estructura: introducción, story, jugabilidad, gráficos, precio, veredicto
- ✅ Puntos clave a cubrir
- ✅ Transiciones entre secciones
- ✅ Música de fondo gaming
- ✅ Sugerencias de pantalla/gameplay a mostrar
- ✅ CTA para subscribirse

### Resultado Esperado
Un análisis de videojuego profesional y estructurado.

---

## 💼 Flujo Típico de Desarrollo

```
1. IDEACIÓN
   ↓
2. SOLICITAR SCRIPT A API
   ↓
3. LEER Y ADAPTAR GUIÓN
   ↓
4. SOLICITAR MÚSICA SI ES NECESARIO
   ↓
5. SOLICITAR COREOGRAFÍA SI ES NECESARIO
   ↓
6. REUNIR EQUIPAMIENTO Y RECURSOS
   ↓
7. GRABAR CONTENIDO
   ↓
8. EDITAR (usando transiciones y timing del script)
   ↓
9. AGREGAR MÚSICA Y EFECTOS DE SONIDO
   ↓
10. PUBLICAR CON HASHTAGS Y CTA SUGERIDOS
```

---

## 🎬 Template JSON General

```json
{
  "caso_uso": "Descripción del video",
  "paso_1_script": {
    "endpoint": "POST /api/video/script",
    "tema": "Tema específico",
    "plataforma": "youtube|tiktok|instagram_reels|youtube_shorts",
    "audiencia": "Descripción de la audiencia",
    "estilo": "Tutorial|Entretenimiento|Educativo|etc.",
    "idioma": "es|en|fr|it",
    "duracion_minutos": "número",
    "informacion_adicional": "contexto extra"
  },
  "paso_2_musica": {
    "endpoint": "POST /api/video/music-guide",
    "tema": "Igual al del script",
    "plataforma": "Igual al del script",
    "genero": "Pop|Electrónico|Hip-Hop|Ambient|etc.",
    "idioma": "es|en|fr|it"
  },
  "paso_3_coreografia": {
    "endpoint": "POST /api/video/choreography",
    "tema": "Tema de baile",
    "audiencia": "Descripción",
    "nivel_dificultad": "Principiante|Intermedio|Avanzado",
    "idioma": "es|en|fr|it",
    "informacion_adicional": "detalles"
  }
}
```

---

## 💡 Tips de Optimización

### Para Máximo Engagement
1. **TikTok & Shorts**: Gancho fuerte primeros 3 segundos
2. **YouTube**: Estructura clara con secciones bien definidas
3. **Instagram Reels**: Transiciones suaves y visuales impactantes
4. **Todos**: CTA claro al final (Like, Subscribe, Compartir)

### Para Viralizar
1. Usar trending sounds (recomendados por `music-guide`)
2. Hashtags específicos (incluidos en el script)
3. Publicar en mejores horas (recomendadas)
4. Contenido que resuelva un problema o entretiene

### Para Calidad Profesional
1. Seguir el timeline exacto del script
2. Usar equipamiento recomendado
3. Sincronizar correctamente música y contenido
4. Realizar checklist de producción

---

## 📊 Estadísticas de Duración Recomendada

| Plataforma | Duración Ideal | Rango |
|-----------|---------------|-------|
| TikTok | 15-30 seg | 15 seg - 10 min |
| Instagram Reels | 30-60 seg | 15 seg - 3 min |
| YouTube Shorts | 30-45 seg | 15 seg - 1 min |
| YouTube | 5-10 min | 2 - 60 min |

---

**Nota**: Todos los ejemplos están listos para implementar. Solo necesitas seguir los pasos y adaptar el contenido generado a tu estilo personal.
