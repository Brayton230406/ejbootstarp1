# Auditoría WCAG 2.2 AA, UX y diseño responsive

**Alcance:** `index.html`, `styles.css` y `script.js` de `paginaCristianoRonaldo`.

**Tipo de revisión:** no destructiva. No se modificaron los tres archivos auditados. Solo se creó este informe.

**Entorno de prueba:** página servida en `http://127.0.0.1:4173/paginaCristianoRonaldo/`, Chromium mediante Playwright, 10 de septiembre de 2026.

## 1. Resumen ejecutivo

La página tiene una base técnica buena: utiliza `<!doctype html>`, idioma `es`, viewport, `header`, `nav`, `main`, `section` y `footer`; mantiene una jerarquía de encabezados coherente; ofrece nombres accesibles para la navegación, imágenes con `alt`, botones reales para la línea de tiempo, enlaces nativos, enlace para saltar al contenido y un foco visible.

No se detectaron errores JavaScript en ejecución ni overflow horizontal en 320, 390, 768 o 1440 px. La interacción de la línea de tiempo funciona con teclado y actualiza correctamente `aria-expanded` y `hidden`.

Hay dos incumplimientos de nivel alto para WCAG 2.2 AA relacionados con contraste de contenido informativo y un incumplimiento de nivel medio relacionado con los objetivos táctiles. También hay mejoras medias de robustez de imágenes y semántica de datos. Los colores cumplen en algunas zonas oscuras, pero la paleta dorada/gris no alcanza contraste suficiente en varias zonas claras.

## 2. Hallazgos críticos, altos, medios y bajos

### Críticos

No se encontraron hallazgos críticos justificables.

### Altos

#### A-01. Contraste insuficiente del dorado sobre fondo claro

- **Criterio:** WCAG 1.4.3 Contraste mínimo, nivel AA.
- **Evidencia:** `styles.css`, variables `--gold: #d5a84c` y `--paper: #f2efe8`; se aplica a `h1 span`, `h2 em` y textos `.eyebrow` en fondos claros.
- **Medición:** dorado sobre papel: **1.92:1**. El contraste mínimo requerido es 4.5:1 para texto normal y 3:1 para texto grande.
- **Elementos afectados:** `#timeline-title em`, `h2 em` de secciones claras y cualquier `.eyebrow` colocado sobre `--paper`.
- **Recomendación:** usar un dorado más oscuro para texto, por ejemplo un tono validado con contraste mínimo 4.5:1, y conservar el dorado actual solo para elementos decorativos o fondos. Repetir la medición con una herramienta WCAG antes de aprobar.

#### A-02. Contraste insuficiente del texto blanco sobre fondo dorado

- **Criterio:** WCAG 1.4.3 Contraste mínimo, nivel AA.
- **Evidencia:** `styles.css`, `.closing-inner h2 em { color: var(--white); }` sobre `.closing-section { background: var(--gold); }`.
- **Medición:** blanco sobre dorado: **2.17:1**, por debajo de 3:1 incluso para texto grande.
- **Elemento afectado:** el texto “cuando cambia el escenario.” dentro del encabezado final.
- **Recomendación:** cambiar el texto a `--ink` o cambiar el fondo a un dorado suficientemente oscuro. Verificar también el estado hover y cualquier combinación de texto sobre el fondo dorado.

#### A-03. Texto gris insuficiente en zonas claras

- **Criterio:** WCAG 1.4.3 Contraste mínimo, nivel AA.
- **Evidencia:** `styles.css`, `--muted: #77786f` sobre `--paper: #f2efe8`; se usa en `.section-label`, `.section-note`, `.site-nav` y `.site-footer`.
- **Medición:** gris sobre papel: **3.89:1**. Los tamaños observados son aproximadamente 12.8–13.6 px, por lo que no aplican como texto grande.
- **Elementos afectados:** enlaces “Historia”, “Números”, “Galería”, etiquetas de sección, notas y texto del pie.
- **Recomendación:** oscurecer `--muted` hasta alcanzar al menos 4.5:1 en fondos claros. Si se usa el mismo token sobre fondo oscuro, comprobar ambas combinaciones por separado o definir tokens específicos para superficies claras y oscuras.

### Medios

#### M-01. Objetivos táctiles de la navegación por debajo de 24 × 24 CSS px

- **Criterio:** WCAG 2.2 2.5.8 Tamaño mínimo del objetivo, nivel AA.
- **Evidencia:** `styles.css`, `.site-nav a` no tiene padding ni un área mínima; en las pruebas sus cajas midieron aproximadamente 43 × 18 px, 50 × 18 px y 39 × 18 px a 320/390 px.
- **Elementos afectados:** enlaces `Historia`, `Números` y `Galería` de `index.html`.
- **Recomendación:** añadir un área clicable mínima de 24 × 24 px, preferiblemente con `padding: .35rem .25rem` y un margen/gap que conserve la composición. Repetir la prueba en 320 px para comprobar que no aparece overflow.

#### M-02. Imágenes sin dimensiones reservadas

- **Criterio relacionado:** estabilidad visual, UX responsive y buenas prácticas de rendimiento; impacta la experiencia aunque no sea por sí solo un incumplimiento WCAG automático.
- **Evidencia:** `index.html`, las tres imágenes `.gallery-card img` usan `loading="lazy"`, pero no tienen `width`/`height`; `styles.css` fija `height` pero no define una relación de aspecto reservada antes de descargar.
- **Riesgo:** puede producir desplazamiento de contenido mientras cargan las imágenes, especialmente con red lenta o al abrir la galería en móvil.
- **Recomendación:** añadir dimensiones proporcionales reales o `aspect-ratio` en `.gallery-card img` y mantener `object-fit: cover`. Comprobar la carga con throttling de red.

#### M-03. Uso de imagen principal como fondo CSS

- **Criterio relacionado:** robustez, mantenimiento y experiencia con CSS bloqueado o imágenes no disponibles.
- **Evidencia:** `styles.css`, `.hero-portrait` usa `background: ... url(...)`; `index.html` representa el contenido con un `div role="img" aria-label`.
- **Resultado actual:** el nombre accesible es correcto y no se marca como error de nombre alternativo.
- **Riesgo:** un fondo CSS no ofrece dimensiones, fallback ni el comportamiento nativo de una imagen; además, el nombre accesible depende de que el `div` mantenga correctamente el rol ARIA.
- **Recomendación:** valorar un `<img>` real con `alt`, `width`, `height` y `object-fit: cover` dentro del contenedor. Si se mantiene el fondo, añadir un color de fallback y probar con CSS/imágenes deshabilitados.

#### M-04. Estadísticas sin semántica explícita de relación término-valor

- **Criterio relacionado:** estructura semántica y comprensión por tecnologías de asistencia.
- **Evidencia:** `index.html`, `.stats-grid` contiene cuatro `div` con `<strong>` y `<span>`.
- **Resultado actual:** el texto es visible y legible, pero no se expone como un conjunto de términos y valores.
- **Recomendación:** usar `<dl>` con `<dt>` para cada etiqueta y `<dd>` para cada cifra, o una lista estructurada equivalente. Mantener el diseño visual mediante CSS.

### Bajos

#### B-01. Carga duplicada de la tipografía

- **Evidencia:** `index.html` carga Google Fonts mediante `<link>` y `styles.css` vuelve a cargar las mismas familias con `@import`.
- **Impacto:** petición redundante y mayor complejidad de carga.
- **Recomendación:** conservar solo la carga del HTML mediante `<link>` y eliminar el `@import` del CSS.

#### B-02. Fuente de datos con fecha de referencia antigua

- **Evidencia:** `index.html`, `.data-note` indica “Actualizados hasta 2024”, mientras el sitio se audita en 2026.
- **Impacto:** no es un fallo WCAG, pero puede inducir a interpretar las cifras como actuales.
- **Recomendación:** indicar una fecha de corte real y enlazar una fuente que mantenga esos datos actualizados, o redactar claramente que son cifras históricas.

## 3. Criterios que cumplen

- **Estructura semántica:** cumple en lo revisado. Hay `header`, `nav`, `main`, `section`, `article`, `figure`, `figcaption` y `footer`. El elemento pedido como `main` existe correctamente.
- **Idioma del documento:** cumple. `html lang="es"` está presente.
- **Jerarquía de encabezados:** cumple. Hay un único `h1` y cinco `h2`; no hay saltos de nivel observados.
- **Nombres accesibles:** cumple en los controles revisados. El `nav` tiene `aria-label`, la marca tiene `aria-label`, los botones tienen texto visible y los enlaces tienen nombres comprensibles.
- **Textos alternativos:** cumple en las tres imágenes HTML. Todas tienen `alt` descriptivo y no se detectaron imágenes sin atributo `alt`.
- **Enlaces externos:** cumple en lo revisado. Los enlaces con `target="_blank"` incluyen `rel="noopener noreferrer"`.
- **Uso de controles:** cumple. La línea de tiempo usa `<button type="button">` para una acción y los destinos externos/internos usan `<a>`.
- **ARIA de la línea de tiempo:** cumple funcionalmente. Cada botón tiene `aria-expanded` y `aria-controls`; los paneles cerrados usan `hidden`.
- **Navegación con teclado:** cumple en la prueba realizada. El primer `Tab` llega al enlace para saltar al contenido y los controles son elementos nativos enfocables.
- **Foco visible:** cumple en la prueba realizada. `:focus-visible` aplica un contorno de 3 px con desplazamiento de 4 px; Chromium mostró el foco del skip link.
- **Reducción de movimiento:** cumple parcialmente de forma positiva. `prefers-reduced-motion: reduce` desactiva prácticamente las transiciones y el desplazamiento suave.
- **Responsive y overflow:** cumple en las dimensiones probadas. No hubo overflow horizontal: el `scrollWidth` coincidió con el ancho de cliente en 320, 390, 768 y 1440 px.
- **Imágenes cargadas:** cumple en la prueba con viewport. Las tres imágenes de galería cargaron con ancho natural mayor que cero.
- **Errores JavaScript:** cumple en ejecución. No se registraron `pageerror` durante la carga, la navegación ni la prueba de la línea de tiempo.

## 4. Evidencia concreta y recomendaciones de corrección

| ID | Archivo y elemento | Evidencia | Corrección recomendada |
|---|---|---|---|
| A-01 | `styles.css`, `--gold`, `h1 span`, `h2 em` | `#d5a84c` sobre `#f2efe8`: 1.92:1 | Oscurecer el token para texto o reservarlo para decoración/fondo. |
| A-02 | `styles.css`, `.closing-inner h2 em` | `#fffdf7` sobre `#d5a84c`: 2.17:1 | Usar `--ink` o un fondo dorado más oscuro. |
| A-03 | `styles.css`, `--muted`, `.site-nav`, `.section-note`, `.site-footer` | `#77786f` sobre `#f2efe8`: 3.89:1 | Definir un gris más oscuro para superficies claras. |
| M-01 | `index.html` enlaces de `.site-nav`; `styles.css` `.site-nav a` | Alturas medidas de 18–20 px | Añadir padding y mínimo de 24 × 24 px. |
| M-02 | `index.html` imágenes de `.gallery-card` | No hay `width`/`height`; solo `loading="lazy"` | Añadir dimensiones o `aspect-ratio`. |
| M-03 | `styles.css` `.hero-portrait` | Imagen principal como `background-image` | Considerar `<img>` real con `alt` y dimensiones, o reforzar fallback. |
| M-04 | `index.html` `.stats-grid` | Cifras y etiquetas son `div` sin relación semántica | Cambiar a `<dl>`, `<dt>` y `<dd>`. |
| B-01 | `index.html` fuentes y `styles.css` `@import` | Dos mecanismos cargan las mismas fuentes | Mantener una sola carga. |
| B-02 | `index.html` `.data-note` | Fecha de datos: 2024 | Actualizar o explicitar la fecha de corte histórica. |

## 5. Pruebas que deberían repetirse después de corregir

1. Ejecutar un análisis automático WCAG 2.2 AA con axe-core, Lighthouse o Accessibility Insights y revisar manualmente los resultados.
2. Recalcular contraste de todos los textos en sus fondos reales, incluidos hover, focus, `:visited` y la sección dorada final.
3. Repetir teclado completo: `Tab`, `Shift+Tab`, `Enter` y `Space`; confirmar que el foco nunca desaparece y que los cuatro capítulos abren y cierran su panel.
4. Comprobar que el foco no queda oculto tras el encabezado al saltar a `#historia`, `#numeros` o `#galeria`.
5. Medir todos los enlaces de navegación con una herramienta de cajas visuales y confirmar objetivos de al menos 24 × 24 CSS px en 320 y 390 px.
6. Repetir pruebas en 320 × 800, 390 × 844, 768 × 900 y un escritorio de al menos 1280 px; comprobar `scrollWidth`, recortes, saltos de línea y legibilidad.
7. Probar zoom del navegador al 200 % y 400 %, además de texto aumentado, buscando pérdida de contenido, solapamientos u overflow.
8. Probar con `prefers-reduced-motion: reduce` y con teclado sin ratón.
9. Simular red lenta y caché vacía; comprobar que las imágenes reservan espacio, muestran fallback razonable y no provocan saltos de layout.
10. Ejecutar el JavaScript con un runtime disponible mediante `node --check script.js` y volver a comprobar la consola del navegador.
11. Verificar los enlaces externos y la vigencia de las cifras antes de publicar.

## Validación realizada

- Los archivos auditados existen: `index.html`, `styles.css` y `script.js`.
- El sitio se sirvió desde un servidor HTTP local.
- La página cargó con el título esperado.
- La línea de tiempo respondió a interacción y teclado; el panel pasó de `aria-expanded="false"` a `true`.
- No hubo errores JavaScript de página durante las pruebas.
- Las tres imágenes de galería cargaron correctamente después de entrar en viewport.
- No se detectó overflow horizontal en 320, 390, 768 ni 1440 px.
- `node` no está disponible en el entorno actual, por lo que no fue posible ejecutar `node --check`; la sintaxis y el comportamiento se validaron ejecutando `script.js` en Chromium sin errores.
