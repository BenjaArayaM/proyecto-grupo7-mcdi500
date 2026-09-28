# MCDI500 · Grupo 7 · Sumativa 1

Preparación reproducible de órdenes de Compra Ágil de la Municipalidad de Valparaíso.

La pregunta central del mapa conceptual es cómo se distribuyen los montos por proveedor, rubro y mes. En la **Sumativa 1**, **F1** define el problema, los datos y el entorno de trabajo, mientras **F2** desarrolla la exploración, limpieza, transformación, diagnóstico y validación inicial de los datos.

**Estado:** F1 y F2 se encuentran implementadas y validadas; F3 Formativa fue integrada, validada y publicada en `main`. F4 permanece proyectada según las futuras etapas del proyecto.

---

## Integrantes

* Benjamín Araya Matta
* Jorge Guaico Ortega
* Alan Cañete Calquin
* Patricio Cortez Triviño

Las contribuciones individuales se identifican mediante ramas, commits y registros en `docs/bitacora_decisiones.md`.

---

## Estructura del repositorio

```text
.
├── F1/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── docs/
│   ├── notebooks/
│   └── src/
├── F2/
│   ├── data/
│   │   └── processed/
│   ├── docs/
│   ├── notebooks/
│   ├── src/
│   └── tests/
├── F3/
├── F4/
├── docs/
├── evidencias/
├── informe/
├── scripts/
├── proyecto.json
├── requirements.txt
└── requirements-validacion.txt
```

### Componentes principales

| Ruta                                     | Función                                                       |
| ---------------------------------------- | ------------------------------------------------------------- |
| `F1/notebooks/F1_Definicion.ipynb`       | Definición del problema, datos y entorno                      |
| `F1/src/entorno.py`                      | Validaciones iniciales del entorno y datos                    |
| `F1/data/raw/`                           | Datos originales utilizados por el proyecto                   |
| `F2/notebooks/F2_Preprocesamiento.ipynb` | Exploración, diagnóstico y documentación del preprocesamiento |
| `F2/src/preprocesamiento.py`             | Limpieza, transformación y generación de resultados           |
| `F2/src/informe.py`                      | Generación de elementos diagnósticos para el informe          |
| `F2/tests/`                              | Pruebas automatizadas del preprocesamiento                    |
| `F2/data/processed/`                     | Parámetros y resultados generados por el pipeline             |
| `scripts/`                               | Automatización de ejecución y verificación                    |
| `evidencias/`                            | Registros de ejecuciones y validaciones                       |
| `docs/`                                  | Bitácora, decisiones y trazabilidad con el mapa               |
| `informe/`                               | Informe técnico y elementos asociados                         |

---

## Relación con el mapa conceptual

El mapa conceptual de la Sumativa 1 se encuentra en:

* `F1/docs/Mapa_conceptual_Grupo7_V2.pdf`
* `F1/docs/Mapa_conceptual_Grupo7_V2_EDITABLE.pptx`

La materialización de sus componentes en el repositorio se documenta en:

`docs/vinculacion_mapa.md`

En términos generales:

* **Datos originales:** lectura, validación y versionado.
* **Exploración:** Jupyter y pandas.
* **Limpieza y transformación:** Python y pandas.
* **Indicadores y transformaciones:** NumPy.
* **Valores faltantes:** diagnóstico y política documentada.
* **Valores atípicos:** identificación y conservación para análisis.
* **Jerarquía de rubros:** conservación de N1, N2 y N3.
* **Git/GitHub:** control de versiones, ramas y trazabilidad.
* **Informe técnico:** resultados documentados en LaTeX y PDF.
* **F3/F4:** etapas proyectadas, sin afirmar ejecución en esta Sumativa 1.

---

## Datos

El proyecto utiliza datos de órdenes de Compra Ágil de la Municipalidad de Valparaíso.

El archivo original se encuentra versionado en:

```text
F1/data/raw/187402OCCompraAgil.csv
```

Durante la validación se identificaron:

* **11.177 filas** en el archivo original.
* **541 órdenes de compra** identificadas como cabeceras válidas para el procesamiento.
* **6 filas idénticas adicionales** detectadas durante la revisión.
* **3 excepciones de detalle** registradas para revisión.

El archivo original no es sobrescrito por las transformaciones. Los resultados derivados se generan mediante el pipeline de F2.

Las tablas derivadas con registros individuales pueden generarse localmente a partir del pipeline. Su publicación debe revisarse de acuerdo con las condiciones de uso de los datos.

---

## Dependencias y entorno

El proyecto mantiene `requirements.txt` como archivo principal de dependencias.

### Validación inicial de reproducibilidad

Como primera comprobación de estabilidad se realizó una ejecución en un entorno basado en **Python 3.12.14**, utilizando las versiones registradas en:

```text
requirements-validacion.txt
```

Ese archivo conserva la evidencia histórica de dicha validación inicial y **no reemplaza** al `requirements.txt` del equipo.

Posteriormente se revisaron las versiones y disponibilidad de las bibliotecas utilizadas y se continuó la validación en un entorno local actualizado.

### Entorno histórico de validación local de F1 y F2

* Sistema operativo: Windows
* Python: 3.13.15
* Entorno virtual: `.venv`
* Kernel Jupyter: `grupo7_mcdi500`
* Dependencias: `requirements.txt`

El intérprete utilizado durante la validación fue:

```text
.venv/Scripts/python.exe
```

La instalación se verificó mediante `pip check`, sin dependencias rotas.

---

## Preparación del entorno

### Windows · Git Bash

Desde la raíz del repositorio:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m pip check
```

Para registrar el kernel utilizado por Jupyter:

```bash
python -m ipykernel install --user --name grupo7_mcdi500 --display-name "Python (grupo7-mcdi500)"
```

### macOS / Linux

Para la revisión de Formativa 3 se proporciona un conjunto de dependencias directo y comprobado; el listado histórico de Windows no es un bloqueo multiplataforma.

```bash
python3 -m venv .venv-f3
source .venv-f3/bin/activate
python -m pip install -r requirements-formativa3.txt
python -m pip check
```

Si se desea utilizar el proyecto mediante Jupyter, registrar el kernel con:

```bash
python -m ipykernel install --user --name grupo7_mcdi500 --display-name "Python (grupo7-mcdi500)"
```

---

## Ejecución de notebooks

Las ejecuciones se realizan desde la raíz del repositorio.

### F1

```bash
python scripts/ejecutar_notebooks.py --fase F1 --kernel grupo7_mcdi500
```

### F2

```bash
python scripts/ejecutar_notebooks.py --fase F2 --kernel grupo7_mcdi500
```

### F1 y F2

```bash
python scripts/ejecutar_notebooks.py --fase ambas --kernel grupo7_mcdi500
```

El script ejecuta las celdas de código de cada notebook, conserva las salidas y genera evidencia de la ejecución.

---

## Ejecución del pipeline de F2

El pipeline completo de transformación puede ejecutarse mediante:

```bash
python scripts/ejecutar_pipeline.py
```

En la validación local se obtuvo:

```text
Original: 11177 filas; salida: 541 órdenes.
Excepciones de detalle para revisión: 3.
Tablas generadas en F2/data/processed y diagnóstico en F2/docs.
```

Entre los resultados generados se encuentran tablas procesadas, relaciones de órdenes y rubros, variables exploratorias y parámetros de transformación.

---

## Pruebas automatizadas

Las pruebas de F2 se ejecutan mediante:

```bash
python -m unittest discover -s F2/tests -v
```

La validación realizada registró:

```text
Ran 18 tests
OK
```

La evidencia correspondiente se conserva en:

```text
evidencias/pruebas_F2.json
```

---

## Verificación general de la entrega

El repositorio incorpora un script para revisar la presencia de evidencias y la ejecución registrada:

```bash
python scripts/verificar_entrega.py
```

La ejecución realizada revisó:

6 celdas de código de F1.
12 celdas de código de F2.
Evidencia de ejecución disponible.

Esta verificación es una revisión técnica de la entrega y no reemplaza la revisión académica del equipo.

## Evidencias de reproducibilidad

Los principales registros se encuentran en:

```text
evidencias/
├── ejecucion_F1.json
├── ejecucion_F2.json
├── ejecucion_pipeline_F2.json
├── entorno_F1.json
├── entorno_F2.json
├── pruebas_F2.json
└── validacion_base.json
```

Estos archivos permiten relacionar las ejecuciones con el notebook, entorno, kernel, cantidad de celdas ejecutadas y revisión Git correspondiente.

La evidencia de ejecución actual registra:

F1: 6 celdas de código, 0 errores.
F2: 12 celdas de código, 0 errores.
Pruebas F2: 18 pruebas, 0 fallos y 0 errores.
Pipeline F2: 11.177 filas originales y 541 órdenes de salida.
## Decisiones técnicas relevantes
Conservación del dato original

El archivo ubicado en F1/data/raw/ no se modifica durante el procesamiento. Las transformaciones se realizan sobre estructuras derivadas.

Valores faltantes

Los valores faltantes se diagnostican antes de aplicar una política de tratamiento. La comparación y sus resultados se conservan en:

F2/docs/comparacion_faltantes.csv
Valores atípicos

Los valores atípicos se identifican mediante procedimientos documentados en F2. Se conservan para su posterior análisis en lugar de eliminarlos automáticamente.

Proveedores

La normalización de proveedores se revisa considerando RUT y nombre. En la ejecución validada no se detectaron RUT asociados a múltiples nombres normalizados.

Rubros

La jerarquía N1–N3 se conserva durante el procesamiento. Una orden puede relacionarse con más de una categoría, por lo que no se debe repetir automáticamente su importe completo al agregar por categoría.

Registros duplicados

Las filas idénticas detectadas se documentan y se revisan antes de aplicar cualquier eliminación. La conciliación de firmas deja excepciones explícitas para revisión.

## Hallazgos de la validación de datos

Durante la revisión de F1 y F2 se documentaron, entre otros, los siguientes puntos:

El archivo contiene 11.177 filas, pero estas no corresponden directamente a 11.177 órdenes de compra.
La conciliación permite identificar 541 cabeceras de órdenes.
Se identificaron etiquetas en los niveles N1, N2 y N3 de la jerarquía de rubros.
Se identificaron órdenes relacionadas con más de un N1.
La evaluación de proveedores mediante RUT y nombre no detectó, en esta ejecución, RUT asociados a múltiples nombres normalizados.
Se identificaron registros idénticos adicionales que requieren conciliación antes de cualquier tratamiento.
La detección de valores extremos depende de la variable analizada y del denominador utilizado, por lo que los conteos deben interpretarse junto con la definición de cada métrica.

El detalle y la trazabilidad de estos hallazgos se encuentran en docs/vinculacion_mapa.md y en los archivos diagnósticos de F2.

## Informe técnico de F1 y F2

El informe se encuentra en:

informe/informe.pdf

La fuente principal está disponible en:

informe/informe.tex

Para compilar el informe se puede utilizar:

python scripts/compilar_informe.py

Los elementos auxiliares del informe se encuentran en:

informe/figuras/
informe/tablas/
## Versionado y flujo de trabajo

El proyecto utiliza Git para registrar el desarrollo mediante commits y ramas.

Flujo recomendado:

```bash
git status
git pull --ff-only
```

Realizar los cambios y validaciones correspondientes y luego:

```bash
git status
git diff --check
git add <archivos>
git commit -m "tipo: descripción breve del cambio"
git pull --ff-only
git push
```

Las contribuciones individuales se identifican mediante:

ramas de trabajo;
commits identificables;
validaciones asociadas a cada contribución;
registros en docs/bitacora_decisiones.md.

La bitácora permite complementar el historial Git con las decisiones y validaciones relevantes del proyecto.

## Convención de commits

Se recomienda utilizar mensajes breves y descriptivos, por ejemplo:

```text
feat: agrega transformación de datos
fix: corrige tratamiento de faltantes
docs: actualiza README
test: agrega pruebas de preprocesamiento
chore: actualiza configuración del entorno
```
## Estado de las fases
| Fase | Estado |
|---|---|
| F1 · Definición | Implementada y validada |
| F2 · Preprocesamiento | Implementada y validada |
| F3 · Formativa | Integrada, validada y publicada en `main` |
| F4 | Proyectada |

En la Sumativa 1, F3 y F4 estaban proyectadas. La Formativa 3 y su revisión se documentan en los apartados siguientes; F4 continúa pendiente.

## Documentación complementaria
- `docs/bitacora_decisiones.md` — registro de decisiones y validaciones.
- `docs/vinculacion_mapa.md` — trazabilidad entre el mapa conceptual y los artefactos implementados.
- `docs/matriz_rubrica.md` — relación con los criterios de evaluación.
- `docs/plan_sumativa1.md` — planificación de la Sumativa 1.
- `docs/inicio_gitbash.md` — apoyo para configuración y flujo Git.
- `requirements.txt` — dependencias principales del proyecto.
- `requirements-validacion.txt` — registro histórico de la primera validación estable del entorno.
## Reproducibilidad de F1 y F2

El procedimiento histórico de esas fases es:

1. Clonar o descargar el repositorio.
2. Crear un entorno virtual.
3. Instalar `requirements.txt`.
4. Ejecutar `pip check`.
5. Registrar el kernel `grupo7_mcdi500`.
6. Ejecutar F1 y F2 mediante `scripts/ejecutar_notebooks.py`.
7. Ejecutar el pipeline de F2.
8. Ejecutar las pruebas automatizadas.
9. Ejecutar `scripts/verificar_entrega.py`.

La secuencia permite verificar por separado el entorno, los notebooks, el pipeline, las pruebas y las evidencias de ejecución.

## Entrega original de Formativa 3

Durante la Fase 3 se incorporó una evaluación de eficiencia algorítmica aplicada a la detección de valores atípicos mediante IQR sobre la variable `MontoNetoOC_CLP`.

Se compararon dos implementaciones funcionalmente equivalentes:

- una basada en bucle;
- una basada en operaciones vectorizadas con pandas.

Ambas identificaron 61 valores potencialmente atípicos sobre 541 observaciones. La comparación de tiempos se realizó mediante `time.perf_counter()`, utilizando 1.000 ejecuciones por medición y tres repeticiones por implementación.

Los principales archivos incorporados en esta fase son:

- `F3/notebooks/F3_Formativa_Eficiencia_IQR.ipynb`
- `F3/src/funciones_iqr.py`
- `F3/docs/f3_s02_grupo7.pdf`

La organización de esta fase separa la ejecución y documentación del análisis en el notebook de las funciones reutilizables almacenadas en `F3/src`.


## Revisión de Formativa 3 según retroalimentación docente

La entrega evaluada obtuvo 53/69. Esta revisión añade pruebas reales, límites IQR
reutilizables y mediciones de tiempo/memoria para siete tamaños. La integración posterior
incorpora además la arquitectura POO de F3, conservando F2 como productor de `ordenes.csv`,
las 541 OC y los 61 extremos, sin nuevas imputaciones.

- Arquitectura y relación entre fases: `F3/docs/arquitectura.md`.
- Casos y resultados de prueba: `F3/tests/test_funciones_iqr.py` y `F3/evidencias`.
- Datos del experimento: `F3/docs/benchmark_iqr.csv`, `benchmark_iqr_muestras.json` y `resultados_iqr.json`.
- Correspondencia con la evaluación: `F3/docs/correcciones_formativa3.md`.
- Informe de entrega: `F3/docs/f3_s02_grupo7.pdf`; fuente reproducible en LaTeX junto al PDF.
- Dependencias directas comprobadas: `requirements-formativa3.txt`. No se reemplaza automáticamente el entorno de cada integrante.

Desde la raíz y con el entorno activado:

```bash
python scripts/ejecutar_pipeline.py
python scripts/ejecutar_formativa3.py
python scripts/verificar_formativa3.py
python scripts/compilar_formativa3.py
```

El notebook contiene 11 celdas de código en la ejecución actualmente validada. El ejecutor
usa un proceso de kernel nuevo, conserva las salidas y verifica las celdas ejecutadas. La ejecución
registrada de F3 no presentó errores.
El PDF se compila desde las métricas de la ejecución registrada, no desde tiempos escritos a mano.

El bucle y pandas son O(n), pero pandas prepara máscaras y selección; ese costo fijo puede dominar
en n pequeño. Los tamaños mayores son réplicas de carga, no nuevas observaciones. El pico de
`tracemalloc` no representa la RAM total. La decisión de rendimiento depende de la máquina.

Las evidencias incluidas en el paquete están rotuladas `validacion_asistida_linux`; cada integrante
debe generar y revisar su ejecución antes de atribuirse una validación. `.mailmap` unifica la
presentación de alias verificados con el mismo correo, sin reescribir commits.
