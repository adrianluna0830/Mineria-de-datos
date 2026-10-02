import pandas as pd
from pathlib import Path
from scipy.stats import kruskal, shapiro


carpeta = Path(__file__).resolve().parent
datos = pd.read_csv(carpeta.parent / "practica 1" / "anilist_limpio.csv")
total = len(datos)
datos = datos.dropna(subset=["formato", "calificacion"])
datos["formato"] = datos["formato"].str.lower()
resultados = carpeta / "resultados"
resultados.mkdir(exist_ok=True)
alfa = 0.05

resumen = datos.groupby("formato")["calificacion"].agg(["count", "mean", "median"])
resumen.columns = ["cantidad", "media", "mediana"]
resumen.round(2).to_csv(resultados / "resumen_por_formato.csv")

normalidad = []
grupos = []
for formato, grupo in datos.groupby("formato"):
    calificaciones = grupo["calificacion"]
    grupos.append(calificaciones)
    estadistico, valor_p = shapiro(calificaciones)
    resultado = "no se rechaza normalidad"
    if valor_p < alfa:
        resultado = "se rechaza normalidad"
    normalidad.append([formato, estadistico, valor_p, resultado])

normalidad = pd.DataFrame(normalidad, columns=["formato", "estadistico_w", "valor_p", "resultado"])
normalidad.to_csv(resultados / "normalidad_por_formato.csv", index=False)
rechazos = (normalidad["valor_p"] < alfa).sum()
estadistico, valor_p = kruskal(*grupos)
conclusion = "no se rechaza h0, no hay evidencia de diferencias entre formatos"
if valor_p < alfa:
    conclusion = "se rechaza h0, hay diferencias entre al menos dos formatos"

reporte = f"""# reporte de resultados

se comparo la calificacion de {len(datos)} anime en {len(grupos)} formatos mediante kruskal-wallis.
se excluyeron {total - len(datos)} filas sin formato o calificacion.

primero se aplico shapiro-wilk por formato, con h0 de que las calificaciones siguen una distribucion normal.
se rechazo la normalidad en {rechazos} de {len(grupos)} formatos con nivel de significancia {alfa}.
por eso se uso kruskal-wallis para comprobar las diferencias entre formatos.
los resultados de normalidad estan en `normalidad_por_formato.csv`.

- h0: la distribucion de calificaciones es igual en todos los formatos.
- h1: al menos un formato tiene una distribucion diferente.
- nivel de significancia: {alfa}.
- estadistico h: {estadistico:.4f}.
- valor p: {valor_p:.4e}.

{conclusion}.

se consideran independientes las observaciones y cada anime pertenece a un solo formato.
la prueba no requiere suponer una distribucion normal y no identifica cuales formatos difieren.
el resumen por formato esta en `resumen_por_formato.csv`.
"""
(resultados / "reporte_resultados.md").write_text(reporte, encoding="utf-8")
print("pruebas terminadas")
