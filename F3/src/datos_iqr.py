"""Lectura del producto de F2; F3 nunca repite su limpieza ni exporta sobre F2."""
import hashlib
from pathlib import Path
import pandas as pd
from F3.src.funciones_iqr import validar_serie


def encontrar_raiz(inicio=None) -> Path:
    """Ubica proyecto.json desde la raíz o un subdirectorio del repositorio."""
    ruta = Path(inicio or Path.cwd()).resolve()
    if ruta.is_file():
        ruta = ruta.parent
    for candidato in [ruta, *ruta.parents]:
        if (candidato / "proyecto.json").is_file():
            return candidato
    raise FileNotFoundError("Abra el notebook dentro del proyecto MCDI500.")


def cargar_ordenes(raiz: Path) -> tuple[pd.DataFrame, dict]:
    """Valida el contrato de intercambio: una OC por fila y monto finito.

La marca de F2 se lee para comprobar exactamente qué órdenes son extremas.
Los montos procesados usan punto decimal; no se reaplica convertir_decimal.
"""
    ruta = Path(raiz) / "F2/data/processed/ordenes.csv"
    if not ruta.is_file():
        raise FileNotFoundError("Falta ordenes.csv. Ejecute python scripts/ejecutar_pipeline.py desde la raíz.")
    columnas = ["codigoOC", "MontoNetoOC_CLP", "extremo_iqr_neto_clp"]
    datos = pd.read_csv(ruta, usecols=columnas, dtype={"codigoOC": "string"})
    if datos.empty or datos["codigoOC"].isna().any() or datos["codigoOC"].str.strip().eq("").any():
        raise ValueError("Se requieren órdenes y códigos no vacíos.")
    if not datos["codigoOC"].is_unique:
        raise ValueError("codigoOC repetido: F3 requiere una fila por orden de F2.")
    datos["MontoNetoOC_CLP"] = pd.to_numeric(datos["MontoNetoOC_CLP"], errors="raise").astype(float)
    validar_serie(datos["MontoNetoOC_CLP"])
    marcas = datos["extremo_iqr_neto_clp"].astype("string").str.lower()
    if marcas.isna().any() or not marcas.isin(["true", "false"]).all():
        raise ValueError("La marca IQR de F2 debe contener solo True/False.")
    datos["extremo_iqr_neto_clp"] = marcas.eq("true").astype(bool)
    return datos, {"ruta": "F2/data/processed/ordenes.csv", "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
                   "filas": len(datos), "validos": len(datos), "faltantes": 0,
                   "eliminados": 0, "imputados": 0, "unidad": "orden de compra"}
