"""Pruebas de riesgos analíticos: pérdida de órdenes, formatos y límites."""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from F2.src.preprocesamiento import (
    codificar_nominal, codificar_tamano, comparar_faltantes, convertir_decimal,
    convertir_fecha, estandarizar, ejecutar_pipeline, marcar_iqr,
    normalizar_rut, proyectar_ordenes,
)


class TestFunciones(unittest.TestCase):
    def test_coma_decimal_miles_y_nulo(self):
        resultado = convertir_decimal(pd.Series(["1.234,50", "0", "-2,5", None]))
        self.assertEqual(resultado.iloc[:3].tolist(), [1234.5, 0.0, -2.5])
        self.assertTrue(pd.isna(resultado.iloc[3]))

    def test_texto_numerico_invalido_no_se_vuelve_cero(self):
        for valor in ["no informado", "12.34", "NaN", "inf", "1e3"]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                convertir_decimal(pd.Series([valor]))

    def test_decimal_entrada_vacia(self):
        self.assertEqual(len(convertir_decimal(pd.Series([], dtype="string"))), 0)

    def test_fecha_imposible_falla(self):
        with self.assertRaises(ValueError):
            convertir_fecha(pd.Series(["31-02-2025 0:00:00"]))

    def test_fecha_dayfirst_explicita(self):
        self.assertEqual(convertir_fecha(pd.Series(["06-01-2025 0:00:00"])).iloc[0], pd.Timestamp("2025-01-06"))

    def test_orden_repetida_se_cuenta_una_vez_sin_mutar(self):
        datos = pd.DataFrame({"codigoOC": ["A", "A", "B"], "monto": [100, 100, 50]})
        copia = datos.copy(deep=True)
        resultado = proyectar_ordenes(datos, ["codigoOC", "monto"])
        self.assertEqual(resultado["monto"].sum(), 150)
        assert_frame_equal(datos, copia)

    def test_orden_con_montos_contradictorios_falla(self):
        datos = pd.DataFrame({"codigoOC": ["A", "A"], "monto": [100, 999]})
        with self.assertRaisesRegex(ValueError, "no constantes"):
            proyectar_ordenes(datos, ["codigoOC", "monto"])

    def test_columna_faltante_y_codigo_vacio(self):
        with self.assertRaisesRegex(ValueError, "Faltan columnas"):
            proyectar_ordenes(pd.DataFrame({"codigoOC": ["A"]}), ["codigoOC", "monto"])
        with self.assertRaises(ValueError):
            proyectar_ordenes(pd.DataFrame({"codigoOC": [None], "monto": [1]}), ["codigoOC", "monto"])

    def test_rut_con_cero_inicial_conservado(self):
        self.assertEqual(normalizar_rut(pd.Series([" 01.234.567-k "])).iloc[0], "01234567-K")

    def test_iqr_constante_y_extremo(self):
        marcas, _ = marcar_iqr(pd.Series([4.0]*5))
        self.assertFalse(marcas.any())
        marcas, _ = marcar_iqr(pd.Series([1.0]*10 + [1000.0]))
        self.assertTrue(marcas.iloc[-1])
        with self.assertRaises(ValueError):
            marcar_iqr(pd.Series([1.0]), factor=0)

    def test_estandarizacion_constante_y_todo_nulo(self):
        z, parametros = estandarizar(pd.Series([4.0, 4.0]))
        self.assertEqual(z.tolist(), [0.0, 0.0])
        self.assertEqual(parametros["desviacion"], 0)
        with self.assertRaises(ValueError):
            estandarizar(pd.Series([np.nan]))

    def test_tamano_desconocido_no_es_micro(self):
        orden = ["Micro", "Pequeña", "Mediana", "Grande"]
        x = codificar_tamano(pd.Series(["Micro", "Grande", "NoClasificado"]), orden)
        self.assertEqual(x.iloc[:2].tolist(), [1, 4])
        self.assertTrue(pd.isna(x.iloc[2]))
        with self.assertRaises(ValueError):
            codificar_tamano(pd.Series(["Gigante"]), orden)

    def test_onehot_una_categoria(self):
        x = codificar_nominal(pd.DataFrame({"moneda": ["CLP", "CLP"]}), ["moneda"])
        self.assertEqual(x.shape, (2, 1))
        self.assertEqual(x.sum(axis=1).tolist(), [1, 1])

    def test_faltantes_sin_nulos_no_elimina(self):
        x = comparar_faltantes(pd.DataFrame({"region": ["A", "B"]}), ["region"])
        self.assertTrue(x["ordenes_retenidas"].eq(2).all())
        self.assertTrue(x["atributos_reales_asignados_sin_evidencia"].eq(0).all())


class TestArchivoReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resultado = ejecutar_pipeline(Path(__file__).resolve().parents[2])

    def test_proyeccion_y_claves_foraneas(self):
        r = self.resultado
        self.assertEqual(r["metricas"]["filas_original"], 11177)
        self.assertEqual(len(r["ordenes"]), 541)
        self.assertTrue(r["ordenes"]["codigoOC"].is_unique)
        self.assertEqual(set(r["relacion_rubros"]["codigoOC"]), set(r["ordenes"]["codigoOC"]))

    def test_no_ocultar_tres_excepciones_de_detalle(self):
        r = self.resultado
        self.assertEqual(set(r["excepciones_detalle"]["codigoOC"]), {"2427-264-AG25", "2427-511-AG25", "2427-543-AG25"})
        self.assertEqual(r["metricas"]["ordenes_conciliadas_firmas"], 538)
        caso = r["excepciones_detalle"].set_index("codigoOC").loc["2427-264-AG25"]
        self.assertAlmostEqual(float(caso["diferencia_clp"]), -1000000)

    def test_preservar_montos_estados_y_faltantes(self):
        r = self.resultado
        self.assertEqual(r["ordenes"]["ActividadProveedor"].isna().sum(), 139)
        self.assertEqual(r["ordenes"]["RegionProveedor"].isna().sum(), 8)
        self.assertEqual(r["ordenes"]["estado_habilitado_descriptivo"].sum(), 540)
        self.assertAlmostEqual(float(r["ordenes"]["MontoNetoOC_CLP"].sum()), 669016915.2110329, places=3)

    def test_transformaciones_y_denominador_del_mapa(self):
        r = self.resultado
        self.assertAlmostEqual(float(r["variables"]["neto_clp_z"].mean()), 0.0, places=10)
        self.assertAlmostEqual(float(np.std(r["variables"]["neto_clp_z"].to_numpy(dtype=float), ddof=0)), 1.0, places=10)
        self.assertEqual(r["metricas"]["extremos_mapa_total_oc_solo_clp"], 60)
        self.assertEqual(r["metricas"]["extremos_neto_clp_todos_estados"], 61)


if __name__ == "__main__":
    unittest.main(verbosity=2)
