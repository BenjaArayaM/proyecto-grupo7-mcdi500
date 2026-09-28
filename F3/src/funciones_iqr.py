"""Estadísticos compartidos y dos estrategias equivalentes de detección IQR.

Las dos estrategias conservan la API entregada: Series + dos límites -> lista.
Precondición: serie numérica finita, validada una sola vez antes de medir. La
validación y los cuartiles no forman parte del intervalo cronometrado. Los
resultados conservan orden y multiplicidad, pero no el índice (contrato original).
"""
from math import isfinite
import numpy as np
import pandas as pd


def validar_serie(serie: pd.Series, permitir_vacia: bool = False) -> None:
    """Rechaza entradas ambiguas sin imputar ni eliminar observaciones."""
    if not isinstance(serie, pd.Series):
        raise TypeError("Se requiere una pandas.Series.")
    if not pd.api.types.is_numeric_dtype(serie.dtype):
        raise TypeError("La serie debe tener tipo numérico.")
    if serie.empty and not permitir_vacia:
        raise ValueError("No se pueden calcular cuartiles de una serie vacía.")
    if serie.isna().any() or not np.isfinite(serie.to_numpy(dtype=float)).all():
        raise ValueError("La serie contiene faltantes o números no finitos.")


def calcular_limites_iqr(serie: pd.Series, factor: float = 1.5) -> dict:
    """Calcula una vez Q1, Q3 e IQR con interpolación lineal, como en F2.

Una serie constante es válida: IQR=0. Una vacía no permite estimar cuartiles.
Devuelve números serializables; no modifica la serie ni elimina extremos.
"""
    validar_serie(serie)
    if not isfinite(factor) or factor <= 0:
        raise ValueError("El factor debe ser finito y positivo.")
    q1, q3 = serie.quantile([0.25, 0.75], interpolation="linear")
    iqr = float(q3 - q1)
    return {"n": len(serie), "q1": float(q1), "q3": float(q3), "iqr": iqr,
            "limite_inferior": float(q1 - factor * iqr),
            "limite_superior": float(q3 + factor * iqr),
            "factor": float(factor), "interpolacion": "linear"}


def detectar_atipicos_bucle(serie, limite_inferior, limite_superior):
    """Filtra valores con < y > estrictos; entrada validada, vacía -> [].

Se conserva el cuerpo del algoritmo evaluado por el profesor para que la
ampliación experimental compare las mismas dos implementaciones.
"""
    atipicos = []
    for valor in serie:
        if valor < limite_inferior or valor > limite_superior:
            atipicos.append(valor)
    return atipicos


def detectar_atipicos_vectorizado(serie, limite_inferior, limite_superior):
    """Máscara pandas y salida lista, con el mismo contrato del bucle."""
    mascara = (serie < limite_inferior) | (serie > limite_superior)
    return serie[mascara].tolist()
