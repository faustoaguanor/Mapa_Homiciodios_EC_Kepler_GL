<div align="center">

# 🗺️ Mapa de homicidios en Ecuador con Kepler.gl

**Una guía práctica para construir, personalizar y publicar un mapa interactivo con [Kepler.gl](https://kepler.gl)**
usando como ejemplo los clústeres LISA de homicidios (urbano vs rural).

[Ver mapa](https://faustoaguanor.github.io/Mapa_Homiciodios_EC_Kepler_GL/) · [Guía de uso](#-guía-de-uso-de-keplergl) · [Publicar tu mapa](#-publica-tu-propio-mapa)

</div>

---

## ✨ ¿Qué es Kepler.gl?

Kepler.gl es una herramienta de código abierto (creada por Uber, hoy en OpenJS Foundation) para **explorar y visualizar datos geoespaciales en el navegador**, con renderizado WebGL (deck.gl) capaz de manejar cientos de miles de puntos. No requiere servidor ni base de datos: arrastras un archivo y construyes el mapa.

Este repositorio muestra el flujo completo: **diseñar el mapa en Kepler.gl → exportar su configuración → empaquetarlo en una sola página HTML y publicarlo.**

| Lo que hace Kepler.gl | Cómo lo aprovecha este mapa |
| --- | --- |
| Capas de polígonos, puntos, calor, arcos, H3… | Polígonos cantonales coloreados por categoría |
| **Vista dividida** (*split map*) | Urbano a la izquierda, rural a la derecha |
| Color por campo (escala ordinal, cuantiles…) | Color por `lisa_cluster` con paleta personalizada |
| Tooltips configurables | Cantón, conteo, clúster, I de Moran y p |
| Filtros y línea de tiempo | Disponibles en el editor (ver [consejos](#-consejos)) |
| Exportar/compartir como JSON o HTML | Base de `src/kepler_config.json` |

---

## 🚀 Ver el mapa

- **En línea:** <https://faustoaguanor.github.io/Mapa_Homiciodios_EC_Kepler_GL/>
- **En local:** descarga el repositorio y abre `index.html`, o ejecuta `python3 -m http.server 8000` y entra a <http://localhost:8000>.

> **Requisitos:** navegador moderno con **WebGL activado** y conexión a internet (las librerías y el mapa base se cargan desde CDN).
>
> ⚠️ Si ves *"An error in deck.gl"* o una pantalla de aviso, tu navegador tiene el 3D desactivado:
> - **Firefox:** `about:config` → `webgl.disabled = false` y *Ajustes → General → Rendimiento → Usar aceleración por hardware*.
> - **Chrome / Edge / Brave:** *Configuración → Sistema → Usar aceleración gráfica cuando esté disponible*.
> - Comprueba tu soporte en [get.webgl.org](https://get.webgl.org).

### Cómo usar el mapa

| Acción | Resultado |
| --- | --- |
| Pasar el cursor sobre un cantón | Tooltip con cantón, provincia, homicidios, categoría, clúster LISA, `lisa_i` y `lisa_p` |
| Arrastrar / rueda del ratón | Desplazar / acercar |
| Botón de leyenda (columna derecha) | Ver los colores de cada categoría |
| Pestaña **Metodología y uso** | Abrir o cerrar el panel explicativo |

---

## 📘 Guía de uso de Kepler.gl

Pasos para reproducir un mapa como este desde cero en <https://kepler.gl/demo> (no necesitas instalar nada).

### 1. Cargar los datos
Arrastra tus archivos **GeoJSON** o **CSV** a la ventana. Kepler.gl detecta solo la geometría (GeoJSON) o las columnas `latitude` / `longitude` (CSV) y crea una capa por archivo.

### 2. Configurar las capas
En el panel izquierdo, abre cada capa:

1. **Tipo:** polígonos (*Polygon*) para cantones, *Heatmap* o *Point* para puntos.
2. **Fill color → Color Based On:** elige el campo (aquí `lisa_cluster`).
3. **Color Scale → Ordinal** y, en la paleta, **personaliza** el color de cada categoría:
   `HH` rojo · `LL` azul · `HL` naranja · `LH` celeste · `No significativo` gris.
4. **Stroke:** reduce el grosor (0.3–0.5) y la opacidad del contorno para que los cantones pequeños no se pierdan.
5. **Opacity:** ~0.8 para que se vea el mapa base.

### 3. Mostrar dos mapas lado a lado (vista dividida)
1. Pulsa el icono **Split Map** (panel de mapa, arriba a la derecha).
2. En cada mitad, usa el icono de **ojo** de cada capa para decidir qué capas ve ese panel.
3. Panel izquierdo → capa urbana · panel derecho → capa rural. Los límites cantonales van en ambos.

### 4. Configurar tooltips
En **Interactions → Tooltip** marca los campos que quieres mostrar al pasar el cursor (cantón, provincia, conteo, categoría, `lisa_cluster`, `lisa_i`, `lisa_p`). Cada capa/dataset tiene su propia lista.

### 5. Elegir el mapa base
En **Base map** selecciona el estilo (este mapa usa *Dark Matter*, que hace resaltar los colores) y activa o desactiva etiquetas, carreteras, agua, etc.

### 6. Exportar la configuración
**Share → Export Map** (HTML) o **Export Map → JSON**. El JSON guarda capas, colores, filtros, tooltips y vista dividida: es el archivo que este repositorio guarda en [`src/kepler_config.json`](src/kepler_config.json).

---

## 🛠️ Publica tu propio mapa

Este repositorio convierte los datos + la configuración en **un único `index.html`** listo para GitHub Pages.

```bash
# 1. Coloca tus GeoJSON/CSV en data/ y tu config exportada en src/kepler_config.json
# 2. Registra los datasets (id, archivo) en la lista DATASETS de scripts/build.py
# 3. Genera la página
python3 scripts/build.py          # solo Python 3, sin dependencias
```

Después, en GitHub: **Settings → Pages → Deploy from a branch → `main` / root**.

### ¿Cómo funciona por dentro?

Kepler.gl se usa **sin servidor**, con su build UMD cargado desde unpkg y montado con React + Redux (`src/app.js`):

```js
// 1. Store con el reducer de Kepler.gl, en solo lectura y con vista dividida
keplerGl: KeplerGl.keplerGlReducer.initialState({
  uiState:  { readOnly: true },
  mapState: { isSplit: true, latitude: -2.71, longitude: -78.51, zoom: 5.78 }
})

// 2. Datos y configuración (la config exportada del editor)
const datasets = [{ info: { id, label }, data: KeplerGl.processGeojson(geojson) }];
const config   = KeplerGl.KeplerGlSchema.parseSavedConfig(savedConfig);

// 3. Cargar todo en el mapa
store.dispatch(KeplerGl.addDataToMap({ datasets, config, options: { centerMap: false } }));
```

### Estructura

```
index.html                 página final (generada; no editar a mano)
src/index.template.html    plantilla HTML y panel lateral
src/app.js                 montaje de Kepler.gl, carga de datos y detección de WebGL
src/styles.css             estilos
src/kepler_config.json     configuración exportada de Kepler.gl
data/                      GeoJSON y CSV de entrada
scripts/build.py           empaquetado
```

### 💡 Consejos

- **Peso:** redondea coordenadas a 5 decimales (~1 m) y no incrustes capas que no se ven. Así este mapa bajó de 27 MB a ~7 MB.
- **Estabilidad:** fija las versiones de las librerías en las URLs de CDN (`kepler.gl@3.3.0-alpha.0`, `react@18.3.1`…).
- **Solo lectura:** `readOnly: true` oculta el editor; quítalo si quieres que los usuarios exploren las capas.
- **Línea de tiempo:** si tienes una columna de fecha, añade un filtro de tipo *time range* en el editor y se exporta con la config. El CSV de puntos con fechas está en `data/homicidios_puntos.csv` para probarlo.
- **Identificadores:** los `id` de dataset y capa deben coincidir entre `kepler_config.json` y `scripts/build.py`.

---

## 📂 Datos de ejemplo (resumen)

| Archivo en `data/` | Qué es |
| --- | --- |
| `hotspots_urbanos_moran.geojson`, `hotspots_rurales_moran.geojson` | Resultado LISA por cantón (`lisa_cluster`, `lisa_i`, `lisa_p`) |
| `homicidios_urbanos_canton.geojson`, `homicidios_rurales_canton.geojson` | Conteo de homicidios por cantón |
| `DPA_Cantonal.geojson` | Límites cantonales (INEC), 224 unidades, clave `DPA_CANTON` |
| `homicidios_puntos.csv` | 41 778 registros 2014 – mar. 2026, sin datos personales de víctimas |

El **LISA** (Índice de Moran Local, Anselin 1995, p < 0.05) clasifica cada cantón en `HH` hotspot, `LL` coldspot, `HL`/`LH` outliers o no significativo.

> *Pendiente del autor:* fuente institucional y fecha de descarga de los homicidios; matriz de pesos, permutaciones y software del LISA.

---

## 🙏 Créditos y librerías de terceros

| Librería | Uso | Licencia |
| --- | --- | --- |
| [Kepler.gl](https://github.com/keplergl/kepler.gl) 3.3.0-alpha.0 (OpenJS Foundation / Uber) | Visualización geoespacial y vista dividida | MIT |
| [deck.gl](https://deck.gl) (incluido en Kepler.gl) | Renderizado WebGL | MIT |
| [MapLibre GL JS](https://maplibre.org) 3.6 | Renderizado del mapa base | BSD-3-Clause |
| [React](https://react.dev) / ReactDOM 18.3.1 | Interfaz | MIT |
| [Redux](https://redux.js.org) 4.2.1 / [React-Redux](https://react-redux.js.org) 8.1.2 | Estado de la aplicación | MIT |
| [styled-components](https://styled-components.com) 6.1.8 | Estilos de Kepler.gl | MIT |
| [CARTO Dark Matter](https://carto.com/basemaps) · © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors | Mapa base | CC BY 3.0 / ODbL |

Límites cantonales © [INEC Ecuador](https://www.ecuadorencifras.gob.ec). Metodología: Anselin, L. (1995), *Local Indicators of Spatial Association — LISA*, Geographical Analysis 27(2).

## 📄 Licencia y autoría

Contenido propio bajo [CC BY 4.0](LICENSE); las librerías de terceros conservan sus licencias.

**Autor:** [faustoaguanor](https://github.com/faustoaguanor)
Cita: faustoaguanor (2026). *Clústeres espaciales de homicidios en Ecuador (LISA urbano vs rural)*. GitHub. https://github.com/faustoaguanor/Mapa_Homiciodios_EC_Kepler_GL
