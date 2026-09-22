# Aporte de Jorge Guaico Ortega al informe de la Formativa 3

## Codificación funcional y arquitectura básica

El avance inicial de la Fase 3 se desarrolló en el notebook
`F3/notebooks/F3_Formativa_Eficiencia_IQR.ipynb`. El flujo implementado
localiza automáticamente la raíz del repositorio, carga el archivo procesado
generado durante la Fase 2 y selecciona únicamente la variable
`MontoNetoOC_CLP`.

Esta organización separa la ubicación del proyecto, la carga de datos,
la validación de la variable y el cálculo estadístico. Las implementaciones
algorítmicas mediante bucle y operación vectorizada se incorporarán
posteriormente como funciones independientes en `F3/src/`.

## Preprocesamiento y transformación

El análisis utiliza `F2/data/processed/ordenes.csv`, generado durante la
Fase 2. No se repite la limpieza del archivo original ni se modifican los
resultados del pipeline anterior.

Para el análisis se seleccionó `MontoNetoOC_CLP`, correspondiente al monto
neto expresado en pesos chilenos. La columna se convirtió a formato numérico
con control de errores y se verificó la cantidad de valores válidos y
faltantes. La validación registró 541 observaciones, todas numéricas y sin
valores faltantes. Por ello, no fue necesario imputar ni eliminar registros.

## Validación técnica y verificación

Se verificó la existencia del archivo procesado y la disponibilidad de la
columna `MontoNetoOC_CLP`. También se mostraron las primeras observaciones,
el total de registros, los valores válidos y faltantes y las estadísticas
descriptivas principales.

Los resultados obtenidos fueron:

- Observaciones analizadas: 541.
- Valores válidos: 541.
- Valores faltantes: 0.
- Primer cuartil (Q1): 217.923 CLP.
- Tercer cuartil (Q3): 1.620.152 CLP.
- Rango intercuartílico (IQR): 1.402.229 CLP.
- Límite inferior: -1.885.420,50 CLP.
- Límite superior: 3.723.495,50 CLP.

Debido a que los montos analizados son positivos, los posibles valores
atípicos se concentrarán sobre el límite superior. Estos límites se utilizarán
en las implementaciones mediante bucle y vectorizada, permitiendo comparar
ambos procedimientos bajo condiciones equivalentes.

## Contribución individual

Jorge Guaico Ortega preparó la estructura inicial del notebook, la carga del
archivo procesado de F2, la validación de la variable analizada, las
estadísticas descriptivas y el cálculo e interpretación de los límites del
método IQR.