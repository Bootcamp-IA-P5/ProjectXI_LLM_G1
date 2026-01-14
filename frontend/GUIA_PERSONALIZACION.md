# 🎯 Guía de Personalización y Extensión

## Cómo Personalizar los Estilos

### Opción 1: Cambiar Variables Globales

El camino más fácil para personalizar la app es modificar las variables CSS en `src/styles/variables.css`:

```css
:root {
    /* Cambiar solo los colores que quieras */
    --primary-blue: #3b82f6;      /* Nuevo azul */
    --primary-purple: #a855f7;    /* Nuevo morado */
    --accent-cyan: #0891b2;       /* Nuevo cyan */
}
```

**Ventaja**: Un cambio actualiza toda la app automáticamente.

---

## Ejemplos de Personalización

### Ejemplo 1: Tema Verde (Green Startup)

```css
/* En src/styles/variables.css */
:root {
    --primary-dark: #065f46;      /* Verde oscuro */
    --primary-blue: #10b981;      /* Verde principal */
    --primary-purple: #059669;    /* Verde más oscuro */
    --accent-cyan: #34d399;       /* Verde claro */
    --accent-green: #6ee7b7;      /* Verde muy claro */
}
```

### Ejemplo 2: Tema Naranja (Creative Agency)

```css
:root {
    --primary-dark: #7c2d12;      /* Marrón oscuro */
    --primary-blue: #ea580c;      /* Naranja */
    --primary-purple: #f97316;    /* Naranja más claro */
    --accent-cyan: #fb923c;       /* Naranja claro */
    --accent-green: #fcd34d;      /* Amarillo */
}
```

### Ejemplo 3: Tema Minimalista (Tech)

```css
:root {
    --primary-dark: #1f2937;      /* Gris oscuro */
    --primary-blue: #111827;      /* Negro */
    --primary-purple: #374151;    /* Gris medio */
    --accent-cyan: #6b7280;       /* Gris claro */
    --accent-green: #9ca3af;      /* Gris muy claro */
}
```

---

## Crear Nuevos Componentes

### Estructura Base para un Componente

```jsx
// src/components/NewComponent.jsx
import '../styles/NewComponent.css';

export default function NewComponent(props) {
    return (
        <div className="component-container">
            <h2 className="component-title">Título</h2>
            <p className="component-text">Contenido</p>
        </div>
    );
}
```

### Archivo de Estilos Correspondiente

```css
/* src/styles/NewComponent.css */
@import './variables.css';

.component-container {
    background: var(--card-bg);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
    transition: all var(--transition-normal);
}

.component-container:hover {
    box-shadow: var(--shadow-lg);
}

.component-title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-bold);
    color: var(--text-dark);
    margin-bottom: var(--spacing-md);
}

.component-text {
    color: var(--text-light);
    line-height: 1.6;
}
```

---

## Agregar Nuevas Variables

Si necesitas agregar variables para un nuevo componente:

```css
/* En src/styles/variables.css, dentro de :root */

:root {
    /* Variables existentes... */
    
    /* Nuevas variables para nuevo componente */
    --component-bg: #f8fafc;
    --component-border: 2px solid;
    --component-padding: var(--spacing-lg);
}
```

Luego úsalas en tu CSS:

```css
.mi-componente {
    background: var(--component-bg);
    border: var(--component-border);
    padding: var(--component-padding);
}
```

---

## Crear Variantes de Botones

### Agregar nuevos tipos de botones

```css
/* En src/styles/App.css o archivo específico */

/* Botón Terciario */
.btn-tertiary {
    background: transparent;
    color: var(--primary-blue);
    border: 2px solid var(--primary-blue);
    transition: all var(--transition-normal);
}

.btn-tertiary:hover {
    background: var(--primary-blue);
    color: white;
}

/* Botón Pequeño */
.btn-sm {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-sm);
}

/* Botón Grande */
.btn-lg {
    padding: var(--spacing-lg) var(--spacing-xl);
    font-size: var(--font-size-lg);
}

/* Botón Full Width */
.btn-full {
    width: 100%;
}
```

### Usarlos en JSX

```jsx
<button className="btn-primary btn-sm">Pequeño</button>
<button className="btn-secondary btn-lg btn-full">Grande Full</button>
<button className="btn-tertiary">Terciario</button>
```

---

## Crear Utilidades CSS

### Agregar clases de utilidad reutilizables

```css
/* En src/styles/variables.css o nuevo archivo utilities.css */

/* Espaciado */
.p-1 { padding: var(--spacing-md); }
.p-2 { padding: var(--spacing-lg); }
.p-3 { padding: var(--spacing-xl); }

.m-1 { margin: var(--spacing-md); }
.m-2 { margin: var(--spacing-lg); }

/* Flexbox */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.gap-1 { gap: var(--spacing-md); }
.gap-2 { gap: var(--spacing-lg); }

/* Texto */
.text-sm { font-size: var(--font-size-sm); }
.text-lg { font-size: var(--font-size-lg); }
.font-bold { font-weight: var(--font-weight-bold); }
.text-center { text-align: center; }

/* Colores */
.text-primary { color: var(--primary-blue); }
.text-secondary { color: var(--text-light); }
.bg-light { background: var(--light-bg); }
.bg-card { background: var(--card-bg); }

/* Bordes */
.rounded { border-radius: var(--border-radius-md); }
.rounded-lg { border-radius: var(--border-radius-lg); }
.border { border: 1px solid var(--border-color); }
```

### Usarlas en JSX

```jsx
<div className="flex flex-col items-center gap-2 p-3">
    <h3 className="text-lg font-bold text-primary">Título</h3>
    <p className="text-sm text-secondary">Descripción</p>
</div>
```

---

## Crear Animaciones Personalizadas

### Agregar nuevas animaciones

```css
/* En src/styles/variables.css o archivo específico */

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes flipIn {
    0% {
        opacity: 0;
        transform: rotateY(90deg);
    }
    100% {
        opacity: 1;
        transform: rotateY(0);
    }
}

.animate-slideUp {
    animation: slideUp var(--transition-slow);
}

.animate-flipIn {
    animation: flipIn 0.6s ease-in-out;
}
```

### Usarlas

```jsx
<div className="animate-slideUp">Contenido animado</div>
<div className="animate-flipIn">Flip animado</div>
```

---

## Agregar un Tema Oscuro

### Crear variables para modo oscuro

```css
/* En src/styles/variables.css */

/* Agregar al final */
[data-theme="dark"] {
    --light-bg: #1e293b;
    --card-bg: #0f172a;
    --text-dark: #f8fafc;
    --text-light: #cbd5e1;
    --border-color: #334155;
}
```

### Agregar toggle en App.jsx

```jsx
import { useState } from 'react';

export default function App() {
    const [theme, setTheme] = useState('light');
    
    function toggleTheme() {
        setTheme(theme === 'light' ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme === 'light' ? 'dark' : 'light');
    }
    
    return (
        <div data-theme={theme}>
            <button onClick={toggleTheme}>
                {theme === 'light' ? '🌙' : '☀️'}
            </button>
            {/* ... resto del app ... */}
        </div>
    );
}
```

---

## Mejorar la Validación del Formulario

### Agregar validación de email

```jsx
// En ContentForm.jsx
function validateForm() {
    const newErrors = {};
    
    // Validación existente...
    if (tema.trim() === "") {
        newErrors.tema = "El tema es requerido";
    }
    
    // Nueva validación de email (si es necesario)
    if (email && !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        newErrors.email = "Email inválido";
    }
    
    return newErrors;
}
```

### Validación de longitud mínima

```jsx
if (tema.trim().length < 3) {
    newErrors.tema = "El tema debe tener al menos 3 caracteres";
}

if (audiencia.trim().length < 5) {
    newErrors.audiencia = "Describe mejor tu audiencia (mín. 5 caracteres)";
}
```

---

## Agregar Iconos (FontAwesome o similar)

### Opción 1: Usar CDN

```html
<!-- En public/index.html -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

### Opción 2: Instalar librería

```bash
npm install react-icons
```

Luego usarla:

```jsx
import { FaFire, FaStar } from "react-icons/fa";

export default function Component() {
    return (
        <button>
            <FaFire /> Generar
        </button>
    );
}
```

---

## Performance - Optimizar CSS

### Minificar para producción

```bash
npm run build
```

Esto automáticamente minifica y optimiza todo el CSS.

### Lazy load componentes

```jsx
import { lazy, Suspense } from 'react';

const OutputDisplay = lazy(() => import('./components/OutputDisplay'));

export default function App() {
    return (
        <Suspense fallback={<div>Cargando...</div>}>
            <OutputDisplay />
        </Suspense>
    );
}
```

---

## Pruebas de Accesibilidad

### Verificar contrastes

```
Usar herramienta: https://webaim.org/resources/contrastchecker/
```

### Verificar navegación con teclado

```
- Tab: Navega entre elementos
- Shift+Tab: Navega hacia atrás
- Enter: Activa botones
- Space: Activa checkboxes
```

### Verificar con screen reader

```
- NVDA (gratis): https://www.nvaccess.org/
- JAWS (pago)
- VoiceOver (Mac integrado)
```

---

## Estructura Recomendada para Proyectos Grandes

```
frontend/src/
├── styles/
│   ├── variables.css         # Variables globales
│   ├── App.css              # App principal
│   ├── components/          # Estilos por componente
│   │   ├── Button.css
│   │   ├── Form.css
│   │   └── Card.css
│   ├── utils/               # Utilidades
│   │   ├── animations.css
│   │   ├── responsive.css
│   │   └── typography.css
│   └── themes/              # Temas
│       ├── light.css
│       └── dark.css
├── components/
│   ├── Button.jsx
│   ├── Form.jsx
│   └── ...
└── ...
```

---

## Recursos Útiles

- **Color**: https://coolors.co/
- **Gradientes**: https://gradient.page/
- **Sombras**: https://www.shadowpalette.com/
- **Tipografía**: https://fonts.google.com/
- **Iconos**: https://heroicons.com/
- **Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/

---

**Guía de Personalización - ContentFlow v2.0**  
*¡Haz que el diseño sea tuyo!*

