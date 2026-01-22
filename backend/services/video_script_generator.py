"""Video Script Generation Service for YouTube and TikTok"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class VideoScriptGenerator:
    """Generador de guiones y guías de video para YouTube y TikTok
    
    Genera estructuras completas para crear videos incluyendo:
    - Guión narrativo
    - Estructura de coreografía
    - Recomendaciones de música
    - Transiciones y efectos
    - Timing y duración
    """

    def __init__(self, llm_client=None):
        """Recibir cliente LLM (inyección de dependencia, opcional)"""
        self.llm_client = llm_client
        self.plataformas_soportadas = ["youtube", "tiktok", "youtube_shorts", "instagram_reels"]
        self.idiomas_soportados = {
            "es": "Castellano",
            "en": "English",
            "fr": "Français",
            "it": "Italiano"
        }

    def _build_video_prompt(
        self,
        tema: str,
        plataforma: str,
        audiencia: str,
        estilo: str,
        idioma: str,
        duracion_minutos: int = 1,
        informacion_adicional: str = ""
    ) -> str:
        """Construir prompt especializado para generar guiones de video"""
        
        # Configuración según plataforma
        config_plataforma = {
            "tiktok": {
                "duracion_default": 0.5,
                "min_duracion": 0.15,
                "max_duracion": 10,
                "enfasis": "Contenido rápido, dinámico, con cortes frecuentes y transiciones impactantes",
                "formato": "Vertical (9:16)"
            },
            "youtube_shorts": {
                "duracion_default": 0.6,
                "min_duracion": 0.15,
                "max_duracion": 1,
                "enfasis": "Contenido vertical corto y cautivador con gancho inicial fuerte",
                "formato": "Vertical (9:16)"
            },
            "youtube": {
                "duracion_default": 5,
                "min_duracion": 2,
                "max_duracion": 60,
                "enfasis": "Contenido detallado, bien estructurado con introducción, desarrollo y conclusión",
                "formato": "Horizontal (16:9)"
            },
            "instagram_reels": {
                "duracion_default": 0.75,
                "min_duracion": 0.15,
                "max_duracion": 3,
                "enfasis": "Contenido visualmente atractivo con transiciones suaves y trend-oriented",
                "formato": "Vertical (9:16)"
            }
        }

        plat = config_plataforma.get(plataforma, config_plataforma["youtube"])
        nombre_idioma = self.idiomas_soportados.get(idioma, "Castellano")

        prompt = f"""Eres un experto en creación de contenido de video para redes sociales.
Genera una GUÍA COMPLETA Y DETALLADA para crear un video profesional.

PARÁMETROS:
- Idioma: {nombre_idioma}
- Plataforma: {plataforma}
- Tema: {tema}
- Audiencia: {audiencia}
- Estilo: {estilo}
- Duración: {duracion_minutos} minutos
- Formato: {plat['formato']}
- Enfoque: {plat['enfasis']}

ESTRUCTURA REQUERIDA (Genera cada sección de forma clara y detallada):

1️⃣ CONCEPTO GENERAL
   - Idea principal del video
   - Objetivo del contenido
   - Gancho inicial (primeros 3 segundos)

2️⃣ GUIÓN NARRATIVO
   - Narración palabra por palabra (si aplica)
   - Diálogos (si aplica)
   - Timing estimado para cada sección
   - Indicaciones de tono y énfasis

3️⃣ ESTRUCTURA VISUAL Y COREOGRAFÍA
   - Posiciones iniciales
   - Movimientos corporales recomendados (paso a paso)
   - Expresiones faciales sugeridas
   - Accesorios o props necesarios
   - Formaciones de grupo (si aplica)

4️⃣ RECOMENDACIONES MUSICALES
   - Género musical recomendado
   - Tempo (BPM) sugerido
   - 3 ejemplos de canciones similares (artista - canción)
   - Dónde encontrar música libre (Spotify, YouTube Audio Library, etc.)
   - Timing de la música según el video

5️⃣ TRANSICIONES Y EFECTOS
   - Lista de transiciones recomendadas (fade, corte, zoom, barrido, etc.)
   - Dónde aplicar cada transición
   - Efectos especiales sugeridos
   - Timing de cada transición (en segundos)
   - Software/herramientas recomendadas

6️⃣ EQUIPAMIENTO Y RECURSOS
   - Cámara/dispositivo recomendado
   - Iluminación necesaria
   - Ubicación/escenario ideal
   - Vestuario sugerido
   - Maquillaje (si aplica)

7️⃣ TIMELINE DETALLADO
   - Segundo a segundo o segmento por segmento
   - Acción visual
   - Audio/música/narración
   - Transición siguiente

8️⃣ TIPS PARA VIRALIZAR
   - Elementos que pueden resonar con la audiencia
   - Hashtags sugeridos ({plataforma})
   - Mejor hora para publicar
   - CTAs (llamados a la acción) recomendados

9️⃣ CHECKLIST DE PRODUCCIÓN
   - Lista de verificación antes de grabar
   - Lista de verificación antes de editar
   - Lista de verificación antes de publicar

{f"INFORMACIÓN ADICIONAL: {informacion_adicional}" if informacion_adicional else ""}

Genera la respuesta de forma clara, estructurada y lista para ser implementada. 
Usa emojis y formatos para mejorar la legibilidad.
Sé específico y práctico en cada recomendación."""

        return prompt

    def generate_video_script(
        self,
        tema: str,
        plataforma: str,
        audiencia: str,
        estilo: str = "Educativo",
        idioma: str = "es",
        duracion_minutos: int = 1,
        informacion_adicional: str = ""
    ) -> Dict[str, Any]:
        """Generar guión completo para video
        
        Args:
            tema: Tema principal del video
            plataforma: youtube, tiktok, youtube_shorts, instagram_reels
            audiencia: Descripción de la audiencia objetivo
            estilo: Educativo, Entretenimiento, Tutorial, etc.
            idioma: Código de idioma (es, en, fr, it)
            duracion_minutos: Duración deseada del video
            informacion_adicional: Información contextual adicional
            
        Returns:
            Diccionario con el guión generado y metadatos
        """
        
        # Validaciones
        if plataforma not in self.plataformas_soportadas:
            raise ValueError(
                f"Plataforma '{plataforma}' no soportada. Usa: {self.plataformas_soportadas}"
            )
        
        if idioma not in self.idiomas_soportados:
            raise ValueError(
                f"Idioma '{idioma}' no soportado. Usa: {list(self.idiomas_soportados.keys())}"
            )

        try:
            # Construir prompt especializado
            prompt_final = self._build_video_prompt(
                tema=tema,
                plataforma=plataforma,
                audiencia=audiencia,
                estilo=estilo,
                idioma=idioma,
                duracion_minutos=duracion_minutos,
                informacion_adicional=informacion_adicional
            )

            logger.info(f"🎬 Generando guión de video: {plataforma} - {tema}")

            # Generar con LLM
            guion = self.llm_client.generate(prompt_final)

            logger.info(f"✅ Guión generado exitosamente ({len(guion)} caracteres)")

            return {
                "status": "success",
                "plataforma": plataforma,
                "tema": tema,
                "audiencia": audiencia,
                "estilo": estilo,
                "idioma": idioma,
                "duracion_minutos": duracion_minutos,
                "guion": guion
            }

        except Exception as e:
            logger.error(f"❌ Error generando guión de video: {str(e)}")
            raise ConnectionError(f"Error al generar guión de video: {str(e)}")

    def generate_choreography_guide(
        self,
        tema: str,
        audiencia: str,
        nivel_dificultad: str = "Intermedio",
        idioma: str = "es",
        informacion_adicional: str = ""
    ) -> Dict[str, Any]:
        """Generar guía específica de coreografía para video de baile"""

        nombre_idioma = self.idiomas_soportados.get(idioma, "Castellano")

        prompt = f"""Eres un coreógrafo profesional experto en crear danzas para redes sociales.
Genera una GUÍA DE COREOGRAFÍA DETALLADA Y PASO A PASO.

TEMA: {tema}
AUDIENCIA: {audiencia}
NIVEL: {nivel_dificultad} (Principiante, Intermedio, Avanzado)
IDIOMA: {nombre_idioma}

ESTRUCTURA:

1️⃣ VISIÓN GENERAL
   - Concepto de la coreografía
   - Música recomendada
   - Duración total

2️⃣ PASOS BÁSICOS (si aplica)
   - Nombre del paso
   - Descripción detallada
   - Ilustración verbal (cómo se ve)

3️⃣ COREOGRAFÍA PASO A PASO
   Para cada sección temporal (0-15seg, 15-30seg, etc.):
   - Posición inicial
   - Movimiento paso 1 (descripción clara)
   - Movimiento paso 2
   - Movimiento paso 3
   - Transición al siguiente segmento
   - Timing en segundos

4️⃣ VARIACIONES
   - Versión más fácil
   - Versión más difícil
   - Adaptaciones para diferente número de personas

5️⃣ TIPS DE EJECUCIÓN
   - Errores comunes a evitar
   - Forma correcta de cada movimiento
   - Consejos para mejorar la presentación
   - Energía y expresión recomendada

6️⃣ FORMACIONES (si aplica)
   - Para 1 persona
   - Para 2-3 personas
   - Para grupo

{f"CONTEXTO ADICIONAL: {informacion_adicional}" if informacion_adicional else ""}

Sé muy específico y práctico. Usa descripciones detalladas que cualquiera pueda seguir."""

        try:
            logger.info(f"🕺 Generando guía de coreografía: {tema}")
            coreografia = self.llm_client.generate(prompt)

            return {
                "status": "success",
                "tipo": "choreography",
                "tema": tema,
                "nivel_dificultad": nivel_dificultad,
                "idioma": idioma,
                "contenido": coreografia
            }
        except Exception as e:
            logger.error(f"❌ Error generando coreografía: {str(e)}")
            raise ConnectionError(f"Error al generar guía de coreografía: {str(e)}")

    def generate_music_guide(
        self,
        tema: str,
        plataforma: str,
        genero: str = "Pop",
        idioma: str = "es"
    ) -> Dict[str, Any]:
        """Generar recomendaciones de música para video"""

        nombre_idioma = self.idiomas_soportados.get(idioma, "Castellano")

        prompt = f"""Eres un experto en selección de música para contenido digital.
Proporciona recomendaciones de MÚSICA detalladas para {plataforma}.

TEMA DEL VIDEO: {tema}
GÉNERO PREFERIDO: {genero}
IDIOMA: {nombre_idioma}

PROPORCIONA:

1️⃣ ANÁLISIS DEL TEMA
   - Emociones a transmitir
   - Tempo recomendado (BPM)
   - Duración ideal de la canción

2️⃣ TOP 5 CANCIONES RECOMENDADAS
   Para cada canción:
   - Artista - Título
   - Duración
   - BPM
   - Dónde encontrarla
   - Por qué funciona para este video

3️⃣ ALTERNATIVAS SIN COPYRIGHT
   - Plataformas recomendadas
   - Canciones específicas libres
   - Links de descarga

4️⃣ PISTAS DE AUDIO LIBRES
   - Soundtracks instrumentales recomendadas
   - Ambientes de sonido
   - Efectos de sonido necesarios

5️⃣ TIMING Y SINCRONIZACIÓN
   - Cómo sincronizar la música con el video
   - Puntos de corte recomendados
   - Transiciones musicales

Sé específico con artistas y canciones reales."""

        try:
            logger.info(f"🎵 Generando guía de música: {tema}")
            musica = self.llm_client.generate(prompt)

            return {
                "status": "success",
                "tipo": "music_guide",
                "tema": tema,
                "plataforma": plataforma,
                "genero": genero,
                "idioma": idioma,
                "contenido": musica
            }
        except Exception as e:
            logger.error(f"❌ Error generando guía de música: {str(e)}")
            raise ConnectionError(f"Error al generar guía de música: {str(e)}")
