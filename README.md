# Clústeres espaciales de homicidios en Ecuador

**Visualización con [Kepler.gl](https://kepler.gl) · LISA urbano vs rural · nivel cantonal**

Mapa web de doble panel construido con **Kepler.gl** (deck.gl + MapLibre) que muestra los clústeres
LISA de homicidios por cantón: **urbano** a la izquierda, **rural** a la derecha. Este repositorio
es, sobre todo, una **plantilla reproducible para publicar un mapa Kepler.gl autocontenido** en una sola página HTML.

## Cómo abrir el mapa

| Opción | Pasos |
| --- | --- |
| **Local** | Descargue el ZIP, descomprima y abra `index.html`; o `python3 -m http.server 8000` y vaya a <http://localhost:8000>. |
| **GitHub Pages** | *Settings → Pages → Deploy from a branch → `main` / root*. |

### Requisitos y solución de problemas

- Navegador moderno con **WebGL activado** e **internet** (librerías y mapa base vienen de CDN).
- Si ve **"An error in deck.gl"** o una pantalla de aviso: su navegador tiene WebGL/aceleración 3D desactivados.
  - **Firefox:** `about:config` → `webgl.disabled = false`, y *Ajustes → General → Rendimiento → Usar aceleración por hardware*.
  - **Chrome / Edge / Brave:** *Configuración → Sistema → Usar aceleración gráfica cuando esté disponible*.
  - Verifique en [get.webgl.org](https://get.webgl.org) y actualice los controladores de vídeo.
  - El mapa detecta esta situación y muestra estas instrucciones en pantalla.

## Cómo está construido el mapa con Kepler.gl

Kepler.gl se usa **sin servidor**, cargando su build UMD desde unpkg y montándolo con React + Redux:

1. **Store Redux** con el reducer `keplerGlReducer`, en modo **`readOnly`** (se oculta el panel de edición) y **vista dividida** (`mapState.isSplit: true`).
2. **Datos**: cada GeoJSON se convierte con `KeplerGl.processGeojson()` y se registra con un `id` fijo.
3. **Configuración**: `src/kepler_config.json` es la config exportada de Kepler.gl (capas, colores, tooltips, `splitMaps`); se aplica con `KeplerGlSchema.parseSavedConfig()` y `addDataToMap()`.
4. **Panel urbano vs rural**: en `splitMaps` cada panel activa una capa distinta (`qlxdln` urbano, `980e40a` rural) más los límites cantonales.
5. **Simbología**: capas `geojson` coloreadas por el campo `lisa_cluster` con escala **`customOrdinal`** (HH rojo, LL azul, HL naranja, LH celeste, no significativo gris).
6. **Extras**: botón de efectos inyectado con `injectComponents()` y panel lateral propio.

### Flujo para crear su propio mapa

1. Diseñe el mapa en [kepler.gl/demo](https://kepler.gl/demo) y exporte la configuración (*Share → Export Map / config JSON*).
2. Guarde la config en `src/kepler_config.json` y sus GeoJSON/CSV en `data/`.
3. Registre los datasets (id, archivo) en la lista `DATASETS` de `scripts/build.py`.
4. Ejecute `python3 scripts/build.py` → genera `index.html` autocontenido (~7 MB).

### Estructura

```
index.html                 mapa final (generado; no editar a mano)
src/index.template.html    plantilla HTML y panel lateral
src/app.js                 montaje de Kepler.gl, carga de datos y detección de WebGL
src/styles.css             estilos
src/kepler_config.json     configuración de Kepler.gl (capas, colores, tooltips)
data/                      datos de entrada (GeoJSON y CSV)
scripts/build.py           empaquetado (solo Python 3, sin dependencias)
```

### Consejos de rendimiento

- Redondee coordenadas (5 decimales ≈ 1 m): `build.py` lo hace y redujo el HTML de 27 MB a ~7 MB.
- Incruste solo las capas que se ven; los datos extra viven en `data/`.
- Fije versiones de las librerías en las URLs de CDN para que el mapa no se rompa con actualizaciones.

## Metodología (resumen)

El **Índice de Moran Local (LISA, Anselin 1995)** clasifica cada cantón según su valor y el de sus vecinos
(significancia p < 0.05, análisis separado para zona urbana y rural):

| Categoría | Color | Significado |
| --- | --- | --- |
| HH — Hotspot | rojo | Valor alto con vecinos altos |
| LL — Coldspot | azul | Valor bajo con vecinos bajos |
| HL — Outlier alto | naranja | Valor alto con vecinos bajos |
| LH — Outlier bajo | celeste | Valor bajo con vecinos altos |
| No significativo | gris | Sin evidencia de clúster |

Pase el cursor sobre un cantón para ver conteo, categoría, clúster, `lisa_i` (I local) y `lisa_p`.
*Pendiente del autor:* matriz de pesos, nº de permutaciones y software usado.

## Datos

Archivos en [`data/`](data/): `hotspots_urbanos_moran.geojson`, `hotspots_rurales_moran.geojson`,
`homicidios_urbanos_canton.geojson`, `homicidios_rurales_canton.geojson`, `DPA_Cantonal.geojson`
(224 unidades = 221 cantones + 3 zonas no delimitadas; clave `DPA_CANTON`, WGS 84) y
`homicidios_puntos.csv` (41 778 registros 2014 – mar. 2026, sin variables personales de las víctimas).
Límites: DPA del INEC. *Pendiente del autor:* institución, enlace y fecha de descarga de los registros de homicidios.

## Créditos y librerías de terceros

Este proyecto no sería posible sin software libre. Todas las librerías se cargan desde CDN (unpkg) y conservan su licencia original:

| Librería | Uso | Licencia |
| --- | --- | --- |
| [Kepler.gl](https://github.com/keplergl/kepler.gl) 3.3.0-alpha.0 (OpenJS Foundation / Uber) | Visualización geoespacial y vista dividida | MIT |
| [MapLibre GL JS](https://maplibre.org) 3.6 | Renderizado del mapa | BSD-3-Clause |
| [React](https://react.dev) / ReactDOM 18.3.1 | Interfaz | MIT |
| [Redux](https://redux.js.org) 4.2.1 / [React-Redux](https://react-redux.js.org) 8.1.2 | Estado de la aplicación | MIT |
| [styled-components](https://styled-components.com) 6.1.8 | Estilos de Kepler.gl | MIT |
| [CARTO Dark Matter](https://carto.com/basemaps) · datos © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors | Mapa base | CC BY 3.0 / ODbL |
| Fuente *Superfine* de Uber | Tipografía de la interfaz | Uso conforme a Kepler.gl |

Datos: límites cantonales © [INEC Ecuador](https://www.ecuadorencifras.gob.ec) (DPA). Metodología: Anselin, L. (1995), *Local Indicators of Spatial Association — LISA*, Geographical Analysis 27(2).

## Licencia

El contenido propio de este repositorio (mapa, análisis y datos procesados) se distribuye bajo [CC BY 4.0](LICENSE). Las librerías de terceros conservan sus propias licencias.

## Autoría

**faustoaguanor** — [github.com/faustoaguanor](https://github.com/faustoaguanor)

Cite como: faustoaguanor (2026). *Clústeres espaciales de homicidios en Ecuador (LISA urbano vs rural)*. GitHub. https://github.com/faustoaguanor/Mapa_Homiciodios_EC_Kepler_GL
