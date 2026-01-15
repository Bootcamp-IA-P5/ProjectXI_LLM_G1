# Prompt base (aplica a todo)
SYSTEM_PROMPT = "Eres experto en generar contenido para diversos medios y audiencias, utilizando IA generativa y automatizando publicaciones, listas para publicar:"

# Prompts especificos por plataforma
def create_twitter_prompt(tema, audiencia, informacion_adicional=""):
    return f"""
    Eres un experto en Social Media especializado en Twitter/X.
    Genera un hilo de máximo 3 tweets sobre el tema: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    Requisitos:
    - El primer tweet debe ser un 'hook' (gancho) que invite a seguir leyendo.
    - Máximo 280 caracteres por tweet.
    - Tono: Directo, conciso y con personalidad.
    - Incluye emojis pertinentes y 2-3 hashtags estratégicos al final.
    - Si es apropiado, termina con una pregunta para fomentar el engagement.
    """

def create_instagram_prompt(tema, audiencia, informacion_adicional=""):
    return f"""
    Eres un copywriter creativo experto en Instagram.
    Genera el caption para una publicación sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    Requisitos:
    - Estructura: Gancho inicial, cuerpo con valor/entretenimiento y Call to Action (CTA).
    - Tono: Visual, inspirador y cercano.
    - Usa saltos de línea para facilitar la lectura.
    - Incluye un bloque de 5-10 hashtags relevantes al final.
    - Sugiere brevemente qué tipo de imagen o diseño debería acompañar a este texto.
    """

def create_linkedin_prompt(tema, audiencia, informacion_adicional=""):
    return f"""
    Eres un líder de opinión y experto en branding profesional en LinkedIn.
    Escribe un post reflexivo sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    Requisitos:
    - Tono: Profesional, analítico y autoritario pero accesible.
    - Formato: Estilo "copywriting de LinkedIn" (líneas cortas, mucho espacio en blanco).
    - Contenido: Aporta un ángulo de negocio, una lección aprendida o una tendencia del sector.
    - Finaliza con una pregunta que invite al debate profesional.
    - Máximo 3 hashtags profesionales.
    """

def create_blog_prompt(tema, audiencia, informacion_adicional=""):
    return f"""
    Eres un redactor de contenidos SEO senior.
    Escribe un artículo de blog estructurado sobre: '{tema}'.
    Audiencia objetivo: {audiencia}.
    {f'Contexto de la empresa/marca: {informacion_adicional}' if informacion_adicional else ''}
    
    Requisitos:
    - Título optimizado para SEO (H1).
    - Introducción sugerente que plantee un problema o necesidad.
    - Cuerpo dividido con subtítulos claros (H2, H3).
    - Conclusión con un resumen de puntos clave.
    - Tono: Educativo, detallado y bien estructurado.
    - Longitud aproximada: 500-800 palabras.
    """
    
# Funcion que combine todo
def get_full_prompt(tema, plataforma, audiencia, informacion_adicional=""):
    plataformas = {
        "twitter": create_twitter_prompt,
        "blog": create_blog_prompt,
        "instagram": create_instagram_prompt,
        "linkedin": create_linkedin_prompt
    }
    func = plataformas[plataforma]
    
    base = SYSTEM_PROMPT
    specific = func(tema, audiencia, informacion_adicional)
    return base + "\n" + specific

def get_full_prompt(tema, audiencia, plataforma, informacion_adicional, idioma):
    """
    Construye el 'Super Prompt' combinando todas las capas de requisitos.
    """
    # Capa 1: Restricción de Idioma (Prioridad máxima)
    instruccion_idioma = f"Toda tu respuesta debe estar escrita en {idioma}."

    # Capa 2: Personalización de Marca 
    # Si hay info de la empresa, la incluimos para que el contenido sea único
    contexto_marca = f"Ten en cuenta esta información de la marca: {informacion_adicional}" if informacion_adicional else ""

    # Capa 3: Instrucción de Tarea 
    # Aquí es donde el modelo aplica su conocimiento de la plataforma
    tarea = f"Escribe un contenido para {plataforma} sobre el tema '{tema}' dirigido a una audiencia de {audiencia}."

    # Unimos todo en un solo bloque de texto coherente
    return f"{instruccion_idioma}\n{contexto_marca}\n\n{tarea}"