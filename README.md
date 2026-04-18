# Clústeres Espaciales de Homicidios en Ecuador

### Análisis LISA — Índice de Moran Local · Urbano vs Rural

Mapa interactivo de doble panel que visualiza los clústeres espaciales estadísticamente significativos de homicidios en Ecuador, diferenciando entre contexto urbano y rural a nivel cantonal.

---

## Visualización

El mapa usa una vista dividida:

| Panel izquierdo                | Panel derecho                  |
| ------------------------------ | ------------------------------ |
| Clústeres Urbanos de Homicidio | Clústeres Rurales de Homicidio |

**Abre el mapa:** [`Homicidios_Urbano_Rurales.html`](Homicidios_Urbano_Rurales.html)

---

## Metodología

La clasificación espacial se obtiene mediante el **Índice de Moran Local (LISA)** con umbral de significancia **p < 0.05**, lo que garantiza que los patrones detectados tienen menos del 5% de probabilidad de ser aleatorios.

| Categoría         | Color   | Descripción                                                 |
| ----------------- | ------- | ----------------------------------------------------------- |
| HH — Hotspot      | Rojo    | Cantón con alta violencia rodeado de cantones también altos |
| LL — Coldspot     | Azul    | Cantón con baja violencia rodeado de cantones también bajos |
| HL — Outlier alto | Naranja | Cantón con alta violencia pero vecinos bajos                |
| LH — Outlier bajo | Celeste | Cantón con baja violencia pero vecinos altos                |
| No significativo  | Gris    | Sin evidencia estadística de clúster                       ecinos altos |
| No significativo | Gris | Sin evidencia estadística de clúster |

---

## Datos

- **Homicidios:** Registros oficiales desagregados por zona urbana/rural a nivel cantonal — Ecuador.
- **Límites geográficos:** División Político-Administrativa Cantonal (DPA) — INEC Ecuador.
- **Unidad de análisis:** 221 cantones del Ecuador continental e insular.

---

## Tecnologías

- [Kepler.gl](https://kepler.gl) — visualización geoespacial (MIT License)
- [MapLibre GL JS](https://maplibre.org) — renderizado de mapas
- React · Redux

---

## Licencia

Este trabajo se distribuye bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Puedes compartir y adaptar el contenido siempre que des crédito apropiado al autor original.  
Ver [`LICENSE`](LICENSE) para el texto completo.

---

## Autor

FAGR
