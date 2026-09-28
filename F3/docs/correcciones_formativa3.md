# Correspondencia entre retroalimentación y correcciones

Evaluación recibida: **53/69**. Los 16 puntos faltantes se reparten en siete criterios.
La siguiente tabla documenta acciones y evidencias, no una recalificación automática.

| Criterio | Puntaje recibido | Cambio preparado | Evidencia y revisión pendiente |
|---|---:|---|---|
| Portada e índice | 3/3 | Se conservan identificación, integrantes y los diez apartados; índice automático. | Revisar el PDF recompilado localmente. |
| Codificación y arquitectura básica | 6/9 | Carga/validación, cálculo de límites y medición pasan a módulos. | `datos_iqr.py`, `funciones_iqr.py`, `benchmark_iqr.py`; notebook los importa. |
| Preprocesamiento | 6/6 | Se mantiene F2 como entrada, sin eliminar ni imputar. | 541 OC, cero faltantes monetarios y 61 extremos conservados. |
| Validación | 4/6 | 24 pruebas, incluyendo los tres casos pedidos en ambos filtros. | `F3/tests/test_funciones_iqr.py`; JSON y log de pruebas. |
| Eficiencia | 4/6 | Siete tamaños; 1.000 llamadas × tres repeticiones; memoria separada. | CSV, todas las muestras JSON, gráfico y explicación del costo fijo. Repetir en Windows. |
| Modularidad y robustez | 4/6 | Contratos, casos inválidos y evolución explícita F2 → F3. | Arquitectura y pruebas; se conserva la decisión de no usar clases en la formativa. |
| Diseño estructurado | 6/6 | Se conserva la justificación de no usar recursión. | Notebook e informe corregido. |
| Documentación de arquitectura | 4/6 | Decisiones, alternativas y consecuencias concretas. | `F3/docs/arquitectura.md`. |
| Repositorio | 4/6 | Pruebas reales, README, `.mailmap` de alias comprobados. | El usuario debe aplicar el paquete, retirar el Word del índice y realizar commits/PR. |
| Notebook | 6/6 | Ejecución completa, salidas, narrativa y referencia original al foro. | Nueve celdas de código tras modularizar; contadores consecutivos y hash. Validación Windows pendiente. |
| Formalidades | 6/9 | Revisión de acentuación, concordancia y conectores; referencias pertinentes. | PDF y fuente LaTeX. Validación visual por el equipo tras compilar. |

## Reparación independiente de F2

En `main` c02beb5 había 13 bloques de conflicto dentro del JSON del notebook F2 y uno en
`evidencias/entorno_F2.json`. Los del notebook afectan metadatos temporales y una duración de
pruebas, no fuentes de celdas. Se conserva el lado `Updated upstream`, correspondiente al
registro histórico de Patricio, sin atribuirlo a una nueva ejecución. En el JSON se conserva
su intérprete junto al registro histórico. Las variantes anteriores permanecen en Git y en el
respaldo externo que genera el instalador.

El módulo de preprocesamiento F2 no cambia. Sus 18 pruebas pasaron en la comprobación asistida.
La reparación sintáctica no certifica por sí sola una nueva ejecución local de F2.

## Alcance de las evidencias

El paquete trae resultados de validación asistida en Linux, identificados como tales. No se
declaran revisión, autoría de commits ni ejecuciones Windows de integrantes que no ocurrieron.
Los resultados temporales y de memoria se regeneran en el equipo del grupo. No hay garantía
de obtener 69/69: falta su revisión, integración y la evaluación del profesor.
