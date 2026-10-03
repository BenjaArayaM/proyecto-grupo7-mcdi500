# Changelog del proyecto MCDI500

Este archivo resume los principales cambios del proyecto y complementa la trazabilidad registrada en `docs/bitacora_decisiones.md`.

| Fecha | Cambio | Justificación / impacto | Evidencia |
|---|---|---|---|
| 2026-09-15 | Validación local de F2 en un equipo Windows adicional. | Comprobar la reproducibilidad del pipeline y de las pruebas en un entorno distinto. | D24; `evidencias/entorno_F2.json`; 18 pruebas OK. |
| 2026-09-16 | Consolidación e integración de la versión validada de F2 en `main`. | Centralizar la versión aceptada por el equipo y mantener una base estable para las fases posteriores. | D28–D30; commits `70863d7` y `cf9ba6e`. |
| 2026-09-16 | Revisión de F3 con pruebas, benchmark y arquitectura modular. | Incorporar evidencia de eficiencia, límites IQR reutilizables y una estructura basada en responsabilidades separadas. | `F3/docs/benchmark_iqr.csv`, `F3/evidencias/`, `F3/docs/arquitectura.md`. |
| 2026-10-03 | Integración del análisis final de F4. | Responder la pregunta del proyecto mediante análisis por mes de envío, proveedor y rubro, reutilizando las salidas validadas de fases anteriores. | D31; commit `53a208e`; `F4/notebooks/F4_Analisis_Resultados.ipynb`. |
| 2026-10-03 | Reconstrucción monetaria por rubro con control de conciliación. | Evitar duplicar montos de cabecera entre categorías y excluir únicamente de esta desagregación las tres órdenes no conciliadas. | D32; 537 órdenes; cobertura 99,47%; reconstrucción 664.257.301 CLP. |
| 2026-10-03 | Incorporación de tres visualizaciones explicativas. | Vincular cada dimensión de la pregunta con una visualización diferenciada: línea mensual, barras horizontales por proveedor y composición por rubro al 100%. | D33; commit `53a208e`. |
| 2026-10-03 | Actualización de documentación de F4. | Alinear README, bitácora y changelog con el estado actual del proyecto. | `README.md`, `docs/bitacora_decisiones.md`, `docs/changelog.md`. |

## Impacto acumulado

- **Modularidad:** F4 reutiliza el pipeline validado de F2 y la arquitectura de F3 sin crear una lógica paralela de preparación.
- **Rendimiento:** F3 documenta la comparación entre implementación iterativa y vectorizada y conserva evidencia de tiempo y memoria.
- **Reproducibilidad:** se mantienen notebooks ejecutados, pruebas automatizadas, dependencias versionadas y registros de entorno.
- **Documentación:** README, bitácora y changelog relacionan decisiones, resultados y evidencia verificable en Git.