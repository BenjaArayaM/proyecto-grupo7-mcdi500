# Sumativa 1 · Guía de trabajo del Grupo 7

**Git Bash + JupyterLab + LaTeX · Fases F1 y F2**

Esta guía parte de tu carpeta **proyecto-grupo7-mcdi500**, ya existente en el
Escritorio, y de tu entorno virtual instalado. Tú ejecutarás los comandos,
revisarás los cambios y harás cada commit y push.

La base descargable es un punto de partida preparado con asistencia. No es una
entrega aprobada ni acredita aportes de los cuatro integrantes. Se comprobó con el
CSV adjunto: 11.177 filas, 63 columnas y 541 órdenes. El código tiene 18 pruebas
exitosas; los notebooks conservaron 6 celdas de código ejecutadas en F1 y 12 en F2.
La validación utilizó ipykernel en memoria y Linux. Falta comprobar tu JupyterLab
en Windows y reconstruir el entorno acordado por el grupo.

## 1. Qué debes construir y en qué orden

La rúbrica asigna **99 puntos: 66 a código/notebooks, 21 al informe y 12 al repositorio**.
El trabajo debe concentrarse en código ejecutable y decisiones justificadas.

| Producto | Función | Archivo principal |
|---|---|---|
| F1 | Problema, objetivos, alcance, entorno y procedencia; sin limpiar registros | F1/notebooks/F1_Definicion.ipynb |
| F2 | Obtención, diagnóstico, preparación, transformación y validación | F2/notebooks/F2_Preprocesamiento.ipynb |
| Informe | Explicar qué se hizo, por qué y con qué evidencia | informe/informe.tex |
| Trazabilidad | Decisiones cuantificadas y contribuciones reales | docs/bitacora_decisiones.md e historial Git |

El mapa V2 se conserva en F1/docs y se conecta con el trabajo mediante
docs/vinculacion_mapa.md. F3 y F4 permanecen proyectadas.

## 2. Confirmar la carpeta correcta

En el Explorador de Windows, abre **proyecto-grupo7-mcdi500** y selecciona
**Open Git Bash here**. Ejecuta:

~~~bash
pwd
git status
git remote -v
~~~

El remoto debe ser BenjaArayaM/proyecto-grupo7-mcdi500. Si aparece “not a git
repository”, estás fuera de la carpeta correcta. Entra desde el Explorador;
no ejecutes git init otra vez.

Si git status muestra cambios tuyos, revísalos y guárdalos antes de cambiar de rama.
No uses reset --hard para limpiar la carpeta.

Con tu trabajo guardado y el repositorio limpio:

~~~bash
git switch main
git pull --ff-only
git switch -c sumativa1-benjamin
~~~

La rama nueva permite desarrollar y revisar antes de integrar en main.
Si ya creaste sumativa1-benjamin, usa git switch sumativa1-benjamin.
Los compañeros deben elegir ramas propias para tareas simultáneas.

**Nota sobre esta conversación:** se creó previamente la rama remota
sumativa1-f1-f2-base, apuntando al mismo commit que main. No recibió archivos ni
commits nuevos. Esta guía no depende de esa rama: los materiales se entregan
mediante descarga y tú realizarás las subidas.

## 3. Incorporar los archivos descargables

Descarga y extrae **Base_Sumativa1_Grupo7.zip** fuera del repositorio. Dentro
encontrarás la carpeta **para_copiar**. Copia su contenido a la raíz de
proyecto-grupo7-mcdi500, combinando las carpetas F1 y F2 con las existentes.

No copies una carpeta completa dentro de otra con el mismo nombre: la ruta debe
seguir siendo proyecto-grupo7-mcdi500/F1, no una estructura duplicada.

El paquete no incluye tu entorno virtual, la carpeta interna de Git, el
requirements.txt previo ni el original CSV. Se conservan tus instalaciones,
historial y mapa V2. Antes de reemplazar README, configuración o notebooks del
mismo nombre, compara las versiones y conserva fuera del repositorio una copia de
cualquier trabajo local que hayas modificado.

Los archivos preparados incluyen:

- Notebooks F1/F2 con narrativa y salidas de validación.
- Funciones Python, 18 pruebas y scripts de ejecución.
- Configuración con esquema, selección por código y hash del original.
- Bitácora, plan y matriz de los 15 criterios.
- Fuente LaTeX, referencias, tablas, figura y PDF técnico en borrador.

La lista concreta de archivos revisados antes del commit es tu evidencia de qué
incorporaste; no presentes el paquete completo como desarrollo original del grupo.

## 4. Activar y comprobar tu entorno

~~~bash
source .venv/Scripts/activate
python -c "import sys; print(sys.executable)"
python -m pip check
git config user.name
git config user.email
~~~

El intérprete debe terminar en **.venv/Scripts/python.exe**. El nombre y correo
Git deben corresponder a quien hace el trabajo; el correo debe estar asociado a
su cuenta de GitHub.

No reinstales todo si las dependencias ya funcionan. El requirements.txt existente
pertenece al entorno previo del equipo. requirements-validacion.txt documenta el
entorno de comprobación de la base; no declara que ambos sean iguales.
Si pip check informa incompatibilidades, resolverlas antes de afirmar que el
entorno está cerrado y reproducible.

### Conservar las salidas de los notebooks

El instructivo anterior activaba nbstripout. La nueva guía exige evidencia
visible en Git, por lo que hay que retirar ese filtro de este repositorio:

~~~bash
nbstripout --uninstall
git check-attr filter -- \
  F1/notebooks/F1_Definicion.ipynb \
  F2/notebooks/F2_Preprocesamiento.ipynb
~~~

filter debe aparecer como **unset** o **unspecified**. Si sigue apareciendo
nbstripout, revisar de dónde proviene; no desactivar configuraciones globales
sin conocer su efecto. Cada integrante debe comprobar su propia copia.

## 5. Copiar el CSV y verificar su integridad

Copia el adjunto completo a:

**F1/data/raw/187402OCCompraAgil.csv**

Solo cambia su nombre. No selecciones columnas en Excel ni vuelvas a guardarlo
desde Excel, porque cambiarías los bytes utilizados para verificar su procedencia.
Comprueba que no quede una extensión duplicada .csv.csv.

~~~bash
python scripts/verificar_original.py
~~~

Resultado esperado: **21.743.181 bytes** y “Integridad correcta”. El SHA-256 debe
coincidir con proyecto.json. El programa detiene la ejecución si el original cambia.

**Publicación de datos pendiente.** La revisión automática bloqueó el intento de
subir el CSV procesado por contener nombres y RUT de proveedores sin autorización
explícita. El paquete conserva el original y las tablas individuales fuera de
Git mediante .gitignore. Puedes trabajarlos localmente; no uses git add -f para
eludir esa exclusión. Para cerrar reproducibilidad y acceso del docente, el grupo
debe resolver una forma autorizada de compartir los insumos.

## 6. Primer commit: incorporar la base asistida

Este commit debe describir la incorporación del material de partida. Hazlo después
de revisar los archivos. Los comandos siguientes no incluyen el original ni las
tablas individuales:

~~~bash
git status --short
git add .gitignore .gitattributes README.md proyecto.json
git add requirements-validacion.txt
git add F1/src F1/notebooks/F1_Definicion.ipynb
git add F2/src F2/tests F2/notebooks
git add F2/docs/metricas.json F2/docs/perfil_original.csv
git add F2/docs/comparacion_faltantes.csv
git add F2/data/processed/parametros_transformacion.json
git add docs scripts evidencias informe
git diff --cached --stat
git diff --cached --name-only
python scripts/verificar_entrega.py --staged
~~~

Revisa esa lista antes de confirmar. Si contiene archivos ajenos a este avance,
retíralos del área preparada sin borrarlos del disco. Por ejemplo:

~~~bash
git restore --staged ruta/del/archivo
~~~

Cuando la selección sea correcta:

~~~bash
git commit -m \
  "chore(sumativa1): incorpora base asistida para revision del grupo"
git push -u origin sumativa1-benjamin
~~~

Estos comandos los ejecutas tú; no están ejecutados por esta guía. Si Git indica
“nothing to commit”, revisa el estado y no crees un commit vacío. Un push correcto
publica la rama de trabajo; todavía no la integra en main.

## 7. Desarrollar F1 desde JupyterLab

~~~bash
python -m jupyter lab
~~~

Mantén abierta esa ventana. En el navegador, abre
**F1/notebooks/F1_Definicion.ipynb** y selecciona **Python (grupo7-mcdi500)**.

Si el kernel no aparece, registra el que corresponde a tu .venv desde otra ventana
Git Bash, abierta en la raíz y con el entorno activo:

~~~bash
python -m ipykernel install --user \
  --name grupo7_mcdi500 --display-name "Python (grupo7-mcdi500)"
~~~

Revisa problema, objetivos y alcance con el equipo. No agregues limpieza ni
imputación en F1. Comprueba que los objetivos sean medibles y que las exclusiones
coincidan con lo que permite el archivo.

Usa **Kernel → Restart Kernel and Run All Cells** y guarda. El intérprete observado
debe ser tu .venv, no el entorno Linux de la validación inicial.

Para registrar también una ejecución automática, guarda primero tus cambios:

~~~bash
python scripts/ejecutar_notebooks.py \
  --fase F1 --kernel grupo7_mcdi500
~~~

El script actualiza el notebook y evidencias/ejecucion_F1.json. No lo ejecutes al
mismo tiempo que editas ese mismo archivo. Al volver a Jupyter, recarga la versión
guardada en disco si lo solicita.

Después de una revisión real de F1:

~~~bash
git add F1/notebooks/F1_Definicion.ipynb
git add evidencias/entorno_F1.json evidencias/ejecucion_F1.json
git add docs/bitacora_decisiones.md
git diff --cached --stat
python scripts/verificar_entrega.py --staged
git commit -m "docs(f1): revisa alcance y registra ejecucion local"
git push
~~~

Agrega F1/src o proyecto.json solo si realmente los modificaste y revisaste.

## 8. Desarrollar F2 con decisiones basadas en cifras

Abre **F2/notebooks/F2_Preprocesamiento.ipynb**. Lee y ejecuta en orden:
obtener, diagnosticar, decidir, transformar, validar y exportar.

La auditoría inicial encontró problemas concretos:

- **11.177 filas y 541 OC:** no sumar montos de cabecera por cada fila.
- **Faltantes por OC:** actividad en 139/541 y región en 8/541. El neto CLP
  no tiene faltantes; no corresponde imputarlo para mostrar una técnica.
- **Rubros:** 180 OC tienen más de un N1. No repetir el monto de una OC en
  cada rubro. La tabla puente expresa pertenencia.
- **Detalle:** tres OC no concilian al quedarse con firmas distintas.
  Borrar una fila idéntica en la OC 2427-264-AG25 perdería 1.000.000 CLP.
- **Extremos:** conservarlos y justificarlos. Los 60 del mapa y los 61 del
  diagnóstico del neto CLP usan variables y poblaciones diferentes.

El código y el informe explican qué está implementado y qué sigue abierto.
El equipo debe revisar el diccionario monetario, los estados incluidos, las tres
excepciones y la utilidad de las transformaciones.

Actualiza la bitácora con fecha real, responsable, decisión, motivo, cifras y
efecto. No escribas que una consulta a la fuente o una revisión ya ocurrió si
todavía no se ha realizado.

Al terminar cada avance:

~~~bash
python scripts/ejecutar_notebooks.py \
  --fase F2 --kernel grupo7_mcdi500
python -m unittest discover -s F2/tests -v
python scripts/verificar_entrega.py
~~~

Se esperan 18 pruebas satisfactorias en esta base. Si cambias una política,
actualiza las pruebas pertinentes con una justificación; no cambies el resultado
esperado solo para ocultar un fallo.

Commit de un avance real de F2:

~~~bash
git add F2/src F2/tests F2/notebooks/F2_Preprocesamiento.ipynb
git add F2/docs/metricas.json F2/docs/perfil_original.csv
git add F2/docs/comparacion_faltantes.csv
git add F2/data/processed/parametros_transformacion.json
git add evidencias/entorno_F2.json evidencias/ejecucion_F2.json
git add evidencias/pruebas_F2.json docs/bitacora_decisiones.md
git diff --cached --stat
python scripts/verificar_entrega.py --staged
git commit -m "feat(f2): documenta politica revisada y valida resultados"
git push
~~~

Adapta el mensaje a tu cambio concreto. El ejemplo no significa que la política
ya fue revisada por el grupo.

## 9. Redactar el informe LaTeX dentro de JupyterLab

En JupyterLab, abre **informe/informe.tex** con **Open With → Editor**.
Puedes editar el texto desde ahí. El PDF lo compila un programa LaTeX externo al
entorno virtual de Python.

Primero comprueba:

~~~bash
pdflatex --version
~~~

Si el comando no existe, instala MiKTeX para Windows desde su sitio oficial.
Reabre Git Bash después de instalarlo y activa .venv. No se instala con pip.
MiKTeX puede descargar paquetes faltantes durante la primera compilación.

En el .tex completa los comandos Docente y FechaEntrega. Confirma los nombres,
curso y formato institucional. Desarrolla la reflexión con decisiones propias
del equipo y revisa informe/referencias.tex: las fuentes docentes adjuntas no
incluyen autor/fecha explícitos y esos metadatos deben confirmarse.

Para regenerar tablas y compilar:

~~~bash
python scripts/compilar_informe.py
~~~

Se actualiza **informe/informe.pdf**, que puedes abrir con doble clic en JupyterLab.
Las cifras vienen del pipeline: no cambies a mano informe/tablas para que el PDF
muestre valores diferentes de los notebooks.

El script realiza tres pasadas de pdflatex para actualizar índice y referencias.
Si falla, revisa informe/informe.log. Conserva el estado de borrador hasta que el
grupo revise el texto y cierre los pendientes.

Después de una revisión real:

~~~bash
git add informe/informe.tex informe/referencias.tex
git add informe/tablas informe/figuras informe/informe.pdf
git add docs/bitacora_decisiones.md
git diff --cached --stat
git commit -m "docs(informe): integra decisiones y resultados revisados"
git push
~~~

La terminal integrada de Jupyter puede abrir PowerShell. Los comandos Python
funcionan allí, pero source y los bloques de esta guía están pensados para Git Bash.

## 10. Colaboración e integración en GitHub

Cada integrante debe tener acceso real y aportar desde su propia cuenta. Acuerden
responsables para F1/entorno, datos/diagnóstico, funciones/pruebas e informe/revisión.
No se asignan autores ni fechas ficticias y no se simula trabajo espaciando commits
vacíos. El desarrollo y las revisiones deben ocurrir durante el período de trabajo.

Después del primer push, abre tu repositorio en GitHub y elige **Compare & pull request**.
Configura base main y la rama de tu avance. Describe problema, cambio, evidencia
y pendientes. Puedes mantener el PR como borrador durante el desarrollo.
Un compañero debe revisar antes de que el grupo integre el cambio.

Ejemplos de evidencia de revisión: una corrección justificada, una prueba nueva
para un riesgo detectado o una ejecución independiente con resultados comparables.
Copiar el paquete de partida no sustituye esos aportes.

Si push se rechaza porque la rama remota avanzó, no uses push --force. Guarda tu
trabajo, ejecuta git fetch origin y revisa la divergencia antes de integrar.
Eviten editar el mismo notebook simultáneamente.

## 11. Comprobar que el avance llegó

~~~bash
git status
git log -5 --oneline
git log --format="%h | %an | %ad | %s" --date=short -10
~~~

En GitHub, selecciona la rama correcta y comprueba el commit y sus archivos.
Un repositorio local limpio no demuestra que se haya hecho push.
Verifica también las salidas de los notebooks en GitHub.

## 12. Cierre de la entrega

Utiliza docs/matriz_rubrica.md como lista de evidencias de los 15 criterios.
Antes de entregar:

- Ejecutar F1/F2 completos en Windows y reconstruir el entorno en otro equipo.
- Cerrar o delimitar formalmente las tres excepciones y la semántica monetaria.
- Resolver acceso autorizado al original para que el docente pueda reproducir.
- Confirmar commits y revisiones reales de los cuatro integrantes.
- Revisar portada, índice, redacción y al menos cinco referencias citadas:
  dos docentes, dos oficiales y una académica de los últimos cinco años.
- Mantener coherencia entre mapa, bitácora, notebooks, código e informe.
- Comprobar acceso del docente al repositorio y el nombre de entrega requerido.

No se puede garantizar la nota máxima con una plantilla: estos puntos requieren
evidencia real y una explicación que el grupo pueda defender.

## Fuentes de apoyo técnico

JupyterLab: edición de LaTeX y visualización de PDF.
https://jupyterlab.readthedocs.io/en/stable/user/file_formats.html

MiKTeX: instalación oficial para Windows.
https://miktex.org/howto/install-miktex

nbstripout: instalación y retirada del filtro del repositorio.
https://github.com/kynan/nbstripout#using-as-a-git-filter

Guía de desarrollo de la Sumativa 1, rúbrica de 99 puntos y mapa V2:
documentos adjuntos proporcionados por el equipo.
