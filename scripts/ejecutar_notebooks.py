"""Ejecuta cada notebook con un kernel nuevo y conserva todas sus salidas."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOKS = {"F1": "F1/notebooks/F1_Definicion.ipynb", "F2": "F2/notebooks/F2_Preprocesamiento.ipynb"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fase", choices=["F1", "F2", "ambas"], default="ambas")
    parser.add_argument("--kernel", default="grupo7_mcdi500")
    parser.add_argument("--motor", choices=["jupyter", "memoria"], default="jupyter",
                        help="Jupyter normal; memoria usa ipykernel en un proceso nuevo sin conexiones de red.")
    parser.add_argument("--etiqueta", default="revision_local", help="Contexto real; no sustituye el autor del commit.")
    args = parser.parse_args()
    fases = list(NOTEBOOKS) if args.fase == "ambas" else [args.fase]
    for fase in fases:
        relativa = NOTEBOOKS[fase]
        ruta = RAIZ / relativa
        nb = nbformat.read(ruta, as_version=4)
        huella_codigo = hashlib.sha256("\n".join(c.source for c in nb.cells).encode("utf-8")).hexdigest()
        inicio = datetime.now(timezone.utc).isoformat()
        opciones = {"timeout": 300, "kernel_name": args.kernel, "resources": {"metadata": {"path": str(ruta.parent)}}}
        if args.motor == "memoria":
            subprocess.run([sys.executable, str(RAIZ / "scripts/ejecutar_notebook_memoria.py"), relativa], cwd=RAIZ, check=True)
            nb = nbformat.read(ruta, as_version=4)
        else:
            NotebookClient(nb, **opciones).execute()
        nb.metadata["validacion"] = {
            "motor": args.motor, "proceso_nuevo_por_notebook": True, "contexto": args.etiqueta
        }
        nbformat.validate(nb)
        nbformat.write(nb, ruta)
        codigo = [c for c in nb.cells if c.cell_type == "code" and c.source.strip()]
        if any(c.execution_count is None or any(o.output_type == "error" for o in c.outputs) for c in codigo):
            raise RuntimeError(f"{fase}: ejecución incompleta o con errores.")
        revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=RAIZ, capture_output=True, text=True)
        evidencia = {
            "notebook": relativa, "contexto": args.etiqueta, "inicio_utc": inicio,
            "fin_utc": datetime.now(timezone.utc).isoformat(), "kernel": args.kernel,
            "motor": args.motor,
            "plataforma_ejecutor": platform.system(), "celdas_codigo_ejecutadas": len(codigo),
            "errores": 0, "salidas_conservadas": True, "sha256_fuente_notebook": huella_codigo,
            "revision_git_al_ejecutar": revision.stdout.strip() if revision.returncode == 0 else None,
        }
        destino = RAIZ / "evidencias" / f"ejecucion_{fase}.json"
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{fase}: {len(codigo)} celdas de código ejecutadas, sin errores; salidas guardadas.")


if __name__ == "__main__":
    main()
