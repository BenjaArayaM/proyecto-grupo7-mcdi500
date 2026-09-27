# Arquitectura de la revisión de Formativa 3

## Decisión principal

Se conserva F2 como productor de datos y F3 como consumidor y experimento algorítmico.
F3 no absorbe las 17 funciones de `F2/src/preprocesamiento.py` ni copia su limpieza.
Esta separación evita cambiar retrospectivamente la preparación ya validada y permite
estudiar dos algoritmos sobre exactamente la misma entrada.

| Componente | Responsabilidad y contrato | Motivo de separarlo |
|---|---|---|
| `F2/src/preprocesamiento.py` | Original → una fila por OC, marcas, métricas y tablas | Las decisiones de moneda, duplicación y faltantes siguen teniendo un único responsable. |
| `F2/data/processed/ordenes.csv` | Interfaz entre fases: `codigoOC` único, monto finito en CLP y marca IQR | F3 reutiliza un producto del pipeline; no vuelve a limpiar el CSV original. |
| `F3/src/datos_iqr.py` | Localizar raíz, cargar y validar la interfaz | Los errores de datos se detectan antes del cronómetro; la E/S no contamina el costo de filtrar. |
| `F3/src/funciones_iqr.py` | Validar serie, calcular cuartiles/límites una sola vez, filtrar por bucle o pandas | Ambas estrategias comparten parámetros y devuelven listas equivalentes. Se evita duplicar Q1/Q3 en celdas. |
| `F3/src/benchmark_iqr.py` | Generar cargas repetidas y medir tiempo y memoria por separado | Cambiar repeticiones o tamaños no altera el criterio estadístico. |
| `F3/tests/test_funciones_iqr.py` | Casos normales, límites, errores e integración con F2 | Las funciones se verifican sin depender del estado de un notebook abierto. |
| Notebook F3 | Orquestación, gráficos, contraste e interpretación | La narrativa queda junto a evidencias; la lógica reutilizable permanece importable. |
| `F3/evidencias` y `F3/docs` | Pruebas, hash, versiones, muestras, tablas, figuras e informe | Permiten revisar qué código y datos produjeron cada resultado. |

## Evolución respecto de la entrega

La entrega tenía dos funciones de filtrado y cuartiles dentro del notebook. La revisión añade
validación de la entrada, lectura con contrato explícito, límites compartidos, instrumentación
reutilizable y pruebas ejecutables. Los cuerpos de los dos filtros se conservan para mantener
la comparación original aprobada. No se reemplaza pandas por NumPy para cambiar artificialmente
la conclusión de rendimiento.

F2 ya contiene `marcar_iqr`. F3 calcula los cuartiles con `Series.quantile` y contrasta límites y
marcas con F2 en una prueba de integración. Esa segunda implementación responde al objetivo
experimental; no es una segunda limpieza. Si se extrae una utilidad estadística común en el
futuro, se hará con pruebas de regresión en ambas fases. No se hace esa refactorización en esta
corrección porque modificaría innecesariamente una fase previa.

## Alternativas y consecuencias

- **Todo en el notebook:** facilita un prototipo, pero impide probar por separado los contratos y mezcla preparación con medición. Se descarta.
- **Copiar todo F2 dentro de F3:** crea dos versiones de reglas monetarias y de faltantes. Se descarta.
- **Funciones sin estado:** suficientes para la formativa y compatibles con las dos estrategias. Se mantienen; no se agrega una jerarquía de clases sin un requisito de estado.
- **Recursión:** no aporta al recorrido de una serie plana. Se reconsideraría ante una estructura jerárquica de profundidad desconocida.
- **Salida como lista:** conserva la API entregada, el orden y los repetidos. No preserva índices; la trazabilidad por OC se verifica adicionalmente con códigos y máscaras.

## Contratos y límites de validez

La serie numérica y finita se valida una vez, fuera del cronómetro. Los filtros reciben límites
finitos ordenados calculados por el módulo o fijados explícitamente por una prueba. Una serie vacía
con límites conocidos devuelve una lista vacía; una serie vacía para estimar cuartiles produce
`ValueError`. La igualdad con el límite no es atípica: se usan `<` y `>` estrictos.

Las 541 OC reales se conservan. Las series mayores son repeticiones para medir carga; no representan
nuevas compras ni deben utilizarse como ampliación de una muestra para modelar. No hay entrenamiento
ni separación train/test en esta formativa. Tampoco se toman tiempos como evidencia de calidad predictiva.
