# Clústeres espaciales de homicidios en Ecuador

**Análisis LISA (Índice de Moran Local) · urbano vs rural · nivel cantonal**

Mapa web interactivo de doble panel (Kepler.gl) que muestra dónde se concentran de forma
estadísticamente significativa los homicidios en Ecuador, separando el contexto **urbano**
(panel izquierdo) del **rural** (panel derecho).

## Cómo abrir el mapa

`index.html` es un archivo único y autocontenido (los datos van incrustados). Elija una opción:

| Opción | Pasos |
| --- | --- |
| **Doble clic** | Descargue el repositorio (*Code → Download ZIP*), descomprima y abra `index.html` en Chrome, Edge o Firefox. |
| **Servidor local** | `python3 -m http.server 8000` en la carpeta del proyecto y abra <http://localhost:8000>. |
| **GitHub Pages** | *Settings → Pages → Deploy from a branch → `main` / root*; el mapa queda en `https://faustoaguanor.github.io/Mapa_Homiciodios_EC_Kepler_GL/`. |

**Requisitos:** navegador moderno con WebGL e **internet** (las librerías —React, Kepler.gl,
MapLibre— y el mapa base se cargan desde CDN). El archivo pesa ~7 MB; la primera carga puede tardar unos segundos.

### Uso

- Pase el cursor sobre un cantón: muestra nombre, provincia, nº de homicidios, categoría,
  tipo de clúster LISA, **I de Moran** local y **valor p**.
- El botón **Metodología y uso** (borde izquierdo) abre/cierra el panel explicativo.
- La leyenda de colores está en el botón de leyenda de la columna derecha de cada panel.

## Metodología

El **Índice de Moran Local (LISA, Anselin 1995)** compara el número de homicidios de cada cantón
con el de sus vecinos. Un clúster se declara cuando el resultado es significativo con **p < 0.05**
(el análisis se hace por separado para homicidios urbanos y rurales).

| Categoría | Color | Significado |
| --- | --- | --- |
| **HH — Hotspot** | rojo | Cantón con valor alto rodeado de vecinos altos |
| **LL — Coldspot** | azul | Cantón con valor bajo rodeado de vecinos bajos |
| **HL — Outlier alto** | naranja | Valor alto rodeado de vecinos bajos |
| **LH — Outlier bajo** | celeste | Valor bajo rodeado de vecinos altos |
| No significativo | gris | Sin evidencia de clúster (p ≥ 0.05) |

Resultados incluidos (224 unidades):

| Zona | HH | LL | HL | LH | No signif. |
| --- | ---: | ---: | ---: | ---: | ---: |
| Urbana | 6 | 26 | 1 | 14 | 177 |
| Rural | 26 | 36 | 1 | 7 | 154 |

Atributos de cada capa `hotspots_*_moran.geojson`: `lisa_cluster` (categoría), `lisa_i` (I local),
`lisa_p` (pseudo-valor p) y `categoria` (Bajo/Medio/… según el conteo de homicidios).

> **Pendiente de documentar por el autor:** matriz de pesos espaciales (p. ej. Queen/KNN),
> nº de permutaciones, software usado (p. ej. GeoDa / PySAL `esda`) y si se aplicó corrección
> por comparaciones múltiples. El valor mínimo observado (`p = 0.001`) es consistente con 999 permutaciones.

## Datos

Todos los datos están en [`data/`](data/):

| Archivo | Contenido | Registros |
| --- | --- | ---: |
| `homicidios_puntos.csv` | Muertes violentas georreferenciadas (tipo, provincia, cantón, área urbano/rural, fecha, coordenadas), 2014-01-01 a 2026-03-31 | 41 778 |
| `homicidios_urbanos_canton.geojson` | Homicidios urbanos por cantón | 224 |
| `homicidios_rurales_canton.geojson` | Homicidios rurales por cantón | 224 |
| `hotspots_urbanos_moran.geojson` | Resultado LISA, zona urbana | 224 |
| `hotspots_rurales_moran.geojson` | Resultado LISA, zona rural | 224 |
| `DPA_Cantonal.geojson` | Límites cantonales (División Político-Administrativa) | 224 |

- **Unidad de análisis:** 224 polígonos = 221 cantones + 3 zonas no delimitadas (códigos 9001, 9003, 9004). Clave de unión: `DPA_CANTON`.
- **Límites:** DPA cantonal del INEC (año 2011 en el atributo `DPA_ANIO`). Sistema de coordenadas: WGS 84 (EPSG:4326).
- **Origen de los homicidios:** registros oficiales de muertes violentas (la estructura —zona, distrito, circuito, subcircuito— corresponde a la organización territorial del Ministerio del Interior / Policía Nacional). *El autor debe indicar aquí la institución, el enlace y la fecha de descarga exactos.*
- **Privacidad:** el CSV publicado **no incluye** variables personales de las víctimas (edad, sexo, etnia, estado civil, profesión, discapacidad…); se eliminaron al preparar el repositorio.
- **Limitaciones:** subregistro y diferencias de calidad de georreferenciación entre cantones; el LISA es sensible a la definición de vecindad y a cantones con pocos casos (la tasa por habitantes no está calculada: se usan conteos).

## Estructura del repositorio

```
index.html            mapa final (generado, no editar a mano)
data/                 datos abiertos de entrada
src/                  plantilla HTML, estilos, JS y configuración de Kepler.gl
scripts/build.py      genera index.html desde src/ + data/
scripts/extract_legacy.py   (histórico) extrajo data/ del index.html monolítico anterior
```

### Regenerar el mapa

```bash
python3 scripts/build.py   # solo requiere Python 3, sin dependencias
```

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
