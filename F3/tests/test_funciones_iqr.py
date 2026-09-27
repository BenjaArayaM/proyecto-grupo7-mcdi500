"""Casos solicitados por el docente y contratos de límites/entrada/salida."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal
from F3.src.funciones_iqr import (calcular_limites_iqr, detectar_atipicos_bucle,
                                detectar_atipicos_vectorizado, validar_serie)
from F3.src.datos_iqr import cargar_ordenes, encontrar_raiz
from F3.src.benchmark_iqr import replicar_serie, ejecutar_benchmark, resumir_cruces

FUNCIONES = (detectar_atipicos_bucle, detectar_atipicos_vectorizado)


class TestDeteccion(unittest.TestCase):
    def comprobar(self, valores, limites, esperado, index=None):
        serie = pd.Series(valores, dtype=float, index=index)
        copia = serie.copy(deep=True)
        for funcion in FUNCIONES:
            with self.subTest(funcion=funcion.__name__):
                self.assertEqual(funcion(serie, *limites), esperado)
                assert_series_equal(serie, copia)

    def test_sin_atipicos(self):
        self.comprobar([0, 1, 2], (-1, 3), [])

    def test_todos_atipicos_limites_externos(self):
        # No se estiman límites de estos mismos dos valores.
        self.comprobar([-10, 10, 20], (-1, 1), [-10, 10, 20])

    def test_serie_vacia(self):
        self.comprobar([], (-1, 1), [])

    def test_igualdad_en_limites_no_es_atipico(self):
        self.comprobar([-2, -1, 0, 1, 2], (-1, 1), [-2, 2])

    def test_preserva_orden_y_multiplicidad(self):
        self.comprobar([8, 0, -5, 8], (-1, 1), [8, -5, 8], [20, 2, 90, 20])


class TestLimites(unittest.TestCase):
    def test_cuartiles_conocidos(self):
        r = calcular_limites_iqr(pd.Series([0., 1., 2., 3., 4.]))
        self.assertEqual((r['q1'], r['q3'], r['iqr']), (1., 3., 2.))
        self.assertEqual((r['limite_inferior'], r['limite_superior']), (-2., 6.))

    def test_constante(self):
        r = calcular_limites_iqr(pd.Series([7., 7., 7.]))
        self.assertEqual(r['iqr'], 0)
        for funcion in FUNCIONES:
            self.assertEqual(funcion(pd.Series([7., 7., 7.]), r['limite_inferior'], r['limite_superior']), [])

    def test_un_valor(self):
        self.assertEqual(calcular_limites_iqr(pd.Series([7.]))['limite_superior'], 7.)

    def test_vacia_no_estima_cuartiles(self):
        with self.assertRaises(ValueError):
            calcular_limites_iqr(pd.Series([], dtype=float))

    def test_rechaza_faltantes_e_infinitos(self):
        for valor in [np.nan, np.inf, -np.inf]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                calcular_limites_iqr(pd.Series([1., valor]))

    def test_factor_invalido(self):
        for factor in [0, -1, np.nan, np.inf]:
            with self.subTest(factor=factor), self.assertRaises(ValueError):
                calcular_limites_iqr(pd.Series([1., 2.]), factor)

    def test_tipo_no_numerico(self):
        with self.assertRaises(TypeError):
            validar_serie(pd.Series(['a', 'b']))

    def test_no_modifica_y_factor_configurable(self):
        s = pd.Series([0., 1., 2., 3., 4.]); copia = s.copy()
        self.assertEqual(calcular_limites_iqr(s, 1.)['limite_superior'], 5.)
        assert_series_equal(s, copia)


class TestCarga(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(); self.raiz = Path(self.temp.name)
        (self.raiz / 'F2/data/processed').mkdir(parents=True)
        (self.raiz / 'proyecto.json').write_text('{}')
        self.ruta = self.raiz / 'F2/data/processed/ordenes.csv'

    def tearDown(self):
        self.temp.cleanup()

    def escribir(self, codigo=('OC1', 'OC2'), monto=(1., 3.), marca=(False, True)):
        pd.DataFrame({'codigoOC': codigo, 'MontoNetoOC_CLP': monto,
                      'extremo_iqr_neto_clp': marca}).to_csv(self.ruta, index=False)

    def test_carga_y_raiz(self):
        self.escribir(); datos, resumen = cargar_ordenes(self.raiz)
        self.assertEqual(len(datos), 2); self.assertEqual(resumen['eliminados'], 0)
        self.assertEqual(encontrar_raiz(self.ruta), self.raiz)

    def test_no_coacciona_texto_a_faltante(self):
        self.escribir(monto=('error', '3'))
        with self.assertRaises(ValueError): cargar_ordenes(self.raiz)

    def test_no_omite_faltantes(self):
        self.escribir(monto=(np.nan, 3.))
        with self.assertRaises(ValueError): cargar_ordenes(self.raiz)

    def test_rechaza_oc_duplicada(self):
        self.escribir(codigo=('OC1', 'OC1'))
        with self.assertRaises(ValueError): cargar_ordenes(self.raiz)

    def test_rechaza_marca_ambigua(self):
        self.escribir(marca=('quizas', 'True'))
        with self.assertRaises(ValueError): cargar_ordenes(self.raiz)

    def test_falta_archivo(self):
        with self.assertRaises(FileNotFoundError): cargar_ordenes(self.raiz)


class TestBenchmark(unittest.TestCase):
    def test_replica_exacta_no_modifica_original(self):
        s = pd.Series([1., 2., 3.]); copia = s.copy()
        self.assertEqual(replicar_serie(s, 5).tolist(), [1., 2., 3., 1., 2.])
        assert_series_equal(s, copia)

    def test_tamano_invalido(self):
        for n in [0, -1, 1.5, True]:
            with self.subTest(n=n), self.assertRaises(ValueError):
                replicar_serie(pd.Series([1.]), n)

    def test_medicion_conserva_muestras_y_equivalencia(self):
        s = pd.Series([0., 1., 2., 100.])
        tabla, muestras = ejecutar_benchmark(s, calcular_limites_iqr(s), [4, 8], 3, 2)
        self.assertEqual(len(tabla), 4); self.assertEqual(len(muestras), 24)
        self.assertTrue(tabla['min_por_llamada_us'].ge(0).all())
        self.assertTrue(tabla['mediana_pico_bytes'].ge(0).all())
        self.assertEqual(tabla.groupby('n')['atipicos'].nunique().tolist(), [1, 1])

    def test_cruce_es_intervalo_y_no_punto_exacto(self):
        t = pd.DataFrame({'n': [500, 500, 2000, 2000], 'metodo': ['bucle','pandas']*2,
                          'min_por_llamada_us': [2., 4., 8., 5.]})
        self.assertEqual(resumir_cruces(t)['intervalos_observados'],
                         [{'ultimo_n_bucle_no_mas_lento': 500, 'primer_n_pandas_mas_rapido': 2000}])


class TestIntegracionF2(unittest.TestCase):
    def test_mismas_observaciones_y_limites_que_f2(self):
        from F2.src.preprocesamiento import marcar_iqr
        raiz = Path(__file__).resolve().parents[2]
        datos, _ = cargar_ordenes(raiz)
        s = datos['MontoNetoOC_CLP']; r = calcular_limites_iqr(s)
        marca_f2, limites_f2 = marcar_iqr(s)
        self.assertEqual(len(s), 541); self.assertEqual(int(marca_f2.sum()), 61)
        self.assertEqual(r['q1'], 217923.); self.assertEqual(r['q3'], 1620152.)
        self.assertEqual(r['limite_superior'], 3723495.5)
        for clave in ['q1','q3','limite_inferior','limite_superior']:
            self.assertAlmostEqual(r[clave], limites_f2[clave], places=6)
        self.assertEqual(marca_f2.tolist(), datos['extremo_iqr_neto_clp'].tolist())
        esperados = s[marca_f2.astype(bool)].tolist()
        for funcion in FUNCIONES:
            self.assertEqual(funcion(s, r['limite_inferior'], r['limite_superior']), esperados)


if __name__ == '__main__': unittest.main()
