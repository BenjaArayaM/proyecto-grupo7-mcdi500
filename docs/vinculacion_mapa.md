# Del mapa V2 a una implementación verificable

Mapa: F1/docs/Mapa_conceptual_Grupo7_V2.pdf y su archivo editable PPTX.
Se conserva la secuencia y se adaptan sus rutas genéricas a la estructura F1–F4.

| Elemento del mapa | Estado en Sumativa 1 | Evidencia exacta |
|---|---|---|
| Pregunta: montos por proveedores, rubros y mes | Definida; respuesta sustantiva posterior | F1/notebooks/F1_Definicion.ipynb, §§1–3 |
| Datos originales / adquisición | Lectura e integridad implementadas; commit del original pendiente en la base remota | F1/src/entorno.py; proyecto.json; F1/data/raw/187402OCCompraAgil.csv |
| Exploración con Jupyter y pandas | Implementada con salidas | F2/notebooks/F2_Preprocesamiento.ipynb, §§2–3 |
| Limpieza y conversiones con Python/pandas | Implementada sin sobrescribir el original | F2/src/preprocesamiento.py: preparar_ordenes |
| Datos procesados | Generados por código, separados de raw | F2/data/processed/ordenes.csv; relacion_orden_rubro.csv |
| NumPy: indicadores y transformaciones | IQR y Z implementados, parámetros guardados | F2/src/preprocesamiento.py: marcar_iqr, estandarizar |
| Rubros N1–N3 | Ruta jerárquica conservada | F2/data/processed/relacion_orden_rubro.csv |
| Proveedores escritos de formas distintas | Riesgo comprobado; 0 RUT con varios nombres normalizados en esta copia | F2/docs/metricas.json |
| Valores faltantes | Diagnóstico y política implementados | F2/docs/comparacion_faltantes.csv; notebook §5 |
| Montos atípicos | Marcados y conservados | F2/docs/metricas.json; notebook §8 |
| Git versiona la limpieza | Código y documentación listos para commits de desarrollo | F2/src; docs/bitacora_decisiones.md; historial Git |
| GitHub integra y revisa | Proyectado: el usuario hará commits, push y PR; colaboración de cuatro pendiente | URL del repositorio y docs/inicio_gitbash.md |
| Jupyter documenta la exploración | Implementado | F1 y F2 notebooks con salidas |
| Visualización | Figura diagnóstica implementada; gráficos de negocio proyectados | F2/src/informe.py; informe/figuras/faltantes_oc.pdf |
| Reporte técnico | Borrador LaTeX y PDF | informe/informe.tex; informe/informe.pdf |
| F3/F4 | Proyectadas según futuras guías | Carpetas F3/F4 existentes, sin afirmar ejecución |

## Ajustes al mapa sustentados en datos

- 11.177 filas no son 11.177 OC: se validan 541 cabeceras.
- Proveedores variantes es un riesgo a comprobar, no un hallazgo confirmado.
- Existen 53/191/487 etiquetas en N1/N2/N3 y 180 OC con más de un N1. La pertenencia
  a un rubro no permite repetir el importe de la OC en cada categoría.
- Los 60 extremos del mapa corresponden a MontoTotalOC de 536 OC CLP. La variable
  propuesta para el pipeline es MontoNetoOC_CLP de las 541 OC y marca 61 extremos.
  No son conteos contradictorios: variable y denominador quedan documentados.
- Se detectaron 6 filas idénticas adicionales; no se borran indiscriminadamente.
  La conciliación de firmas deja tres excepciones explícitas.

La tabla prueba la implementación de lo pertinente en F1/F2 y distingue las tareas
futuras, tal como solicita la guía.
