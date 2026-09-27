"""Tiempo y memoria de los mismos algoritmos de la entrega formativa.

La creación de la entrada, su validación y los cuartiles quedan fuera de la
medición. Se incluye construir la lista de salida en AMBAS implementaciones.
No se modifican F2 ni las órdenes reales para simular tamaños crecientes.
"""
import gc
import time
import tracemalloc
from statistics import median
import numpy as np
import pandas as pd
from F3.src.funciones_iqr import (validar_serie, detectar_atipicos_bucle,
                                detectar_atipicos_vectorizado)


def replicar_serie(serie: pd.Series, n: int) -> pd.Series:
    """Repite cíclicamente y trunca: datos sintéticos de carga, no nuevas OC."""
    validar_serie(serie)
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError("n debe ser un entero positivo.")
    return pd.Series(np.resize(serie.to_numpy(dtype=float), n), name=serie.name)


def medir_pico_memoria(funcion, serie, inferior, superior, repeticiones=3):
    """Pico incremental rastreado, con la salida viva; NO es RAM total/RSS.

Se realizan llamadas separadas de las temporales. La entrada se creó antes
de iniciar tracemalloc. Las asignaciones nativas no rastreadas quedan fuera.
"""
    if tracemalloc.is_tracing():
        raise RuntimeError("Desactive tracemalloc externo antes del experimento.")
    picos = []
    for _ in range(repeticiones):
        gc.collect()
        tracemalloc.start()
        try:
            inicial, _ = tracemalloc.get_traced_memory()
            resultado = funcion(serie, inferior, superior)
            _, pico = tracemalloc.get_traced_memory()
            picos.append(max(0, pico - inicial))
            del resultado
        finally:
            tracemalloc.stop()
    return picos


def ejecutar_benchmark(serie, limites, tamanos=None, repeticiones=3, iteraciones=1000):
    """Series idénticas, calentamiento y orden alternado; mínimo por llamada.

Devuelve tabla agregada y todas las repeticiones. No contiene aserciones
sobre qué estrategia debe ganar: esa conclusión depende del entorno.
"""
    validar_serie(serie)
    if repeticiones < 3 or iteraciones < 1:
        raise ValueError("Use al menos tres repeticiones y una iteración.")
    inferior, superior = limites["limite_inferior"], limites["limite_superior"]
    if not np.isfinite([inferior, superior]).all() or inferior > superior:
        raise ValueError("Límites inválidos.")
    if tracemalloc.is_tracing():
        raise RuntimeError("La medición temporal debe hacerse sin tracemalloc activo.")
    tamanos = list(tamanos) if tamanos is not None else [len(serie), 1000, 2000, 5000, 10000, 20000, 50000]
    funciones = {"bucle": detectar_atipicos_bucle, "pandas": detectar_atipicos_vectorizado}
    filas, muestras = [], []
    for n in sorted(set(tamanos)):
        entrada = replicar_serie(serie, n)
        esperados = funciones["bucle"](entrada, inferior, superior)
        if esperados != funciones["pandas"](entrada, inferior, superior):
            raise AssertionError(f"Resultados distintos en n={n}.")
        for funcion in funciones.values():
            for _ in range(3):
                funcion(entrada, inferior, superior)
        tiempos = {nombre: [] for nombre in funciones}
        for repeticion in range(repeticiones):
            orden = list(funciones) if repeticion % 2 == 0 else list(reversed(funciones))
            for nombre in orden:
                funcion = funciones[nombre]
                inicio = time.perf_counter()
                for _ in range(iteraciones):
                    funcion(entrada, inferior, superior)
                transcurrido = time.perf_counter() - inicio
                tiempos[nombre].append(transcurrido)
                muestras.append({"n": int(n), "metodo": nombre, "repeticion": repeticion + 1,
                                 "iteraciones": iteraciones, "tiempo_total_s": transcurrido})
        for nombre, funcion in funciones.items():
            picos = medir_pico_memoria(funcion, entrada, inferior, superior, repeticiones)
            for repeticion, pico in enumerate(picos, 1):
                muestras.append({"n": int(n), "metodo": nombre, "repeticion": repeticion,
                                 "pico_rastreado_bytes": pico})
            filas.append({"n": int(n), "metodo": nombre, "atipicos": len(esperados),
                          "entrada_replicada": n != len(serie), "iteraciones": iteraciones,
                          "repeticiones": repeticiones, "min_total_s": min(tiempos[nombre]),
                          "min_por_llamada_us": min(tiempos[nombre]) / iteraciones * 1e6,
                          "mediana_por_llamada_us": median(tiempos[nombre]) / iteraciones * 1e6,
                          "max_por_llamada_us": max(tiempos[nombre]) / iteraciones * 1e6,
                          "mediana_pico_bytes": median(picos),
                          "entrada_bytes": int(entrada.memory_usage(index=True, deep=True))})
    return pd.DataFrame(filas), muestras


def resumir_cruces(tabla):
    """Intervalos muestreados donde pandas pasa a ganar; no umbral universal."""
    ancho = tabla.pivot(index="n", columns="metodo", values="min_por_llamada_us").sort_index()
    prev, cruces = None, []
    for n, fila in ancho.iterrows():
        gana = bool(fila["pandas"] < fila["bucle"])
        if prev is not None and not prev[1] and gana:
            cruces.append({"ultimo_n_bucle_no_mas_lento": int(prev[0]), "primer_n_pandas_mas_rapido": int(n)})
        prev = (n, gana)
    return {"intervalos_observados": cruces,
            "nota": "Se comparan mínimos de tres mediciones. No se estima un punto exacto ni se garantiza monotonicidad.",
            "pandas_gana_en_todos": bool((ancho["pandas"] < ancho["bucle"]).all()),
            "pandas_no_gana_en_ninguno": bool((ancho["pandas"] >= ancho["bucle"]).all())}
