# MCDI500 · Grupo 7 · Sumativa 1

Preparación reproducible de órdenes de Compra Ágil de la Municipalidad de Valparaíso.
La pregunta del mapa es cómo se distribuyen los montos por proveedor, rubro y mes.
F1 define el problema y el entorno; F2 obtiene, diagnostica, prepara y valida.

**Estado: base inicial para revisión del equipo, con asistencia de Codex.** Los
resultados de validación no acreditan ejecución en los cuatro equipos ni cierre de
las decisiones metodológicas. El informe es un borrador técnico.

## Comenzar en el equipo Windows existente

Leer [inicio_gitbash.md](docs/inicio_gitbash.md). Se utiliza el repositorio y el
entorno virtual que el grupo ya creó; no hace falta reinicializar Git.

1. Incorporar los archivos descargables de la base y copiar el adjunto completo como
   **F1/data/raw/187402OCCompraAgil.csv**, sin editarlo ni guardarlo desde Excel.
2. Activar el entorno, comprobar dependencias y seleccionar el kernel
   **Python (grupo7-mcdi500)**.
3. Ejecutar F1 y F2, revisar las salidas y desarrollar las decisiones del equipo.
4. Editar **informe/informe.tex** en JupyterLab; compilar con el script.
5. Revisar cambios y evidencias antes de cada commit.

~~~bash
source .venv/Scripts/activate
python -m pip check
python -m jupyter lab
~~~

Ejecución automatizada, desde la raíz y con el kernel ya registrado:

~~~bash
python scripts/ejecutar_notebooks.py --fase ambas --kernel grupo7_mcdi500
python -m unittest discover -s F2/tests -v
python scripts/compilar_informe.py
python scripts/verificar_entrega.py
~~~

LaTeX requiere **pdflatex**, instalado con MiKTeX o TeX Live fuera del entorno Python.
JupyterLab permite editar el .tex y abrir el PDF. La compilación actual usa tres
pasadas de pdflatex para actualizar índice y referencias; no necesita Biber.

## Archivos y orden

| Ruta | Función |
|---|---|
| F1/data/raw/187402OCCompraAgil.csv | Original de 21.743.181 bytes, copiado sin cambios |
| proyecto.json | SHA-256, esquema completo, columnas seleccionadas y políticas |
| F1/notebooks/F1_Definicion.ipynb | Problema, objetivos, entorno y reconocimiento |
| F1/src/entorno.py | Rutas, integridad y entorno observado |
| F1/docs/Mapa_conceptual_Grupo7_V2.pdf | Mapa corregido; conserva su editable PPTX |
| F2/notebooks/F2_Preprocesamiento.ipynb | Secuencia analítica con narrativa y salidas |
| F2/src/preprocesamiento.py | Funciones parametrizadas del pipeline |
| F2/src/informe.py | Figura y tablas LaTeX generadas desde los resultados |
| F2/tests/test_preprocesamiento.py | Casos normales, límite, error y datos reales |
| F2/data/processed | Tablas y parámetros generados por código |
| F2/docs | Perfiles, conciliación y métricas cuantificadas |
| evidencias | Entorno y ejecuciones; distingue validación asistida de revisión local |
| informe/informe.tex | Fuente del borrador técnico |
| informe/referencias.tex | Referencias en formato autor-fecha y lista APA 7 |
| informe/informe.pdf | PDF compilado; revisar pendientes antes de entregar |
| docs | Plan, rúbrica, vínculo con mapa y bitácora |
| F3 y F4 | Fases posteriores, todavía proyectadas |

## Datos y unidades

La copia adjunta y la utilizada para el mapa V2 tienen el mismo SHA-256:

~~~text
1fcbdec3161500e95a15d2af82df3d007549f2d5da9a6d0b4e6063540406be1c
~~~

Lectura: separador punto y coma, Windows-1252, campos iniciales como texto.
11.177 filas y 63 columnas corresponden a **541 órdenes** y **277 RUT proveedores**.
La cobertura observada es 2025-01-06 a 2025-06-30. El archivo tiene relaciones
repetidas entre cabecera, ítems y cotizaciones: no sumar montos directamente por fila.

- **ordenes.csv:** 541 OC únicas, conserva todos los estados y los montos netos CLP.
- **relacion_orden_rubro.csv:** 1.683 relaciones de pertenencia; no contiene importes.
  Los conteos de OC por rubro se solapan.
- **variables_exploratorias.csv:** vista transformada, separada de los importes.
- **excepciones_detalle.csv:** tres OC cuyo detalle de firmas distintas no concilia.
  No se ha producido un detalle monetario definitivo por rubro.

La URL/fecha exactas de descarga y el diccionario oficial están pendientes de
documentación por el equipo. El original y las tablas con registros individuales
se mantienen fuera de GitHub, a la espera de autorización explícita para publicar
los datos de proveedores. Se generan localmente desde el adjunto de igual hash.
La rama por sí sola todavía no contiene todos los insumos para reproducir el análisis.

## Reproducibilidad y versiones

**requirements.txt** conserva el freeze previo del equipo Windows; aún debe
comprobarse su reconstrucción. **requirements-validacion.txt** registra las
dependencias directas efectivamente utilizadas para comprobar esta base inicial:
Python 3.12.14, pandas 2.2.3, NumPy 2.3.5 y Matplotlib 3.10.8, entre otras.
No son dos entornos declarados equivalentes. Resolver y justificar las diferencias
antes de la entrega; no sustituir el freeze del equipo por uno de Linux a ciegas.

Los informes JSON y las celdas registran las versiones observadas. Los nombres de
archivo, RUT y códigos no dependen de rutas absolutas. La semilla 42 está declarada;
el pipeline actual no muestrea y es determinista.

La comprobación asistida ejecutó cada notebook en un proceso nuevo con ipykernel
en memoria, porque este entorno no permite conexiones Jupyter. El motor consta en
las evidencias. La ejecución habitual con JupyterLab y kernel del entorno Windows
sigue pendiente; el comando predeterminado usa ese modo normal.

## Versionamiento y cierre

No versionar el entorno virtual, contraseñas ni auxiliares de LaTeX. Esta rama
versiona código, parámetros, documentación y salidas agregadas ejecutadas.
El original y las tablas individuales están excluidos hasta autorizar su publicación.
El atributo -text evita que Git cambie saltos de línea del original al copiarlo
entre sistemas. El filtro nbstripout debe estar desactivado en este repositorio
para conservar evidencia; verificar también la copia preparada para el commit:

~~~bash
python scripts/verificar_entrega.py --staged
~~~

El paquete inicial contiene trabajo asistido y evidencia de validación. Todavía no se publicaron archivos ni nuevos commits de esta base.
Cada integrante debe revisar, ejecutar y aportar cambios propios durante el
desarrollo. No se inventan autores, fechas, revisiones ni colaboraciones.
Ver [matriz_rubrica.md](docs/matriz_rubrica.md) y [plan_sumativa1.md](docs/plan_sumativa1.md).
