"""Tablas y figuras del informe generadas desde los resultados de F2."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def numero_es(valor, decimales=0):
    return f"{valor:,.{decimales}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def escapar_tex(texto):
    equivalencias = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(equivalencias.get(c, c) for c in str(texto))


def generar_insumos_informe(resultado: dict, raiz: Path) -> None:
    """Solo escribe archivos derivados; informe.tex contiene la deliberación editorial."""
    destino = raiz / "informe"
    (destino / "figuras").mkdir(parents=True, exist_ok=True)
    (destino / "tablas").mkdir(exist_ok=True)
    m = resultado["metricas"]
    macros = {
        "FilasOriginal": numero_es(m["filas_original"]), "ColumnasOriginal": m["columnas_original"],
        "Ordenes": m["ordenes"], "Proveedores": m["proveedores_rut"],
        "DuplicadosAdicionales": m["filas_identicas_adicionales"],
        "OrdenesMultirrubro": m["ordenes_con_mas_de_un_n1"],
        "OrdenesConciliadas": m["ordenes_conciliadas_firmas"],
        "ExcepcionesDetalle": len(m["ordenes_no_conciliadas"]),
        "NetoTotal": numero_es(m["neto_clp_total_todos_estados"], 2),
        "ExtremosNeto": m["extremos_neto_clp_todos_estados"],
        "UmbralNeto": numero_es(m["iqr_neto_clp"]["limite_superior"], 2),
        "ExtremosMapa": m["extremos_mapa_total_oc_solo_clp"],
        "UmbralMapa": numero_es(m["iqr_mapa_total_oc_solo_clp"]["limite_superior"], 2),
        "TamanoDesconocido": m["tamano_sin_clasificar"],
        "FechaMin": m["fecha_min"], "FechaMax": m["fecha_max"],
        "VarianzaNeto": numero_es(m["varianza_neto_clp_sin_imputacion_ddof0"], 2),
    }
    (destino / "tablas/metricas.tex").write_text("% Generado por F2; no editar a mano.\n" + "\n".join("\\newcommand{\\" + k + "}{" + str(v) + "}" for k, v in macros.items()) + "\n", encoding="utf-8")
    filas = []
    for campo, etiqueta in [("ActividadProveedor", "Actividad del proveedor"), ("RegionProveedor", "Región del proveedor"), ("ImpuestoEspecificoItem", "Impuesto específico del ítem")]:
        nf = m["nulos_por_fila"][campo]
        oc = m["nulos_por_oc"].get(campo)
        porcentaje = numero_es(nf / m["filas_original"] * 100, 2)
        por_oc = "No aplica: campo de ítem" if oc is None else f"{oc} / {m['ordenes']} ({numero_es(oc/m['ordenes']*100,2)}\\%)"
        filas.append(f"{etiqueta} & {numero_es(nf)} ({porcentaje}\\%) & {por_oc} " + r"\\")
    inicio_faltantes = r"""\begin{tabularx}{\textwidth}{@{}Yp{0.23\textwidth}p{0.31\textwidth}@{}}
\toprule
Campo & Filas ausentes & OC ausentes\\
\midrule
"""
    (destino / "tablas/faltantes.tex").write_text(inicio_faltantes + "\n".join(filas) + "\n" + r"\bottomrule" + "\n" + r"\end{tabularx}" + "\n", encoding="utf-8")
    filas = []
    for _, f in resultado["excepciones_detalle"].iterrows():
        filas.append(f"{escapar_tex(f['codigoOC'])} & {numero_es(f['MontoNetoOC_CLP'],2)} & {numero_es(f['neto_linea_clp_diagnostico'],2)} & {numero_es(f['diferencia_clp'],2)} " + r"\\")
    inicio_excepciones = r"""\begin{tabular}{@{}lrrr@{}}
\toprule
Orden & Neto OC (CLP) & Suma de firmas & Diferencia\\
\midrule
"""
    (destino / "tablas/excepciones.tex").write_text(inicio_excepciones + "\n".join(filas) + "\n" + r"\bottomrule" + "\n" + r"\end{tabular}" + "\n", encoding="utf-8")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(6.5, 2.8), layout="constrained")
    etiquetas = ["Actividad del proveedor", "Región del proveedor"]
    valores = [m["nulos_por_oc"][c] / m["ordenes"] * 100 for c in ["ActividadProveedor", "RegionProveedor"]]
    barras = ax.barh(etiquetas, valores, color=["#126D82", "#668AAD"], height=.5)
    ax.invert_yaxis()
    ax.set_xlim(0, max(valores) * 1.25)
    ax.set_xlabel("Órdenes sin información (%) · denominador: 541 OC")
    ax.bar_label(barras, labels=[numero_es(v, 2) + "%" for v in valores], padding=5)
    fig.savefig(destino / "figuras/faltantes_oc.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    (destino / "tablas/procedencia.json").write_text(json.dumps({"sha256_original": m["origen"]["sha256"], "generador": "F2/src/informe.py", "entrada": "ejecutar_pipeline(raiz)", "sin_cifras_editadas_a_mano": True}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
