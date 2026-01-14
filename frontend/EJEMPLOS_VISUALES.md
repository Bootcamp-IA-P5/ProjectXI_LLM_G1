# 🖼️ Ejemplos Visuales - Componentes ContentFlow v2.0

## Header

### Código HTML
```html
<header class="app-header">
    <div class="header-content">
        <div class="logo-section">
            <h1 class="app-title">✨ ContentFlow</h1>
            <p class="app-subtitle">Generador de Contenido Inteligente con IA</p>
        </div>
    </div>
</header>
```

### Estilos
```css
.app-header {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary-blue));
    color: white;
    padding: var(--spacing-xl);
    box-shadow: var(--shadow-lg);
}

.app-title {
    font-size: var(--font-size-3xl);
    font-weight: 800;
    background: linear-gradient(135deg, #fff, #e0e7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.app-subtitle {
    font-size: var(--font-size-lg);
    color: rgba(255, 255, 255, 0.85);
}
```

### Características
- Gradiente azul oscuro a azul vibrante
- Título con gradiente blanco
- Sombra elegante
- Animación fadeInDown
- Responsive

---

## Formulario

### Código React
```jsx
<form onSubmit={handleSubmit} className="form-card">
    <div className="form-header">
        <h2 className="form-title">📝 Crea tu Contenido</h2>
    </div>
    
    <div className={`form-group ${errors.tema ? 'error' : ''}`}>
        <label className="form-label">Tema Principal</label>
        <input 
            type="text"
            placeholder="Ej: Machine Learning..."
            value={tema}
            onChange={(e) => setTema(e.target.value)}
        />
        {errors.tema && <span className="form-error">{errors.tema}</span>}
    </div>
    
    <button type="submit">✨ Generar Contenido</button>
</form>
```

### Estilos CSS
```css
.form-card {
    background: var(--card-bg);
    border-radius: var(--border-radius-xl);
    padding: var(--spacing-2xl);
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
}

.form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: var(--spacing-lg);
    gap: var(--spacing-sm);
}

.form-label {
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--text-dark);
    text-transform: uppercase;
}

input[type="text"]:focus {
    border-color: var(--primary-blue);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

button[type="submit"] {
    background: linear-gradient(135deg, var(--primary-blue), var(--accent-cyan));
    color: white;
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: var(--border-radius-md);
    cursor: pointer;
    transition: all var(--transition-normal);
}

button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
}
```

### Características
- Validación en tiempo real
- Mensajes de error con icono
- Botón gradient azul-cyan
- Efecto hover elevado
- Animación slideInLeft
- Campo con error: borde rojo

---

## Validación de Formulario

### Estado Normal
```
┌─────────────────────────────────┐
│ Tema Principal                  │
│ ┌─────────────────────────────┐ │
│ │ Escribe tu tema aquí...     │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

### Estado con Error
```
┌─────────────────────────────────┐
│ Tema Principal                  │
│ ┌─────────────────────────────┐ │ ← Borde rojo
│ │                             │ │
│ └─────────────────────────────┘ │
│ ⚠️ El tema es requerido          │ ← Mensaje error
└─────────────────────────────────┘
```

### Estado Focus
```
┌─────────────────────────────────┐
│ Tema Principal                  │
│ ┌─────────────────────────────┐ │ ← Borde azul
│ │ Cursor aquí                 │ │
│ └─────────────────────────────┘ │ ← Sombra azul
│                                 │
└─────────────────────────────────┘
```

---

## Salida de Contenido

### Código React
```jsx
<div className="output-card">
    <div className="output-header">
        <h2 className="output-title">
            <span className="output-icon">✨</span>
            Contenido Generado
        </h2>
    </div>

    {loading && (
        <div className="loading-container">
            <div className="loading-spinner-large"></div>
            <p className="loading-text">Generando tu contenido...</p>
        </div>
    )}

    {error && (
        <div className="error-container">
            <h3 className="error-title">⚠️ Error en la Generación</h3>
            <p className="error-message">{error}</p>
        </div>
    )}

    {contenido && (
        <>
            <div className="output-content">
                <p className="output-text">{contenido}</p>
            </div>
            <div className="output-actions">
                <button className="btn-copy" onClick={handleCopy}>
                    {copied ? '✓ Copiado' : '📋 Copiar'}
                </button>
                <button className="btn-secondary" onClick={handleDownload}>
                    ⬇️ Descargar
                </button>
            </div>
        </>
    )}

    {!loading && !error && !contenido && (
        <div className="empty-state">
            <div className="empty-icon">📄</div>
            <h3 className="empty-title">Sin contenido aún</h3>
            <p className="empty-description">
                Completa el formulario y haz clic en "Generar"
            </p>
        </div>
    )}
</div>
```

### Estados

#### Estado: Cargando
```
┌──────────────────────────────────┐
│ ✨ Contenido Generado            │
├──────────────────────────────────┤
│                                  │
│              ⟳                   │ ← Spinner girando
│                                  │
│     Generando tu contenido...    │
│                                  │
└──────────────────────────────────┘
```

#### Estado: Error
```
┌──────────────────────────────────┐
│ ✨ Contenido Generado            │
├──────────────────────────────────┤
│ ⚠️ Error en la Generación         │
│                                  │
│ La API no respondió             │
│                                  │
└──────────────────────────────────┘
```

#### Estado: Contenido
```
┌──────────────────────────────────┐
│ ✨ Contenido Generado            │
├──────────────────────────────────┤
│ Este es el contenido generado   │
│ por tu IA. Puedes copiarlo o   │
│ descargarlo fácilmente.         │
├──────────────────────────────────┤
│ [📋 Copiar]  [⬇️ Descargar]    │
└──────────────────────────────────┘
```

#### Estado: Vacío
```
┌──────────────────────────────────┐
│ ✨ Contenido Generado            │
├──────────────────────────────────┤
│                                  │
│             📄                   │
│      Sin contenido aún           │
│                                  │
│  Completa el formulario y       │
│  haz clic en "Generar"          │
│                                  │
└──────────────────────────────────┘
```

---

## Botones

### Botón Principal (Generar)
```css
/* Código */
background: linear-gradient(135deg, var(--primary-blue), var(--accent-cyan));
color: white;
border: none;
border-radius: var(--border-radius-md);
padding: var(--spacing-md) var(--spacing-lg);
font-weight: 600;
cursor: pointer;
box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
transition: all var(--transition-normal);

/* Estado Normal */
┌─────────────────────────────┐
│  ✨ Generar Contenido       │
└─────────────────────────────┘

/* Estado Hover */
┌─────────────────────────────┐
│  ✨ Generar Contenido       │  ↑ Elevado
└─────────────────────────────┘

/* Estado Active */
┌─────────────────────────────┐
│  ✨ Generar Contenido       │  ↓ Presionado
└─────────────────────────────┘

/* Estado Disabled */
┌─────────────────────────────┐
│  ✨ Generando...            │  Opaco
│  [⟳]                        │
└─────────────────────────────┘
```

### Botón Secundario (Copiar)
```css
background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
color: white;
border: none;
border-radius: var(--border-radius-md);
```

### Botón Terciario (Reset)
```css
background: var(--light-bg);
color: var(--text-dark);
border: 2px solid var(--border-color);
border-radius: var(--border-radius-md);
```

---

## Paleta de Colores Visualizada

### Colores Primarios
```
┌──────────────────────────────┐
│  ■ Azul Oscuro (#0f172a)     │ Header, fondos
├──────────────────────────────┤
│  ■ Azul Vibrante (#2563eb)   │ Botones, acentos
├──────────────────────────────┤
│  ■ Morado (#7c3aed)          │ Títulos, gradientes
├──────────────────────────────┤
│  ■ Cyan (#06b6d4)            │ Acentos, botones
├──────────────────────────────┤
│  ■ Verde (#10b981)           │ Éxito, positivo
└──────────────────────────────┘
```

### Escala de Grises
```
■ #0f172a Muy oscuro
■ #1e293b Oscuro
■ #475569 Gris oscuro
■ #94a3b8 Gris medio
■ #cbd5e1 Gris claro
■ #f1f5f9 Muy claro
■ #ffffff Blanco puro
```

---

## Animaciones Visuales

### fadeInDown (Header)
```
Frame 0%:    Opaco 0%, Y-20px
             ↓
Frame 50%:   Opaco 50%, Y-10px
             ↓
Frame 100%:  Opaco 100%, Y 0px   ✅
```

### slideInLeft (Formulario)
```
Frame 0%:    Opaco 0%, X-20px
             ↓
Frame 50%:   Opaco 50%, X-10px
             ↓
Frame 100%:  Opaco 100%, X 0px   ✅
```

### spin (Spinner)
```
    ⟳ Gira 360°
Cada 0.8s
Infinito
```

### bounce (Icono)
```
    ▲
    │  ↑ Sube 5px
────┼────
    │  ↓ Baja 5px
    ▼

Cada 2s, infinito
```

---

## Layout Responsivo

### Desktop (1024px+)
```
┌────────────────────────────────────┐
│        ✨ ContentFlow             │
├────────────────┬────────────────────┤
│                │                    │
│   Formulario   │   Salida           │
│                │                    │
│   50%          │   50%              │
│                │                    │
└────────────────┴────────────────────┘
│         Footer                     │
└────────────────────────────────────┘
```

### Tablet (641-1024px)
```
┌────────────────────────────┐
│   ✨ ContentFlow          │
├────────────────────────────┤
│                            │
│      Formulario            │
│                            │
├────────────────────────────┤
│                            │
│       Salida               │
│                            │
└────────────────────────────┘
│      Footer               │
└────────────────────────────┘
```

### Móvil (<640px)
```
┌──────────────┐
│ ✨ Content   │
├──────────────┤
│  Formulario  │
│   (100%)     │
│              │
├──────────────┤
│    Salida    │
│   (100%)     │
│              │
├──────────────┤
│   Footer     │
└──────────────┘
```

---

## Validaciones Visuales

### Campo Requerido vs Optional
```
Requerido:
● Tema Principal        ← Punto azul

Opcional:
◦ Info Adicional        ← Punto verde
```

### Estados de Campo
```
Normal:          Input vacío, borde gris claro

Focus:           Input activo, borde azul, sombra azul

Error:           Input con error, borde rojo, fondo rojo suave

Lleno:           Input con valor, borde gris oscuro

Success:         Input válido (implícito cuando se envía)
```

---

## Ejemplo Completo: Flujo de Usuario

### 1. Estado Inicial
```
┌────────────────────────────────────┐
│   ✨ ContentFlow                  │
├────────────┬────────────────────────┤
│ Tema       │  ✨ Contenido         │
│ [______]   │                        │
│ Platform   │    Sin contenido aún   │
│ [v]        │                        │
│ Audience   │    📄                  │
│ [______]   │                        │
│            │    Completa el         │
│ [Generar]  │    formulario...       │
└────────────┴────────────────────────┘
```

### 2. Usuario Escribe
```
┌────────────────────────────────────┐
│   ✨ ContentFlow                  │
├────────┬──────────────────────────┤
│ Tema   │  ✨ Contenido           │
│ [AI ↓] │                          │
│ Plat.  │    Sin contenido aún     │
│ [Blog] │                          │
│ Aud.   │    📄                    │
│ [Devs] │                          │
│ Info   │                          │
│ [texto]│                          │
│ [✨Gen]│                          │
└────────┴──────────────────────────┘
```

### 3. Cargando
```
┌────────────────────────────────────┐
│   ✨ ContentFlow                  │
├────────┬──────────────────────────┤
│ (Form  │  ✨ Contenido           │
│  dis)  │                          │
│        │      ⟳                   │
│        │  Generando...            │
│        │                          │
└────────┴──────────────────────────┘
```

### 4. Resultado
```
┌────────────────────────────────────┐
│   ✨ ContentFlow                  │
├────────┬──────────────────────────┤
│ (Forma │  ✨ Contenido           │
│  reset)│                          │
│        │  Este es tu contenido   │
│        │  generado por IA...     │
│        │                          │
│        │ [📋 Copiar]             │
│        │ [⬇️ Descargar]          │
└────────┴──────────────────────────┘
```

---

**Ejemplos Visuales - ContentFlow v2.0**  
*Cada detalle diseñado para profesionalismo*

