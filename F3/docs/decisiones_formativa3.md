# Bitácora de la revisión de Formativa 3

Fecha de preparación: 2026-09-27. Autoría de la propuesta: asistencia técnica; pendiente de revisión del grupo.
No reemplaza ni reescribe las decisiones históricas de `docs/bitacora_decisiones.md`.

| ID | Decisión y motivo | Evidencia |
|---|---|---|
| F3-R01 | Conservar los dos filtros y su salida como lista para comparar el mismo algoritmo de la entrega. | Igualdad de valores, orden y repetidos; marcas por OC coincidentes con F2. |
| F3-R02 | Extraer límites comunes y validar la entrada antes de medir. | `calcular_limites_iqr`; Q1=217923, Q3=1620152, límite superior=3723495,5 CLP. |
| F3-R03 | Preservar 541 OC y 61 extremos. Un extremo estadístico no demuestra error. | Cero eliminaciones/imputaciones; prueba de integración con F2. |
| F3-R04 | Distinguir vacío en detección de vacío al estimar cuartiles. | Detección devuelve `[]`; cálculo de límites rechaza la entrada sin observaciones. |
| F3-R05 | Replicar hasta 50.000 valores para medir carga sin inventar nuevas órdenes. | Siete tamaños en `benchmark_iqr.csv`; límites nativos fijos. |
| F3-R06 | Medir memoria separada del tiempo. | Tres picos de tracemalloc por método/tamaño; mediana, salida incluida y entrada excluida. |
| F3-R07 | Acotar el cambio de ventaja mediante tamaños observados. | `resultados_iqr.json`; no extrapolar un punto exacto ni universal. |
| F3-R08 | Mantener F2 como productor y F3 como consumidor experimental. | Contrato de columnas, clave única y pruebas contra `marcar_iqr`. |
| F3-R09 | Conservar funciones sin estado y no forzar recursión. | Decisiones aprobadas en la rúbrica de la formativa. |
| F3-R10 | Normalizar solo alias Git con el mismo correo verificado. | `.mailmap`: BenjaAraya/Benjamin Araya y jguaicoortega/Jorge Guaico; sin reescritura de historia. |

El integrante que ejecute en Windows debe agregar una línea propia con fecha real, entorno,
tamaños, intervalo observado, resultado de pruebas y decisión adoptada. No basta añadir un nombre
al registro asistido. Los cambios de implementación posteriores requieren volver a ejecutar el notebook.

## Validación local — 2026-09-27

Responsable: Benjamín Araya.

Se ejecutó F3 en Windows con Python 3.12.0, pandas 3.0.5 y NumPy 2.5.3.
Se verificaron 541 órdenes, 61 extremos y 24 pruebas satisfactorias.

Para 541 valores, el tiempo mínimo por llamada fue de 35,14 µs con bucle
y 140,72 µs con pandas. La mediana del pico de memoria rastreada fue de
2,36 KiB y 7,62 KiB, respectivamente.

El bucle fue más rápido con 2.000 valores y pandas con 5.000.
El cambio observado queda acotado entre esos tamaños; no representa
un umbral exacto ni universal. Los tamaños mayores provienen de
réplicas para medir carga, no de nuevas órdenes de compra.

Decisión: preferir el bucle para este experimento con 541 valores por
su menor tiempo y memoria rastreada. Mantener ambas implementaciones
para comparar tamaños mayores, sin modificar el procesamiento de F2.