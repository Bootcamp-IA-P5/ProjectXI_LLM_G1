# 🎨 Guía de Diseño - ContentFlow

## Paleta de Colores Profesional

### Colores Primarios

#### 🔵 Azul Oscuro (Primary Dark)
```css
--primary-dark: #0f172a
RGB: (15, 23, 42)
Uso: Header, fondos oscuros, navegación
```
**Características:** Profundo, profesional, confiable

#### 🟦 Azul Vibrante (Primary Blue)
```css
--primary-blue: #2563eb
RGB: (37, 99, 235)
Uso: Botones principales, acentos, links
```
**Características:** Vibrante, energético, llamativo

#### 🟪 Morado Elegante (Primary Purple)
```css
--primary-purple: #7c3aed
RGB: (124, 58, 237)
Uso: Gradientes, títulos, acentos secundarios
```
**Características:** Elegante, diferenciador, moderno

### Colores de Acento

#### 🔶 Cyan/Verde Agua (Accent Cyan)
```css
--accent-cyan: #06b6d4
RGB: (6, 182, 212)
Uso: Botones secundarios, acentos, efectos hover
```
**Características:** Refrescante, moderno, accesible

#### 🟢 Verde Profesional (Accent Green)
```css
--accent-green: #10b981
RGB: (16, 185, 129)
Uso: Estados de éxito, confirmaciones, positivo
```
**Características:** Positivo, tranquilizador, accesible

### Colores de Estado

#### 🔴 Rojo Error (Error Color)
```css
--error-color: #ef4444
RGB: (239, 68, 68)
Uso: Errores, advertencias, validaciones negativas
```
**Características:** Claro, urgente, visible

#### ⚠️ Ámbar Advertencia
```css
--warning-color: #f59e0b
RGB: (245, 158, 11)
Uso: Advertencias, información importante
```

#### ℹ️ Azul Información
```css
--info-color: #2563eb
RGB: (37, 99, 235)
Uso: Información, tips, help
```

### Escala de Grises

#### Fondos
```css
--light-bg: #f8fafc      (Fondo claro principal)
--card-bg: #ffffff        (Fondos de tarjetas)
--dark-bg: #0f172a        (Fondo oscuro)
```

#### Texto
```css
--text-dark: #1e293b      (Texto principal - oscuro)
--text-light: #64748b     (Texto secundario - gris medio)
--text-lighter: #94a3b8   (Texto terciario - gris claro)
--text-white: #ffffff     (Texto en fondos oscuros)
```

#### Bordes y Separadores
```css
--border-color: #e2e8f0       (Bordes sutiles - gris claro)
--border-color-dark: #cbd5e1  (Bordes más visibles - gris medio)
```

---

## Uso de Colores por Componente

### Header
```css
Fondo: Linear-gradient(135deg, --primary-dark, --primary-blue)
Texto: --text-white
Acentos: --primary-purple, --accent-cyan
```

### Botones

#### Botón Principal (Submit)
```css
Fondo: Linear-gradient(135deg, --primary-blue, --accent-cyan)
Texto: --text-white
Hover: Más saturado
Sombra: rgba(37, 99, 235, 0.3)
```

#### Botón Secundario
```css
Fondo: --light-bg
Borde: 2px --border-color
Texto: --text-dark
Hover: --border-color más oscuro
```

#### Botón Copiar/Éxito
```css
Fondo: Linear-gradient(135deg, --accent-green, --accent-cyan)
Texto: --text-white
```

### Formulario

#### Inputs/Selects/Textarea
```css
Fondo: --light-bg
Borde: 2px --border-color
Texto: --text-dark
Focus: 
  - Borde: --primary-blue
  - Fondo: white
  - Box-shadow: rgba(37, 99, 235, 0.1)
```

#### Labels
```css
Texto: --text-dark
Font-weight: 600
Indicador: Punto pequeño (--primary-blue)
```

### Validación

#### Campo con Error
```css
Borde: --error-color
Fondo: rgba(239, 68, 68, 0.05)
Texto error: --error-color
```

#### Mensaje de Error
```css
Fondo: rgba(239, 68, 68, 0.05)
Borde izquierdo: 4px --error-color
Texto: --text-dark
```

### Salida

#### Container Carga
```css
Spinner border: --border-color
Spinner top: --primary-blue
Spinner right: --primary-purple
```

#### Container Error
```css
Fondo: rgba(239, 68, 68, 0.05)
Borde: 2px --error-color
Título: --error-color
```

#### Container Vacío
```css
Icono: Opacidad 0.5
Texto: --text-light
Fondo: Transparent
```

---

## Gradientes Recomendados

### Gradiente Primario (Azul a Cyan)
```css
background: linear-gradient(135deg, #2563eb, #06b6d4);
Uso: Botones principales, efectos especiales
```

### Gradiente Morado a Cyan
```css
background: linear-gradient(135deg, #7c3aed, #06b6d4);
Uso: Títulos, texto resaltado
```

### Gradiente Éxito (Verde a Cyan)
```css
background: linear-gradient(135deg, #10b981, #06b6d4);
Uso: Estados positivos, confirmaciones
```

### Gradiente Sutil (Azul claro)
```css
background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(124, 58, 237, 0.1));
Uso: Fondos de secciones, headers internas
```

---

## Sombras por Intensidad

### Sombra Pequeña (Elementos sutiles)
```css
box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
Uso: Elementos pequeños, separadores
```

### Sombra Media (Tarjetas)
```css
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
Uso: Tarjetas, containers principales
```

### Sombra Grande (Elevación)
```css
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
Uso: Modales, componentes elevados
```

### Sombra Extra Grande (Máxima elevación)
```css
box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
Uso: Overlays, popups importantes
```

### Sombras de Color (Especiales)
```css
box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2);  /* Azul */
box-shadow: 0 10px 15px -3px rgba(124, 58, 237, 0.2); /* Morado */
box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.2); /* Verde */
Uso: Botones, elementos destacados
```

---

## Combinaciones de Color Recomendadas

### Combinación 1: Profesional
```
Fondo: #f8fafc (Light)
Primario: #2563eb (Blue)
Secundario: #7c3aed (Purple)
Acento: #06b6d4 (Cyan)
Texto: #1e293b (Dark)
```

### Combinación 2: Moderno
```
Fondo: #ffffff (White)
Primario: #7c3aed (Purple)
Secundario: #06b6d4 (Cyan)
Acento: #10b981 (Green)
Texto: #0f172a (DarkDark)
```

### Combinación 3: Energético
```
Fondo: #f1f5f9 (Very Light)
Primario: #2563eb (Blue)
Secundario: #06b6d4 (Cyan)
Acento: #f97316 (Orange)
Texto: #1e293b (Dark)
```

---

## Accesibilidad de Color

### Ratio de Contraste (WCAG AA)
- ✅ **Texto oscuro (#1e293b) sobre fondo claro (#f8fafc)**: 9.5:1
- ✅ **Texto blanco (#ffffff) sobre azul (#2563eb)**: 4.5:1
- ✅ **Texto oscuro sobre rojo (#ef4444)**: 3.5:1
- ✅ **Texto blanco sobre morado (#7c3aed)**: 4.5:1

### No Confiar Solo en Color
- ✅ Usar iconos junto a colores
- ✅ Usar patrones o texturas
- ✅ Usar texto descriptivo
- ✅ Usar bordes y sombras

---

## Tips de Diseño

1. **Consistencia**: Usar siempre los mismos colores para las mismas acciones
2. **Claridad**: El contraste debe ser suficiente para leer cómodamente
3. **Jerarquía**: Los colores primarios para acciones principales
4. **Descanso Visual**: Incluir espacios en blanco y colores neutros
5. **Emociones**: Los colores evocan emociones, úsalo a tu favor
   - Azul: Confianza, profesionalismo
   - Morado: Creatividad, elegancia
   - Verde: Éxito, naturaleza
   - Rojo: Urgencia, error

---

## Personalización

Para cambiar la paleta global, solo modifica `src/styles/variables.css`:

```css
:root {
    --primary-blue: #3b82f6;      /* Cambia aquí */
    --primary-purple: #a855f7;    /* Y aquí */
    --accent-cyan: #0891b2;       /* Y aquí */
}
```

Todos los componentes se actualizar automáticamente.

---

**Guía de Diseño - ContentFlow v2.0**  
*Mantén la consistencia para una experiencia visual profesional*

