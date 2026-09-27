# Reparación de JSON de F2 previa a la revisión F3

Base auditada: `c02beb597797d6eccb1cd562804d732e13c97f53`.

- `F2/notebooks/F2_Preprocesamiento.ipynb`: 13 bloques de conflicto. Doce contienen metadatos de ejecución y uno la duración del resumen de pruebas. Las fuentes de todas las celdas son iguales entre las dos variantes.
- `evidencias/entorno_F2.json`: un conflicto entre rutas de intérprete de Patricio y Alan.
- Se conserva `Updated upstream` en todos esos bloques. El notebook y el JSON vuelven a ser legibles y se mantiene un registro histórico coherente; no se inventa una ejecución nueva.
- No cambian `F2/src/preprocesamiento.py`, los parámetros de limpieza ni el original.
- El instalador crea un respaldo externo antes de copiar estos dos archivos; el usuario publica esta reparación en un commit separado.

Las 18 pruebas de F2 se ejecutaron satisfactoriamente en la copia de validación asistida Linux.
Los metadatos históricos de Windows que se restauran no pertenecen a esa ejecución asistida.
