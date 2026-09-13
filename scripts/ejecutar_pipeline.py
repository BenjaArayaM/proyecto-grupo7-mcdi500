"""Ejecutar desde la raíz: python scripts/ejecutar_pipeline.py"""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from F2.src.preprocesamiento import ejecutar_pipeline, exportar_resultados

if __name__ == "__main__":
    resultado = ejecutar_pipeline(RAIZ)
    exportar_resultados(resultado, RAIZ)
    print(f"Original: {resultado['metricas']['filas_original']} filas; salida: {len(resultado['ordenes'])} órdenes.")
    print(f"Excepciones de detalle para revisión: {len(resultado['excepciones_detalle'])}.")
    print("Tablas generadas en F2/data/processed y diagnóstico en F2/docs.")
