# Prompt base (aplica a todo)
SYSTEM_PROMPT = "Eres experto en generar contenido para diversos medios y audiencias, utilizando IA generativa y automatizando publicaciones, listas para publicar:"

# Mapeo de idiomas
IDIOMA_MAP = {
    "es": "Español",
    "en": "English",
    "fr": "Français",
    "it": "Italiano"
}

def get_idioma_instruction(idioma="es"):
    """Retorna instrucción de idioma para el prompt"""
    idioma_nombre = IDIOMA_MAP.get(idioma, "Español")
    return f"Responde ÚNICAMENTE en {idioma_nombre}. No mezcles idiomas."


# Prompts especificos por plataforma
def create_twitter_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un experto en Social Media especializado en Twitter/X.
    Genera un hilo de máximo 3 tweets sobre el tema: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - El primer tweet debe ser un 'hook' (gancho) que invite a seguir leyendo.
    - Máximo 280 caracteres por tweet.
    - Tono: Directo, conciso y con personalidad.
    - Incluye emojis pertinentes y 2-3 hashtags estratégicos al final.
    - Información clara y valiosa para el público {audiencia}.
    - Si es apropiado, termina con una pregunta para fomentar el engagement.
    
    FORMATO: Presenta cada tweet numerado (Tweet 1:, Tweet 2:, Tweet 3:)
    """

def create_instagram_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un copywriter creativo experto en Instagram.
    Genera el caption para una publicación sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - Estructura: Gancho inicial IMPACTANTE, cuerpo con valor/entretenimiento y Call to Action (CTA) claro.
    - Tono: Visual, inspirador y cercano a {audiencia}.
    - Usa saltos de línea para facilitar la lectura en mobile.
    - Incluye un bloque de 5-10 hashtags relevantes al final.
    - Sugiere brevemente qué tipo de imagen o diseño debería acompañar a este texto.
    - Máximo 2200 caracteres.
    - Información valiosa y específica sobre {tema}.
    
    FORMATO: Caption + línea en blanco + Hashtags
    """

def create_linkedin_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un líder de opinión y experto en branding profesional en LinkedIn.
    Escribe un post reflexivo sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - Tono: Profesional, analítico y autoritario pero accesible a {audiencia}.
    - Estructura: Introducción gancho, desarrollo con insights, conclusión con CTA.
    - Incluye 3-5 emojis estratégicamente colocados para mejorar el visual.
    - Hashtags: 5-8 hashtags relevantes al final.
    - Máximo 3000 caracteres.
    - Información valiosa y original sobre {tema}.
    - Si menciona estadísticas o datos, que sean creíbles y contextuales.
    
    FORMATO: Post completo con estructura clara
    """

def create_blog_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un redactor experto en Blog y Content Marketing.
    Escribe un artículo completo sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - Estructura: Título impactante, introducción, 3-4 secciones con subtítulos, conclusión.
    - Usa # para títulos y ## para subtítulos (Markdown).
    - Tono: Informativo, educativo y accesible a {audiencia}.
    - Mínimo 1500 palabras, máximo 3000.
    - Incluye ejemplos prácticos y casos de uso reales.
    - SEO-friendly: Incluye keywords naturales sobre {tema}.
    - Finaliza con una conclusión que invite a la acción o reflexión.
    
    FORMATO: Artículo completo con estructura Markdown
    """

def create_tiktok_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un experto en TikTok y contenido viral.
    Crea un guion de video corto (30-60 segundos) sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - Hook impactante en los primeros 3 segundos.
    - Transiciones rápidas y dinámicas que mantengan atención.
    - Lenguaje casual y relatable para {audiencia}.
    - Incluye acciones claras (qué mostrar en pantalla).
    - Sugerencias de efectos/sonidos populares.
    - Recomendación de tendencias o hashtags trending.
    - Máximo 150 palabras (texto hablado).
    - Finaliza con un CTA o pregunta para comentarios.
    - Información útil/entretenida sobre {tema}.
    
    FORMATO: Divide por segundos (0-3s: Hook, 3-15s: Contenido, etc.)
    """

def create_youtube_prompt(tema, audiencia, informacion_adicional="", idioma="es"):
    idioma_instruction = get_idioma_instruction(idioma)
    return f"""
    Eres un creador de contenido de YouTube y video marketer experto.
    Crea un guion para un video de 5-10 minutos sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    {idioma_instruction}
    
    Requisitos ESTRICTOS:
    - Thumbnail idea: Descripción visual que capture atención.
    - Título SEO optimizado y atractivo para {audiencia}.
    - Intro (0-30s): Hook emocional que convenza de ver todo.
    - Estructura: Problema → Solución → Demostración → CTA.
    - Secciones con timestamps (intro, desarrollo, conclusión).
    - Lenguaje: Natural, conversacional pero con autoridad sobre {tema}.
    - Incluye puntos clave a destacar con efectos/gráficos.
    - Sugerencias de B-roll o visualización de contenido.
    - Outro con suscripción/social media CTA.
    - Información detallada, educativa y valiosa sobre {tema}.
    
    FORMATO: Outline por minutos (0:00-0:30 Intro, 0:30-2:00 Problema, etc.)
    """

# Funcion que combine todo - VERSIÓN MEJORADA
def get_full_prompt(tema, plataforma, audiencia, informacion_adicional="", idioma="es"):
    """
    Construye el 'Super Prompt' combinando todas las capas de requisitos.
    
    Args:
        tema: Tema sobre el cual generar contenido
        plataforma: Plataforma destino (twitter, instagram, linkedin, blog)
        audiencia: Audiencia objetivo
        informacion_adicional: Contexto de marca o información extra
        idioma: Idioma del contenido (default: "es" para Español)
    """
    # Capa 1: Restricción de Idioma (Prioridad máxima)
    idioma_nombre = IDIOMA_MAP.get(idioma, "Español")
    instruccion_idioma = f"⚠️ IMPORTANTE: Toda tu respuesta debe estar escrita ÚNICAMENTE en {idioma_nombre}."

    # Capa 2: Personalización de Marca 
    contexto_marca = f"🏢 Contexto de marca/empresa: {informacion_adicional}" if informacion_adicional else ""

    # Capa 3: Seleccionar prompt específico según plataforma
    plataformas = {
        "twitter": create_twitter_prompt,
        "blog": create_blog_prompt,
        "instagram": create_instagram_prompt,
        "linkedin": create_linkedin_prompt,
        "tiktok": create_tiktok_prompt,
        "youtube": create_youtube_prompt
    }
    
    if plataforma.lower() not in plataformas:
        raise ValueError(f"Plataforma '{plataforma}' no soportada. Usa: {list(plataformas.keys())}")
    
    func_prompt = plataformas[plataforma.lower()]
    prompt_especifico = func_prompt(tema, audiencia, informacion_adicional, idioma)

    # Unimos todo en un solo bloque de texto coherente
    base = SYSTEM_PROMPT
    return f"{base}\n\n{instruccion_idioma}\n\n{contexto_marca}\n\n{prompt_especifico}" if contexto_marca else f"{base}\n\n{instruccion_idioma}\n\n{prompt_especifico}"