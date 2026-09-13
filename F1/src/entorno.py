"""Utilidades de F1: no imputan, limpian ni transforman observaciones."""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import sys
from pathlib import Path

import pandas as pd


def encontrar_raiz(inicio: Path | None = None) -> Path:
    """Encuentra proyecto.json desde la raíz o cualquier subcarpeta."""
    inicio = (inicio or Path.cwd()).resolve()
    for candidata in (inicio, *inicio.parents):
        if (candidata / "proyecto.json").is_file():
            return candidata
    raise FileNotFoundError("Abra Jupyter desde proyecto-grupo7-mcdi500: falta proyecto.json.")


def cargar_configuracion(raiz: Path) -> dict:
    return json.loads((raiz / "proyecto.json").read_text(encoding="utf-8"))


def sha256_archivo(ruta: Path) -> str:
    digest = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()


def verificar_original(raiz: Path, config: dict) -> dict:
    ruta = raiz / config["datos"]["original"]
    if not ruta.is_file():
        raise FileNotFoundError(
            f"Falta {config['datos']['original']}. Copie el CSV adjunto sin editarlo. "
            "Solo se cambia el nombre a 187402OCCompraAgil.csv."
        )
    sha = sha256_archivo(ruta)
    if sha != config["datos"]["sha256"]:
        raise ValueError("El SHA-256 no coincide. Revise el archivo; no cambie el hash para ocultar la diferencia.")
    return {"ruta_relativa": config["datos"]["original"], "bytes": ruta.stat().st_size, "sha256": sha}


def reconocer_archivo(raiz: Path, config: dict) -> pd.DataFrame:
    """Lee el esquema como texto; preserva identificadores y vacíos del origen."""
    verificar_original(raiz, config)
    return pd.read_csv(
        raiz / config["datos"]["original"], sep=config["datos"]["separador"],
        encoding=config["datos"]["encoding"], dtype="string",
        keep_default_na=False, na_values=[""],
    )


def registrar_entorno() -> dict:
    """Describe el intérprete que realmente ejecuta la celda, sin atribuirlo a un alumno."""
    paquetes = {}
    for nombre in ["numpy", "pandas", "matplotlib", "scikit-learn", "nbformat", "nbclient", "ipykernel", "jupyterlab"]:
        try:
            paquetes[nombre] = importlib.metadata.version(nombre)
        except importlib.metadata.PackageNotFoundError:
            paquetes[nombre] = "no instalado"
    return {
        "python": platform.python_version(), "sistema": platform.system(),
        "interprete": sys.executable, "entorno_virtual": sys.prefix != sys.base_prefix,
        "paquetes": paquetes,
    }
