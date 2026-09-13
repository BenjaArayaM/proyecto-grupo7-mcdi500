# Bitácora de decisiones

Fecha de esta base: 2026-09-13. Registro preparado con asistencia de Codex a partir
del adjunto y de ejecuciones reales en un entorno de validación Linux.
Las propuestas requieren revisión del grupo. No son decisiones aprobadas por los
cuatro integrantes ni intervenciones atribuidas a una persona que no las realizó.

Una fila por decisión. En futuras revisiones agregar fecha real, responsable,
evidencia y commit efectivo; no inventar identificadores de commit.

| ID | Decisión / estado | Evidencia cuantificada | Motivo e impacto |
|---|---|---|---|
| D01 | Implementada: preservar original por SHA-256 | 21.743.181 bytes; hash en proyecto.json; copia (2) igual a la copia anterior | Permite detectar cualquier edición; raw no se sobrescribe |
| D02 | Implementada: leer con ;, cp1252 y texto | 11.177 filas, 63 columnas | Preserva RUT/códigos y caracteres; conversiones solo en F2 |
| D03 | Implementada: proyectar cabecera tras validar constancia | 22 atributos; 541 OC únicas; 277 RUT proveedores | Impide sumar una OC por cada repetición de fila |
| D04 | Propuesta implementada: neto CLP de origen como medida comparable | 536 CLP, 2 USD, 2 UTM, 1 CLF; neto CLP sin faltantes | Evita mezclar monedas; confirmar diccionario y conversión de la fuente |
| D05 | Propuesta implementada: conservar estados y marcar habilitados | 537 Aceptada, 3 Recepcion Conforme, 1 Solicitud de Cancelacion; marca 540 OC | No borra información; confirmar alcance con el equipo |
| D06 | Propuesta implementada: conservar NA y añadir vista/indicador | Actividad: 2.695/11.177 filas, 139/541 OC; región: 150/11.177 filas, 8/541 OC | Eliminar por actividad dejaría 402 OC; por región 533; moda inventaría 139 u 8 atributos |
| D07 | Implementada: no convertir impuesto de ítem ausente en cero | 11.177/11.177 ausencias | No se interpreta ausencia como exención; no entra en cabecera |
| D08 | Implementada: normalizar RUT/nombre solo para comparar | 0 RUT con varios nombres normalizados; 277 RUT | No hay evidencia para fusionar proveedores por similitud |
| D09 | Implementada: puente OC–N1–N2–N3 sin importes | 1.683 relaciones; 53/191/487 etiquetas; 180 OC con varios N1; 1 etiqueta N2 con varios padres | Conserva jerarquía y evita doble imputación del total a rubros |
| D10 | Implementada: no borrar filas repetidas del original | 6 adicionales, 12 en grupos idénticos; 2.040/2.043 grupos OC-producto compatibles con producto de firmas | Repetición de relaciones no equivale automáticamente a registro erróneo |
| D11 | Abierta: reconstrucción monetaria del detalle | 538/541 OC concilian firmas a 1 CLP; diferencias de -1.000.000, -7.489 y -26.525 CLP | No se publica detalle definitivo ni reparto monetario por rubro; revisar OC 264, 511 y 543 |
| D12 | Propuesta implementada: marcar IQR y conservar extremos | Neto CLP: 61/541, umbral 3.723.495,50; mapa: total CLP 60/536, umbral 4.379.267,38 | Un extremo estadístico no prueba error; 0 montos recortados |
| D13 | Implementada: no imputar montos completos | 0 faltantes en neto CLP; varianza poblacional antes/después 2.326.586.109.020,78 CLP² | Media/mediana/grupo no se aplican sin necesidad |
| D14 | Propuesta implementada: vista transformada separada | 541 filas; Z, 7 columnas one-hot, tamaño ordinal; 56 sin clasificación | Conserva dinero original; no se declara modelo ni entrenamiento |
| D15 | Implementada: pruebas de riesgos | 18 casos exitosos; incluye fechas, contradicciones, límites y excepciones reales | Verificar pérdidas y fallos previstos antes de exportar |
| D16 | Implementada: cifras del informe desde código | Tablas, figura y métricas proceden de ejecutar_pipeline | Evita discrepancias de transcripción entre productos |
| D17 | Pendiente local: retirar filtro nbstripout | Guía exige contadores y salidas en F1/F2 | Verificar índice de Git, no solo la vista de Jupyter |
| D18 | Abierta: cierre del entorno grupal y aportes | Validación Linux; requirements previo Windows; dos commits históricos de Benjamín al iniciar esta revisión | Reconstruir versiones acordadas y registrar contribuciones de cuatro personas en tiempo real |
| D19 | Pendiente: autorización de publicación de registros individuales | Revisión automática rechazó subir ordenes.csv por contener nombres/RUT de proveedores | Se publican código, documentación y resultados agregados; original y tablas individuales permanecen locales |

No usar estas cifras si cambia el original sin repetir el diagnóstico. Las métricas
actualizadas se generan en F2/docs/metricas.json.

## Comprobación local de F1

| ID | Fecha | Responsable | Decisión y motivo | Evidencia |
|---|---|---|---|---|
| D20 | 2026-09-13 | Benjamin Araya | Validar F1 con el entorno virtual del proyecto para evitar mezclar instalaciones de Python. | Windows; Python 3.12.0; 6 celdas sin errores; 11.177 filas y 63 columnas; original intacto. |

## Comprobación local de F2

| ID | Fecha | Responsable | Decisión y motivo | Evidencia |
|---|---|---|---|--
| D21 | 2026-09-13 | Benjamin Araya | Ejecutar F2 desde un kernel nuevo para comprobar su reproducción local y conservar las excepciones detectadas. | 12 celdas; 18 pruebas satisfactorias; 541 OC; 3 excepciones de detalle documentadas; original intacto. |