"""Revisa evidencia local o la preparada para el próximo commit; nunca modifica Git."""
import argparse
import json
from pathlib import Path
import subprocess

RAIZ = Path(__file__).resolve().parents[1]
RUTAS = ["F1/notebooks/F1_Definicion.ipynb", "F2/notebooks/F2_Preprocesamiento.ipynb"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true", help="Lee Git index para detectar salidas borradas por un filtro.")
    args = parser.parse_args()
    fallos = []
    for ruta in RUTAS:
        if args.staged:
            resultado = subprocess.run(["git", "show", f":{ruta}"], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8")
            if resultado.returncode:
                fallos.append(f"{ruta}: no existe en el índice de Git")
                continue
            texto = resultado.stdout
        else:
            texto = (RAIZ / ruta).read_text(encoding="utf-8")
        nb = json.loads(texto)
        celdas = [c for c in nb["cells"] if c["cell_type"] == "code" and "".join(c["source"]).strip()]
        if not celdas or any(c.get("execution_count") is None for c in celdas):
            fallos.append(f"{ruta}: faltan contadores de ejecución")
        if not any(c.get("outputs") for c in celdas):
            fallos.append(f"{ruta}: no conserva salidas")
        if any(o.get("output_type") == "error" for c in celdas for o in c.get("outputs", [])):
            fallos.append(f"{ruta}: contiene errores")
        print(f"{ruta}: {len(celdas)} celdas de código revisadas.")
    if fallos:
        raise SystemExit("\n".join(fallos))
    print("Evidencia de ejecución presente. Esta revisión no certifica la nota ni la revisión del equipo.")


if __name__ == "__main__":
    main()
