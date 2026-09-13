"""Alternativa de validación sin red: un ipykernel real en memoria, en proceso nuevo.

No sustituye la revisión en JupyterLab del equipo. El script principal declara
este motor en la evidencia. Las salidas y los contadores los genera el kernel.
"""
import os
from pathlib import Path
import sys
import nbformat
from ipykernel.inprocess.manager import InProcessKernelManager

RAIZ = Path(__file__).resolve().parents[1]


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Indique la ruta relativa de un notebook.")
    ruta = (RAIZ / sys.argv[1]).resolve()
    if RAIZ not in ruta.parents or ruta.suffix != ".ipynb":
        raise SystemExit("Se requiere un notebook del proyecto.")
    nb = nbformat.read(ruta, as_version=4)
    os.chdir(ruta.parent)
    km = InProcessKernelManager()
    km.start_kernel()
    kc = km.client()
    kc.start_channels()
    try:
        for celda in nb.cells:
            if celda.cell_type != "code" or not celda.source.strip():
                continue
            msg_id = kc.execute(celda.source, store_history=True, allow_stdin=False, stop_on_error=True)
            respuesta = kc.get_shell_msg(timeout=300)
            celda.execution_count = respuesta["content"]["execution_count"]
            celda.outputs = []
            km.kernel.stdout.flush()
            km.kernel.stderr.flush()
            while kc.iopub_channel.msg_ready():
                mensaje = kc.get_iopub_msg(timeout=300)
                # InProcessKernel emite streams sin parent_header. La ejecución
                # es síncrona y se drena la cola antes de iniciar otra celda.
                if mensaje.get("parent_header", {}).get("msg_id") not in (None, msg_id):
                    continue
                if mensaje["msg_type"] in {"stream", "display_data", "execute_result", "error"}:
                    celda.outputs.append(nbformat.v4.output_from_msg(mensaje))
            if respuesta["content"]["status"] != "ok":
                nbformat.write(nb, ruta)
                raise RuntimeError(f"Celda {celda.execution_count}: {respuesta['content'].get('evalue')}")
        nb.metadata.language_info = km.kernel.language_info
        nb.metadata["validacion"] = {"motor": "ipykernel_inprocess", "proceso_nuevo_por_notebook": True}
        nbformat.validate(nb)
        nbformat.write(nb, ruta)
    finally:
        kc.stop_channels()
        km.shutdown_kernel()


if __name__ == "__main__":
    main()
