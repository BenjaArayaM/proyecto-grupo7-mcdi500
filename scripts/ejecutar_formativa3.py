"""Ejecuta la revisión F3 en un proceso Python nuevo y guarda su procedencia.

No ejecuta órdenes Git. No crea ramas, commits ni conexiones con GitHub.
El motor memoria usa un ipykernel real sin TCP y se identifica en la evidencia.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone
import nbformat

RAIZ = Path(__file__).resolve().parents[1]
RUTA = RAIZ / 'F3/notebooks/F3_Formativa_Eficiencia_IQR.ipynb'


def ejecutar_memoria(nb):
    from ipykernel.inprocess.manager import InProcessKernelManager
    km = InProcessKernelManager()
    km.start_kernel()
    cliente = km.client()
    cliente.start_channels()
    try:
        for celda in nb.cells:
            if celda.cell_type != 'code' or not celda.source.strip():
                continue
            celda.metadata.pop('execution', None)
            identificador = cliente.execute(celda.source, store_history=True, allow_stdin=False)
            respuesta = cliente.get_shell_msg(timeout=600)
            celda.execution_count = respuesta['content']['execution_count']
            celda.outputs = []
            km.kernel.stdout.flush()
            km.kernel.stderr.flush()
            while cliente.iopub_channel.msg_ready():
                mensaje = cliente.get_iopub_msg(timeout=600)
                if mensaje.get('parent_header', {}).get('msg_id') not in (None, identificador):
                    continue
                if mensaje['msg_type'] in {'stream', 'display_data', 'execute_result', 'error'}:
                    celda.outputs.append(nbformat.v4.output_from_msg(mensaje))
            if respuesta['content']['status'] != 'ok':
                raise RuntimeError(f"Celda {celda.execution_count}: {respuesta['content'].get('evalue')}")
        nb.metadata.language_info = km.kernel.language_info
    finally:
        cliente.stop_channels()
        km.shutdown_kernel()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kernel', default='grupo7_mcdi500')
    parser.add_argument('--motor', choices=['jupyter', 'memoria'], default='jupyter')
    parser.add_argument('--contexto', default='revision_local_del_equipo')
    args = parser.parse_args()
    os.environ['GRUPO7_CONTEXTO'] = args.contexto
    os.environ['MPLBACKEND'] = 'module://matplotlib_inline.backend_inline'
    inicio = datetime.now(timezone.utc).isoformat()
    nb = nbformat.read(RUTA, as_version=4)
    for celda in nb.cells:
        if celda.cell_type == 'code':
            celda.outputs = []
            celda.execution_count = None
            celda.metadata.pop('execution', None)
    # La invocación de este script es un proceso nuevo; nunca comparte el kernel
    # de una pestaña del navegador ni sus variables.
    if args.motor == 'memoria':
        os.chdir(RUTA.parent)
        ejecutar_memoria(nb)
    else:
        from nbclient import NotebookClient
        NotebookClient(nb, timeout=600, kernel_name=args.kernel,
                       resources={'metadata': {'path': str(RUTA.parent)}}).execute()
    codigo = [c for c in nb.cells if c.cell_type == 'code' and c.source.strip()]
    if [c.execution_count for c in codigo] != list(range(1, len(codigo)+1)):
        raise RuntimeError('La numeración de ejecución no es continua.')
    if any(o.output_type == 'error' for c in codigo for o in c.outputs):
        raise RuntimeError('Hay salidas de error.')
    nb.metadata['validacion'] = {'motor': args.motor, 'contexto': args.contexto,
                                 'proceso_nuevo': True}
    nbformat.validate(nb)
    temporal = RUTA.with_suffix('.tmp')
    nbformat.write(nb, temporal)
    temporal.replace(RUTA)
    resumen = json.loads((RAIZ/'F3/docs/resultados_iqr.json').read_text(encoding='utf-8'))
    evidencia = {'contexto': args.contexto, 'motor': args.motor, 'inicio_utc': inicio,
                 'fin_utc': datetime.now(timezone.utc).isoformat(),
                 'sistema_ejecutor': platform.system(), 'python_ejecutor': platform.python_version(),
                 'kernel': args.kernel if args.motor == 'jupyter' else 'ipykernel_inprocess',
                 'entorno_kernel': resumen['entorno'], 'celdas_codigo': len(codigo),
                 'errores': 0, 'proceso_nuevo': True,
                 'sha256_notebook': hashlib.sha256(RUTA.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                 'sha256_fuentes': resumen['sha256_fuentes']}
    destino = RAIZ/'F3/evidencias/ejecucion_formativa3.json'
    destino.write_text(json.dumps(evidencia, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"F3: {len(codigo)} celdas ejecutadas; {resumen['pruebas']['pruebas']} pruebas; sin errores.")
    print('Revise los resultados antes de compilar el informe o preparar un commit.')


if __name__ == '__main__':
    main()
