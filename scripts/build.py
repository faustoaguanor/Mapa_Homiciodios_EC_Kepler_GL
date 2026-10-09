#!/usr/bin/env python3
"""Genera index.html (autocontenido) a partir de src/ y data/.

    python3 scripts/build.py

Entradas : data/*.geojson, data/homicidios_puntos.csv, src/kepler_config.json,
           src/index.template.html, src/styles.css, src/app.js
Salida   : index.html

Optimizaciones: se redondean coordenadas y se incrustan solo las capas que el
mapa muestra. El CSV de puntos (data/homicidios_puntos.csv) no se incrusta.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA, SRC = ROOT / "data", ROOT / "src"
COORD_DECIMALS = 5  # ~1 m; suficiente para polígonos cantonales y puntos

# id interno de Kepler.gl -> (archivo, etiqueta)
DATASETS = [
    ("-8hs4t8", "homicidios_urbanos_canton.geojson", "homicidios_urbanos_canton.geojson"),
    ("h6tp0y", "homicidios_rurales_canton.geojson", "homicidios_rurales_canton.geojson"),
    ("zgayf8", "hotspots_urbanos_moran.geojson", "hotspots_urbanos_moran.geojson"),
    ("xzn54m", "hotspots_rurales_moran.geojson", "hotspots_rurales_moran.geojson"),
    ("-59fsyl", "DPA_Cantonal.geojson", "DPA_Cantonal.geojson"),
]

LISA_TOOLTIP = [{"name": n, "format": None} for n in ("lisa_cluster", "lisa_p", "lisa_i")]
# Capas (ids de Kepler.gl) visibles en cada panel de la vista dividida
LAYER_URBAN_LISA, LAYER_RURAL_LISA, LAYER_BOUNDARIES = "qlxdln", "980e40a", "a5la1pg"
LAYER_HEATMAP = "v2hpzqg"
POINTS_ID = "-7t46wt"


def round_coords(c):
    if isinstance(c[0], (int, float)):
        return [round(v, COORD_DECIMALS) for v in c]
    return [round_coords(x) for x in c]


def load_geojson(name):
    gj = json.loads((DATA / name).read_text(encoding="utf-8"))
    for f in gj["features"]:
        f["geometry"]["coordinates"] = round_coords(f["geometry"]["coordinates"])
        p = f["properties"]
        if "lisa_i" in p:
            p["lisa_i"] = round(p["lisa_i"], 4)
    return gj


def build_config():
    cfg = json.loads((SRC / "kepler_config.json").read_text(encoding="utf-8"))
    fields = cfg["config"]["visState"]["interactionConfig"]["tooltip"]["fieldsToShow"]
    for key in ("zgayf8", "xzn54m"):
        names = {f["name"] for f in fields[key]}
        fields[key] += [f for f in LISA_TOOLTIP if f["name"] not in names]
    fields.pop(POINTS_ID, None)

    # El mapa de calor (y su filtro temporal) cubría ambos paneles y ocultaba los
    # clústeres LISA: se retira de la página. Los puntos siguen en data/.
    vis = cfg["config"]["visState"]
    vis["layers"] = [l for l in vis["layers"] if l["id"] != LAYER_HEATMAP]
    vis["filters"] = []
    others = [l["id"] for l in vis["layers"]]

    def panel(lisa_id):
        return {"layers": {i: i in (lisa_id, LAYER_BOUNDARIES) for i in others}}

    # Panel izquierdo = urbano, panel derecho = rural
    vis["splitMaps"] = [panel(LAYER_URBAN_LISA), panel(LAYER_RURAL_LISA)]
    return cfg


def main():
    data = []
    for id_, fname, label in DATASETS:
        data.append({"id": id_, "label": label, "format": "geojson", "content": load_geojson(fname)})
    dump = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    data_js = "    window.MAPA_DATA = %s;\n    window.MAPA_CONFIG = %s;" % (dump(data), dump(build_config()))
    html = (SRC / "index.template.html").read_text(encoding="utf-8")
    html = (html.replace("%%CSS%%", (SRC / "styles.css").read_text(encoding="utf-8"))
                .replace("%%APP%%", (SRC / "app.js").read_text(encoding="utf-8"))
                .replace("%%DATA%%", data_js))
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print("index.html: %.1f MB" % ((ROOT / "index.html").stat().st_size / 1e6))


if __name__ == "__main__":
    main()
