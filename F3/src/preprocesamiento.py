"""Pipeline de Compra Ágil - Versión con Patrón Strategy.

Una fila exportada NO equivale a una orden ni a un ítem.
El original se preserva. Las proyecciones se deduplican solo después de validar
su unidad de observación.
"""

from __future__ import annotations
import json
from abc import ABC, abstractmethod
from pathlib import Path
import numpy as np
import pandas as pd
from F1.src.entorno import cargar_configuracion, reconocer_archivo, verificar_original


# ==========================================
# 1. FUNCIONES PURAS Y DE UTILIDAD
# ==========================================

def exigir_columnas(datos: pd.DataFrame, columnas: list[str]) -> None:
    faltan = sorted(set(columnas) - set(datos.columns))
    if faltan:
        raise ValueError(f"Faltan columnas requeridas: {faltan}")


def perfil_columnas(datos: pd.DataFrame) -> pd.DataFrame:
    n = len(datos)
    return pd.DataFrame({
        "columna": datos.columns, "tipo_lectura": datos.dtypes.astype(str).values,
        "filas": n, "faltantes": datos.isna().sum().values,
        "porcentaje_faltantes": datos.isna().mean().values * 100,
        "valores_distintos": datos.nunique(dropna=True).values,
    })


def proyectar_ordenes(datos: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    exigir_columnas(datos, columnas)
    if "codigoOC" not in columnas:
        raise ValueError("La proyección debe incluir codigoOC.")
    if datos.empty or datos["codigoOC"].isna().any():
        raise ValueError("Se requieren órdenes no vacías y un codigoOC por fila.")
    atributos = [c for c in columnas if c != "codigoOC"]
    variaciones = datos.groupby("codigoOC", dropna=False)[atributos].nunique(dropna=False)
    conflictos = variaciones.gt(1)
    if conflictos.any().any():
        ejemplos = conflictos.stack()[lambda x: x].index.tolist()[:10]
        raise ValueError(f"Atributos no constantes dentro de una OC: {ejemplos}")
    return datos.loc[:, columnas].drop_duplicates().sort_values("codigoOC").reset_index(drop=True).copy()


def convertir_decimal(serie: pd.Series) -> pd.Series:
    texto = serie.astype("string").str.strip()
    patron = r"[+-]?(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d+)?"
    incorrecto = texto.notna() & ~texto.str.fullmatch(patron, na=False)
    if incorrecto.any():
        raise ValueError(f"Formato numérico inválido en {serie.name}: {texto[incorrecto].head(5).tolist()}")
    limpio = texto.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    resultado = pd.to_numeric(limpio, errors="raise").astype("Float64")
    if not np.isfinite(resultado.dropna().to_numpy(dtype=float)).all():
        raise ValueError(f"Número no finito en {serie.name}")
    return resultado


def convertir_fecha(serie: pd.Series) -> pd.Series:
    return pd.to_datetime(serie, format="%d-%m-%Y %H:%M:%S", errors="raise")


def normalizar_rut(serie: pd.Series) -> pd.Series:
    return serie.astype("string").str.strip().str.upper().str.replace(".", "", regex=False).str.replace(r"\s+", "", regex=True)


def marcar_iqr(serie: pd.Series, factor: float = 1.5) -> tuple[pd.Series, dict]:
    if factor <= 0:
        raise ValueError("El factor IQR debe ser positivo.")
    valores = serie.dropna().to_numpy(dtype=float)
    if len(valores) == 0 or not np.isfinite(valores).all():
        raise ValueError("IQR requiere al menos un número finito.")
    q1, q3 = np.percentile(valores, [25, 75], method="linear")
    inferior, superior = float(q1 - factor * (q3-q1)), float(q3 + factor * (q3-q1))
    marca = ((serie < inferior) | (serie > superior)).astype("boolean")
    marca.loc[serie.isna()] = pd.NA
    return marca, {"n": len(valores), "q1": float(q1), "q3": float(q3), "limite_inferior": inferior, "limite_superior": superior, "factor": factor}


def estandarizar(serie: pd.Series) -> tuple[pd.Series, dict]:
    valores = serie.dropna().to_numpy(dtype=float)
    if len(valores) == 0 or not np.isfinite(valores).all():
        raise ValueError("Estandarización requiere números finitos observados.")
    media, desviacion = float(np.mean(valores)), float(np.std(valores, ddof=0))
    z = (serie - media) / desviacion if desviacion > 0 else serie * 0
    return z.astype("Float64"), {"media": media, "desviacion": desviacion, "ddof": 0}


def codificar_tamano(serie: pd.Series, orden: list[str]) -> pd.Series:
    inesperadas = set(serie.dropna().unique()) - set(orden) - {"NoClasificado"}
    if inesperadas:
        raise ValueError(f"Tamaños no contemplados: {sorted(inesperadas)}")
    return serie.map({categoria: i + 1 for i, categoria in enumerate(orden)}).astype("Int64")


def codificar_nominal(datos: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    exigir_columnas(datos, columnas)
    if datos[columnas].isna().any().any():
        raise ValueError("Declare una política de categorías faltantes antes de codificar.")
    return pd.get_dummies(datos[columnas].astype("string"), columns=columnas, dtype="int8")


# ==========================================
# 2. Clases y Patron de Diseño
# ==========================================

class EstrategiaFaltantes(ABC):
    """Interfaz abstracta (Strategy) para el manejo de valores faltantes."""
    
    @property
    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def evaluar(self, ordenes: pd.DataFrame, columna: str, nulos: int) -> tuple[int, int]:
        """Retorna una tupla con (ordenes_retenidas, atributos_asignados)."""
        pass


class EstrategiaEliminarOrden(EstrategiaFaltantes):
    @property
    def nombre(self) -> str:
        return "eliminar_orden_sin_dato"

    def evaluar(self, ordenes: pd.DataFrame, columna: str, nulos: int) -> tuple[int, int]:
        return len(ordenes) - nulos, 0


class EstrategiaImputarModa(EstrategiaFaltantes):
    @property
    def nombre(self) -> str:
        return "imputar_moda"

    def evaluar(self, ordenes: pd.DataFrame, columna: str, nulos: int) -> tuple[int, int]:
        return len(ordenes), nulos


class EstrategiaConservarMarca(EstrategiaFaltantes):
    @property
    def nombre(self) -> str:
        return "conservar_NA_y_marca"

    def evaluar(self, ordenes: pd.DataFrame, columna: str, nulos: int) -> tuple[int, int]:
        return len(ordenes), 0


def comparar_faltantes(ordenes: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Aplica dinámicamente las estrategias de manejo de faltantes (Patrón Strategy)."""
    estrategias: list[EstrategiaFaltantes] = [
        EstrategiaEliminarOrden(),
        EstrategiaImputarModa(),
        EstrategiaConservarMarca()
    ]
    
    filas = []
    for columna in columnas:
        nulos = int(ordenes[columna].isna().sum())
        for est in estrategias:
            retenidas, asignados = est.evaluar(ordenes, columna, nulos)
            filas.append({
                "columna": columna, 
                "estrategia": est.nombre, 
                "ordenes_iniciales": len(ordenes),
                "faltantes_originales": nulos, 
                "ordenes_retenidas": retenidas,
                "atributos_reales_asignados_sin_evidencia": asignados
            })
    return pd.DataFrame(filas)


# ==========================================
# 3. PREPARACIÓN Y DIAGNÓSTICO
# ==========================================

def preparar_ordenes(ordenes: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, dict]:
    salida = ordenes.copy(deep=True)
    for columna in config["seleccion"]["numericas_oc"]:
        salida[columna] = convertir_decimal(salida[columna])
    salida["FechaEnvioOC"] = convertir_fecha(salida["FechaEnvioOC"])
    esenciales = ["FechaEnvioOC", "ProveedorRUT", "MontoNetoOC_CLP", "MonedaOC", "EstadoOC"]
    if salida[esenciales].isna().any().any():
        raise ValueError("Falta un atributo esencial.")
    if (salida["MontoNetoOC_CLP"] < 0).any():
        raise ValueError("Montos netos negativos.")
    salida["ProveedorRUT_normalizado"] = normalizar_rut(salida["ProveedorRUT"])
    salida["Proveedor_nombre_comparable"] = salida["Proveedor"].str.strip().str.replace(r"\s+", " ", regex=True).str.upper()
    salida["mes_envio"] = salida["FechaEnvioOC"].dt.to_period("M").astype("string")
    salida["estado_habilitado_descriptivo"] = salida["EstadoOC"].isin(config["analisis"]["estados_habilitados"])
    for columna in ["ActividadProveedor", "RegionProveedor"]:
        salida[columna + "_faltante"] = salida[columna].isna()
        salida[columna + "_vista"] = salida[columna].fillna("Sin información")
    salida["extremo_iqr_neto_clp"], iqr = marcar_iqr(salida["MontoNetoOC_CLP"])
    if not salida["codigoOC"].is_unique:
        raise AssertionError("La salida debe tener una fila por orden.")
    return salida, iqr


def construir_relacion_rubros(datos: pd.DataFrame) -> pd.DataFrame:
    columnas = ["codigoOC", "RubroN1", "RubroN2", "RubroN3"]
    exigir_columnas(datos, columnas)
    return datos[columnas].drop_duplicates().sort_values(columnas).reset_index(drop=True).copy()


def diagnosticar_detalle(datos: pd.DataFrame, ordenes: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    firma_item = ["codigoOC"] + config["seleccion"]["firma_item"]
    firma_cot = ["codigoOC"] + config["seleccion"]["firma_cotizacion"]
    exigir_columnas(datos, firma_item + firma_cot)
    items = datos[firma_item].drop_duplicates().copy()
    cot = datos[firma_cot].drop_duplicates().copy()
    items["neto_linea_clp_diagnostico"] = convertir_decimal(items["MontoNetoItemCLP"])
    suma = items.groupby("codigoOC")["neto_linea_clp_diagnostico"].sum(min_count=1)
    conciliacion = ordenes[["codigoOC", "MontoNetoOC_CLP"]].merge(suma, on="codigoOC", how="left", validate="one_to_one")
    conciliacion["diferencia_clp"] = conciliacion["neto_linea_clp_diagnostico"] - conciliacion["MontoNetoOC_CLP"]
    conciliacion["concilia_firmas_a_1_clp"] = conciliacion["diferencia_clp"].abs().le(1).fillna(False)
    grupos = ["codigoOC", "CodigoProductoONU"]
    cot = cot.rename(columns={"CodigoProductoCotizadoONU": "CodigoProductoONU"})
    cruzada = pd.concat([
        datos.groupby(grupos).size().rename("filas_exportadas"),
        items.groupby(grupos).size().rename("firmas_item"),
        cot.groupby(grupos).size().rename("firmas_cotizacion"),
    ], axis=1).reset_index()
    cruzada["producto_firmas"] = cruzada["firmas_item"] * cruzada["firmas_cotizacion"]
    cruzada["coincide_producto"] = cruzada["filas_exportadas"].eq(cruzada["producto_firmas"])
    return conciliacion, cruzada


def construir_variables(ordenes: pd.DataFrame, config: dict) -> tuple[pd.DataFrame, dict]:
    variables = ordenes[["codigoOC"]].copy()
    variables["neto_clp_z"], escala = estandarizar(ordenes["MontoNetoOC_CLP"])
    variables["tamano_ordinal"] = codificar_tamano(ordenes["TamanoProveedor"], config["analisis"]["orden_tamano"])
    variables["tamano_sin_clasificar"] = variables["tamano_ordinal"].isna()
    dummy = codificar_nominal(ordenes, ["MonedaOC", "EstadoOC"])
    return pd.concat([variables, dummy], axis=1), {"estandarizacion": escala, "orden_tamano": config["analisis"]["orden_tamano"], "columnas_nominales": dummy.columns.tolist()}


# ==========================================
# 4. CLASES DE ORQUESTACIÓN (POO)
# ==========================================

class TransformadorDatos:
    def __init__(self, config: dict):
        self.config = config

    def proyectar(self, datos: pd.DataFrame) -> pd.DataFrame:
        return proyectar_ordenes(datos, self.config["seleccion"]["columnas_oc"])

    def preparar(self, proyeccion: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        return preparar_ordenes(proyeccion, self.config)

    def construir_variables(self, ordenes: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        return construir_variables(ordenes, self.config)


class GeneradorMetricas:
    def __init__(self, datos: pd.DataFrame, ordenes: pd.DataFrame, config: dict):
        self.datos = datos
        self.ordenes = ordenes
        self.config = config

    def calcular(self, origen: str, proyeccion: pd.DataFrame, relacion: pd.DataFrame, 
                 conciliacion: pd.DataFrame, cruce: pd.DataFrame, variables: pd.DataFrame, iqr: dict) -> dict:
        
        importe_clp = self.ordenes.loc[self.ordenes["MonedaOC"].eq("CLP"), "MontoTotalOC"]
        marcas_mapa, iqr_mapa = marcar_iqr(importe_clp)
        nombres_rut = self.ordenes.groupby("ProveedorRUT_normalizado")["Proveedor_nombre_comparable"].nunique()
        excepciones = conciliacion.loc[~conciliacion["concilia_firmas_a_1_clp"]].copy()

        return {
            "origen": origen, "filas_original": len(self.datos), "columnas_original": len(self.datos.columns),
            "ordenes": len(self.ordenes), "proveedores_rut": int(self.ordenes["ProveedorRUT_normalizado"].nunique()),
            "fecha_min": self.ordenes["FechaEnvioOC"].min().date().isoformat(),
            "fecha_max": self.ordenes["FechaEnvioOC"].max().date().isoformat(),
            "filas_identicas_adicionales": int(self.datos.duplicated().sum()),
            "filas_en_grupos_identicos": int(self.datos.duplicated(keep=False).sum()),
            "rut_con_varios_nombres_normalizados": int(nombres_rut.gt(1).sum()),
            "monedas_oc": {str(k): int(v) for k, v in self.ordenes["MonedaOC"].value_counts().items()},
            "estados_oc": {str(k): int(v) for k, v in self.ordenes["EstadoOC"].value_counts().items()},
            "nulos_por_fila": {c: int(v) for c, v in self.datos.isna().sum().items() if v},
            "nulos_por_oc": {c: int(v) for c, v in proyeccion.isna().sum().items() if v},
            "rubros_distintos": {c: int(self.datos[c].nunique()) for c in ["RubroN1", "RubroN2", "RubroN3"]},
            "ordenes_con_mas_de_un_n1": int(relacion.groupby("codigoOC")["RubroN1"].nunique().gt(1).sum()),
            "n2_con_mas_de_un_padre_n1": int(relacion.groupby("RubroN2")["RubroN1"].nunique().gt(1).sum()),
            "grupos_oc_producto": len(cruce), "grupos_compatibles_con_producto_cartesiano": int(cruce["coincide_producto"].sum()),
            "ejemplo_699": cruce.loc[cruce["codigoOC"].eq("2427-699-AG25")].to_dict(orient="records"),
            "ordenes_conciliadas_firmas": int(conciliacion["concilia_firmas_a_1_clp"].sum()),
            "ordenes_no_conciliadas": excepciones["codigoOC"].tolist(),
            "neto_clp_total_todos_estados": float(self.ordenes["MontoNetoOC_CLP"].sum()),
            "ordenes_estado_habilitado": int(self.ordenes["estado_habilitado_descriptivo"].sum()),
            "extremos_neto_clp_todos_estados": int(self.ordenes["extremo_iqr_neto_clp"].sum()), "iqr_neto_clp": iqr,
            "extremos_mapa_total_oc_solo_clp": int(marcas_mapa.sum()), "iqr_mapa_total_oc_solo_clp": iqr_mapa,
            "faltantes_neto_clp": int(self.ordenes["MontoNetoOC_CLP"].isna().sum()),
            "varianza_neto_clp_sin_imputacion_ddof0": float(np.var(self.ordenes["MontoNetoOC_CLP"].to_numpy(dtype=float), ddof=0)),
            "tamano_sin_clasificar": int(variables["tamano_sin_clasificar"].sum()),
            "solo_proveedores_seleccionados": bool(self.datos["ProveedorSeleccionado"].eq("SI").all()),
        }


class ExportadorResultados:
    def __init__(self, raiz: Path):
        self.raiz = raiz

    def exportar(self, resultado: dict) -> None:
        destinos = {
            "ordenes": "F2/data/processed/ordenes.csv",
            "relacion_rubros": "F2/data/processed/relacion_orden_rubro.csv",
            "variables": "F2/data/processed/variables_exploratorias.csv",
            "perfil_original": "F2/docs/perfil_original.csv",
            "comparacion_faltantes": "F2/docs/comparacion_faltantes.csv",
            "conciliacion": "F2/docs/conciliacion_firmas.csv",
            "excepciones_detalle": "F2/docs/excepciones_detalle.csv",
            "cruce_exportacion": "F2/docs/cruce_exportacion.csv",
        }
        for tabla, destino in destinos.items():
            ruta = self.raiz / destino
            ruta.parent.mkdir(parents=True, exist_ok=True)
            resultado[tabla].to_csv(ruta, index=False, encoding="utf-8", lineterminator="\n", date_format="%Y-%m-%d", float_format="%.8f")
            
        for clave, destino in [("metricas", "F2/docs/metricas.json"), ("parametros", "F2/data/processed/parametros_transformacion.json")]:
            (self.raiz / destino).write_text(json.dumps(resultado[clave], ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


class PipelineCompraAgil:
    def __init__(self, raiz: Path):
        self.raiz = raiz

    def ejecutar(self) -> dict:
        config = cargar_configuracion(self.raiz)
        origen = verificar_original(self.raiz, config)
        datos = reconocer_archivo(self.raiz, config)
        
        exigir_columnas(datos, config["datos"]["columnas_esperadas"])
        if datos.columns.tolist() != config["datos"]["columnas_esperadas"]:
            raise ValueError("Cambió el esquema del archivo.")

        transformador = TransformadorDatos(config)
        proyeccion = transformador.proyectar(datos)
        ordenes, iqr = transformador.preparar(proyejson := proyeccion) # type: ignore
        
        relacion = construir_relacion_rubros(datos)
        conciliacion, cruce = diagnosticar_detalle(datos, ordenes, config)
        variables, parametros = transformador.construir_variables(ordenes)

        generador = GeneradorMetricas(datos, ordenes, config)
        metricas = generador.calcular(origen, proyeccion, relacion, conciliacion, cruce, variables, iqr)

        excepciones = conciliacion.loc[~conciliacion["concilia_firmas_a_1_clp"]].copy()

        resultado = {
            "ordenes": ordenes, "relacion_rubros": relacion, "variables": variables,
            "perfil_original": perfil_columnas(datos), 
            "comparacion_faltantes": comparar_faltantes(proyeccion, ["ActividadProveedor", "RegionProveedor"]),
            "conciliacion": conciliacion, "excepciones_detalle": excepciones, 
            "cruce_exportacion": cruce, "metricas": metricas, "parametros": parametros
        }

        assert origen == verificar_original(self.raiz, config)
        assert len(ordenes) == datos["codigoOC"].nunique()

        ExportadorResultados(self.raiz).exportar(resultado)
        return resultado