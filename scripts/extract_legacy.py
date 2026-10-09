"""Extrae los datos incrustados en la versión monolítica antigua de index.html
y los guarda como archivos abiertos en data/ (ejecutado una sola vez).

Uso: python3 scripts/extract_legacy.py ruta/al/index_antiguo.html
"""
import csv, json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
# Columnas del CSV de puntos que se conservan. Se descartan las variables
# personales de las víctimas (edad, sexo, etnia, estado civil, profesión, etc.).
KEEP = ["tipo_muerte", "provincia", "canton", "codigo_canton", "area_hecho",
        "fecha_infraccion", "latitude", "longitude"]


def main(path):
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    ds = json.loads(next(l for l in lines if l.strip().startswith("const datasets =")).strip()[len("const datasets = "):].rstrip(";"))
    DATA.mkdir(exist_ok=True)
    for d in ds:
        dd = d["data"]
        rows = dd.get("rows") or dd["allData"]
        label = dd["label"]
        if label.endswith(".geojson"):
            feats = [r[0] for r in rows]
            (DATA / label).write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        else:
            names = [f["name"] for f in dd["fields"]]
            idx = [names.index(k) for k in KEEP]
            with open(DATA / "homicidios_puntos.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(KEEP)
                for r in rows:
                    w.writerow([r[i] for i in idx])
        print("ok", label, len(rows))
    cfg = next(l for l in lines if l.strip().startswith("const config =")).strip()[len("const config = "):].rstrip(";")
    Path(__file__).resolve().parent.parent.joinpath("src", "kepler_config.json").write_text(json.dumps(json.loads(cfg), ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
