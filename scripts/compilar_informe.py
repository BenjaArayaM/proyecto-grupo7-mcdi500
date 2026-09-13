"""Genera insumos y compila LaTeX. Requiere pdflatex (MiKTeX o TeX Live)."""
from pathlib import Path
import shutil
import subprocess
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
from F2.src.preprocesamiento import ejecutar_pipeline
from F2.src.informe import generar_insumos_informe

if __name__ == "__main__":
    compilador = shutil.which("pdflatex")
    if compilador is None:
        raise SystemExit("No se encontró pdflatex. Instale MiKTeX, reabra Git Bash y active .venv. LaTeX se instala fuera del entorno Python.")
    generar_insumos_informe(ejecutar_pipeline(RAIZ), RAIZ)
    for pasada in range(1, 4):
        resultado = subprocess.run([compilador, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "informe.tex"], cwd=RAIZ / "informe", capture_output=True, text=True, errors="replace")
        if resultado.returncode:
            print(resultado.stdout[-6000:])
            raise SystemExit("LaTeX no compiló. Revise informe/informe.log.")
        print(f"LaTeX: pasada {pasada}/3 correcta.")
    print("PDF actualizado: informe/informe.pdf (borrador técnico hasta cerrar los pendientes).")
