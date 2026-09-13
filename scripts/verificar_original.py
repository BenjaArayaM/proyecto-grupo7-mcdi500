"""Comprueba el CSV local sin generar datos procesados ni modificar el original."""
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from F1.src.entorno import cargar_configuracion, verificar_original

if __name__ == "__main__":
    manifiesto = verificar_original(RAIZ, cargar_configuracion(RAIZ))
    print("Archivo:", manifiesto["ruta_relativa"])
    print("Bytes:", manifiesto["bytes"])
    print("SHA-256:", manifiesto["sha256"])
    print("Integridad correcta. No se modificó ni se subió el archivo.")
