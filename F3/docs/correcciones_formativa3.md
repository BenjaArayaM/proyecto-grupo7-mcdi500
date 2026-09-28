# Correspondencia entre retroalimentación y correcciones

Evaluación recibida: **53/69**. Los 16 puntos faltantes se distribuyen entre los criterios
evaluados. La siguiente tabla documenta las acciones realizadas, sus evidencias y los aspectos
que permanecen pendientes de revisión final. No constituye una recalificación automática.

| Criterio | Puntaje recibido | Corrección realizada | Evidencia y estado |
|---|---:|---|---|
| Portada e índice | 3/3 | Se conservan identificación, integrantes y estructura del informe. | `F3/docs/f3_s02_grupo7.tex`; pendiente de validación visual del PDF final. |
| Codificación y arquitectura básica | 6/9 | Carga, validación, cálculo de límites y medición se separan en módulos reutilizables. | `datos_iqr.py`, `funciones_iqr.py` y `benchmark_iqr.py`; ejecución integrada validada. |
| Preprocesamiento | 6/6 | F2 se mantiene como productor de datos y F3 consume la salida procesada sin repetir su limpieza. | 541 OC procesadas; integración F2 → F3 validada. |
| Validación | 4/6 | Se incorporan pruebas automatizadas para casos normales, límites, entradas inválidas y estrategias de faltantes. | `F3/tests/test_funciones_iqr.py`; **24 pruebas ejecutadas, 0 fallos**. |
| Eficiencia | 4/6 | Se mantiene la comparación entre filtrado por bucle y vectorizado, incorporando medición de tiempo y memoria. | `benchmark_iqr.py`, resultados de las muestras y notebook F3; pendiente revisión final de resultados y explicación del punto de cruce. |
| Modularidad y robustez | 4/6 | Se separan responsabilidades mediante módulos y clases, con contratos explícitos y estrategias de faltantes. | `F3/docs/arquitectura.md`; arquitectura F2 → F3 documentada y pruebas ejecutadas. |
| Diseño estructurado | 6/6 | Se conserva la justificación de utilizar funciones estadísticas simples para el núcleo experimental IQR y se documentan las alternativas consideradas. | `F3/docs/arquitectura.md`; decisiones y consecuencias documentadas. |
| Documentación de arquitectura | 4/6 | Se amplía la documentación para justificar responsabilidades, estado, herencia, polimorfismo y patrón Strategy. | `F3/docs/arquitectura.md`; corrección incorporada y versionada en Git. |
| Repositorio | 4/6 | Se incorporan pruebas, evidencias de ejecución, documentación de arquitectura y actualización del README. | `F3/evidencias/`, README y commits específicos; pendiente revisión final de participación e índice documental. |
| Notebook | 6/6 | Se reorganiza la ejecución y se conserva la narrativa experimental junto con las evidencias de POO e integración. | `F3/notebooks/F3_Formativa_Eficiencia_IQR.ipynb`; **11 celdas de código, 0 errores**. |
| Formalidades | 6/9 | Se mantiene la estructura formal y se corrigen aspectos de redacción, referencias y trazabilidad técnica. | Fuente LaTeX e informe; pendiente compilación final y revisión visual. |

## Arquitectura orientada a objetos

La corrección incorpora una arquitectura POO en el pipeline de procesamiento de F3. Esta
arquitectura no reemplaza artificialmente el núcleo experimental IQR, donde las funciones
estadísticas sin estado son suficientes para comparar los algoritmos.

Se incorporan las clases `PipelineCompraAgil`, `TransformadorDatos`, `GeneradorMetricas` y
`ExportadorResultados`, junto con la jerarquía `EstrategiaFaltantes` y sus implementaciones
`EstrategiaEliminarOrden`, `EstrategiaImputarModa` y `EstrategiaConservarMarca`.

La implementación utiliza herencia y polimorfismo en las estrategias de tratamiento de faltantes,
mientras que la composición de responsabilidades permite mantener separado el flujo de
procesamiento, la generación de métricas y la exportación de resultados.

La relación entre fases se mantiene explícita: **F2 actúa como productor de datos procesados y
F3 como consumidor y núcleo experimental**. La integración fue ejecutada sobre los resultados
de F2, obteniendo:

- 541 órdenes procesadas.
- 1.683 relaciones de rubros.
- 541 variables generadas.
- 32 métricas generadas.

## Evidencias de validación

La revisión incorpora ejecución automatizada del conjunto de pruebas de F3:

- **24 pruebas ejecutadas.**
- **0 fallos.**
- Pruebas específicas para casos normales, todos los valores atípicos, ausencia de valores
  atípicos, límites, entradas inválidas e integración.
- Evidencia de ejecución reproducible mediante `F3/evidencias/ejecucion_formativa3.json`.
- Evidencia de pruebas mediante `F3/evidencias/pruebas_formativa3.json`.

El notebook fue ejecutado nuevamente mediante el script de ejecución de Formativa 3:

```text
F3: 11 celdas ejecutadas; 24 pruebas; sin errores.
```

## Reparación independiente de F2

La reparación realizada sobre archivos JSON de F2 se mantuvo independiente de las correcciones
de F3. El módulo de preprocesamiento F2 no fue modificado como parte de esta revisión.

Las 18 pruebas de F2 se mantienen como evidencia histórica de validación. La reparación sintáctica
de los archivos JSON no se presenta como una nueva ejecución local de F2.

## Alcance de las evidencias

Las evidencias de F3 permiten verificar la ejecución del código, las pruebas automatizadas, la
integración entre F2 y F3 y la arquitectura implementada. Los archivos de evidencia identifican
el entorno y los hashes correspondientes a la ejecución.

Los resultados de eficiencia deben interpretarse como mediciones experimentales sobre las cargas
utilizadas. La comparación no constituye evidencia de calidad predictiva ni implica entrenamiento
de modelos.

La corrección no asegura una recalificación determinada. Su objetivo es dejar trazables las
modificaciones realizadas frente a la retroalimentación recibida y facilitar la revisión del
entregable final.

## Pendientes antes de la entrega

Antes de cerrar la versión final se debe:

1. Ejecutar nuevamente los notebooks completos y comprobar que todas las celdas de código tengan
ejecución y salida.
2. Ejecutar las pruebas automatizadas y verificar que continúen sin fallos.
3. Revisar las versiones exactas del entorno utilizadas en la evidencia.
4. Revisar los resultados de eficiencia, incluyendo tiempo y memoria, y dejar explícita la
interpretación del costo fijo y del punto de cruce entre estrategias.
5. Compilar el informe LaTeX las veces necesarias para resolver referencias cruzadas.
6. Revisar visualmente tablas, nombres, numeración, figuras y referencias.
7. Realizar una última revisión ortográfica y de consistencia entre notebook, documentación,
evidencias e informe.
