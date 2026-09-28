"""Genera tablas desde métricas verificadas y compila el informe con XeLaTeX.

Requiere TeX Live/MiKTeX, ajeno al entorno virtual de Python. No modifica Git.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
from verificar_formativa3 import verificar

RAIZ = Path(__file__).resolve().parents[1]


def escapar(texto):
    tabla = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
             '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}'}
    return ''.join(tabla.get(c, c) for c in str(texto))


def numero(valor, decimales=2):
    return f'{valor:,.{decimales}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def main():
    r = verificar()
    carpeta = RAIZ/'F3/docs'
    programa = shutil.which('xelatex')
    if programa is None:
        raise SystemExit('No se encontró xelatex. Complete TeX Live y abra de nuevo Git Bash.')
    pares = {n: {f['metodo']: f for f in r['benchmark'] if f['n']==n}
             for n in sorted({f['n'] for f in r['benchmark']})}
    nativo = pares[r['entrada']['filas']]
    cruces = r['cruces']['intervalos_observados']
    if cruces:
        texto_cruce = '; '.join(f"entre {numero(c['ultimo_n_bucle_no_mas_lento'],0)} y {numero(c['primer_n_pandas_mas_rapido'],0)} valores" for c in cruces)
    else:
        texto_cruce = 'no se observó un paso de ventaja del bucle a pandas entre tamaños consecutivos'
    macros = {'Contexto': r['contexto'], 'Sistema': r['entorno']['sistema'],
              'VersionPython': r['entorno']['python'], 'VersionPandas': r['entorno']['paquetes']['pandas'],
              'VersionNumpy': r['entorno']['paquetes']['numpy'], 'FechaUTC': r['fecha_utc'][:10],
              'NumeroPruebas': r['pruebas']['pruebas'], 'Ganador': r['ganador_nativo'],
              'IntervaloCruce': texto_cruce, 'HashDatos': r['entrada']['sha256'],
              'TiempoBucleNativo': numero(nativo['bucle']['min_por_llamada_us']),
              'TiempoPandasNativo': numero(nativo['pandas']['min_por_llamada_us'])}
    barra = chr(92)
    texto = '\n'.join(f'{barra}newcommand{{{barra}{nombre}}}{{{escapar(valor)}}}' for nombre,valor in macros.items())+'\n'
    (carpeta/'datos_resultados.tex').write_text(texto, encoding='utf-8')
    filas = [r'\begin{tabular}{rrrrr}',r'\toprule',
             r'Valores & Bucle ($\mu$s) & pandas ($\mu$s) & Bucle (KiB) & pandas (KiB) \\',r'\midrule']
    for n, par in pares.items():
        b,p = par['bucle'],par['pandas']
        vals=[numero(n,0),numero(b['min_por_llamada_us']),numero(p['min_por_llamada_us']),
              numero(b['mediana_pico_bytes']/1024),numero(p['mediana_pico_bytes']/1024)]
        filas.append(' & '.join(vals)+r' \\')
    filas += [r'\bottomrule',r'\end{tabular}']
    (carpeta/'tabla_benchmark.tex').write_text('\n'.join(filas)+'\n',encoding='utf-8')
    for pasada in range(3):
        proceso = subprocess.run([programa, '-interaction=nonstopmode', '-halt-on-error',
                                  '-file-line-error', 'f3_s02_grupo7.tex'], cwd=carpeta,
                                 capture_output=True, text=True, encoding='utf-8', errors='replace')
        if proceso.returncode:
            print(proceso.stdout[-6000:])
            raise SystemExit('Error de LaTeX. Consulte F3/docs/f3_s02_grupo7.log.')
        print(f'LaTeX: pasada {pasada+1}/3 correcta.')
    pdf=carpeta/'f3_s02_grupo7.pdf'
    log=(carpeta/'f3_s02_grupo7.log').read_text(encoding='utf-8',errors='replace')
    fuente='Arial' if 'FUENTE-INFORME: Arial' in log else 'Nimbus Sans (sustitución de revisión)'
    evidencia={'contexto':r['contexto'],'sha256_resultados':hashlib.sha256((carpeta/'resultados_iqr.json').read_bytes()).hexdigest(),
               'sha256_fuente_tex':hashlib.sha256((carpeta/'f3_s02_grupo7.tex').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
               'sha256_pdf':hashlib.sha256(pdf.read_bytes()).hexdigest(),'motor':'xelatex','pasadas':3,'fuente':fuente}
    (RAIZ/'F3/evidencias/compilacion_informe.json').write_text(json.dumps(evidencia,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('PDF actualizado: F3/docs/f3_s02_grupo7.pdf')
    print('Fuente:', fuente)


if __name__ == '__main__': main()
