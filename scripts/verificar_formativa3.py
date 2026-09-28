"""Comprueba archivos/evidencias de F3; no realiza ninguna operación Git."""
from pathlib import Path
import hashlib
import json
import nbformat

RAIZ = Path(__file__).resolve().parents[1]


def verificar():
    resumen = json.loads((RAIZ/'F3/docs/resultados_iqr.json').read_text(encoding='utf-8'))
    evidencia = json.loads((RAIZ/'F3/evidencias/ejecucion_formativa3.json').read_text(encoding='utf-8'))
    ruta = RAIZ/'F3/notebooks/F3_Formativa_Eficiencia_IQR.ipynb'
    nb = nbformat.read(ruta, as_version=4)
    nbformat.validate(nb)
    codigo = [c for c in nb.cells if c.cell_type == 'code' and c.source.strip()]
    assert [c.execution_count for c in codigo] == list(range(1, len(codigo)+1)), 'Ejecución incompleta.'
    assert not any(o.output_type == 'error' for c in codigo for o in c.outputs), 'Salidas de error.'
    assert hashlib.sha256(ruta.read_bytes().replace(b'\r\n',b'\n')).hexdigest() == evidencia['sha256_notebook'], 'El notebook cambió después de su ejecución registrada.'
    for rel, huella in resumen['sha256_fuentes'].items():
        assert hashlib.sha256((RAIZ/rel).read_bytes().replace(b'\r\n',b'\n')).hexdigest() == huella, f'Código cambiado: {rel}'
    assert resumen['sha256_fuentes'] == evidencia['sha256_fuentes'], 'Evidencias de ejecuciones diferentes.'
    assert resumen['contexto'] == evidencia['contexto'], 'Contextos distintos.'
    assert hashlib.sha256((RAIZ/resumen['entrada']['ruta']).read_bytes()).hexdigest() == resumen['entrada']['sha256'], 'Cambió ordenes.csv.'
    assert resumen['pruebas']['exitosas'] and resumen['pruebas']['pruebas'] >= 24
    assert resumen['pruebas']['omitidas'] == 0 and resumen['equivalencia_listas_y_marcas_f2']
    assert len({r['n'] for r in resumen['benchmark']}) >= 7, 'Faltan tamaños medidos.'
    for rel in ['F2/notebooks/F2_Preprocesamiento.ipynb','evidencias/entorno_F2.json']:
        json.loads((RAIZ/rel).read_text(encoding='utf-8'))
    return resumen


if __name__ == '__main__':
    r = verificar()
    print(f"F3 verificada: {r['entrada']['filas']} OC, {r['atipicos']} extremos, {r['pruebas']['pruebas']} pruebas.")
    print('Código, datos y notebook corresponden a las evidencias guardadas.')
    print('Esta revisión no acredita revisión humana, publicación en GitHub ni calificación.')
