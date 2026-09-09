import pandas as pd
from pathlib import Path


carpeta = Path(__file__).resolve().parent
archivo = carpeta.parent / "practica 1" / "anilist_limpio.csv"
resultados = carpeta / "resultados"
modelo = resultados / "modelo_relacional"


def separar(datos, columna, nombre):
    tabla = datos[["id", columna]].dropna().copy()
    tabla[columna] = tabla[columna].str.split("|")
    tabla = tabla.explode(columna)
    tabla[columna] = tabla[columna].str.strip()
    tabla = tabla[tabla[columna] != ""]
    return tabla.rename(columns={"id": "anime_id", columna: nombre}).drop_duplicates()


def agrupar(datos, columna):
    datos = datos.copy()
    datos[columna] = datos[columna].fillna("sin_dato")
    tabla = datos.groupby(columna).agg(
        cantidad_anime=("id", "nunique"),
        calificaciones_disponibles=("calificacion", "count"),
        calificacion_media=("calificacion", "mean"),
        calificacion_mediana=("calificacion", "median"),
        calificacion_desviacion=("calificacion", "std"),
        calificacion_minima=("calificacion", "min"),
        calificacion_maxima=("calificacion", "max"),
        episodios_promedio=("episodios", "mean"),
        duracion_promedio=("duracion", "mean"),
        popularidad_promedio=("popularidad", "mean"),
        popularidad_total=("popularidad", "sum"),
        favoritos_promedio=("favoritos", "mean"),
        favoritos_total=("favoritos", "sum"),
    )
    return tabla.round(2).reset_index().sort_values("cantidad_anime", ascending=False)


def analizar():
    datos = pd.read_csv(archivo, parse_dates=["fecha_inicio"])
    resultados.mkdir(exist_ok=True)
    modelo.mkdir(exist_ok=True)

    numericas = ["episodios", "duracion", "calificacion", "popularidad", "favoritos"]
    estadistica = datos[numericas].agg(
        ["count", "mean", "median", "min", "max", "sum", "var", "std", "skew", "kurt"]
    ).T
    estadistica["mode"] = [datos[columna].mode().iloc[0] for columna in numericas]
    estadistica["null"] = datos[numericas].isna().sum()
    estadistica = estadistica.rename(
        columns={
            "count": "conteo",
            "mean": "media",
            "median": "mediana",
            "mode": "moda",
            "min": "minimo",
            "max": "maximo",
            "sum": "sumatoria",
            "var": "varianza_muestral",
            "std": "desviacion_estandar_muestral",
            "skew": "asimetria",
            "kurt": "curtosis_exceso",
            "null": "nulos",
        }
    )
    orden = [
        "conteo", "nulos", "media", "mediana", "moda", "minimo", "maximo",
        "sumatoria", "varianza_muestral", "desviacion_estandar_muestral",
        "asimetria", "curtosis_exceso",
    ]
    estadistica[orden].round(4).rename_axis("variable").to_csv(
        resultados / "estadistica_numerica.csv"
    )

    calidad = pd.DataFrame({
        "columna": datos.columns,
        "tipo": datos.dtypes.astype(str).values,
        "total_filas": len(datos),
        "no_nulos": datos.notna().sum().values,
        "nulos": datos.isna().sum().values,
        "porcentaje_nulos": (datos.isna().mean().values * 100).round(2),
        "valores_unicos": datos.nunique().values,
    })
    calidad.to_csv(resultados / "resumen_calidad.csv", index=False)

    categorias = []
    for columna in ["formato", "estado"]:
        conteos = datos[columna].value_counts()
        categorias.append({
            "variable": columna,
            "conteo": datos[columna].count(),
            "nulos": datos[columna].isna().sum(),
            "valores_unicos": datos[columna].nunique(),
            "moda": conteos.index[0],
            "frecuencia_moda": conteos.iloc[0],
            "porcentaje_moda": round(conteos.iloc[0] / datos[columna].count() * 100, 2),
        })
    pd.DataFrame(categorias).to_csv(resultados / "estadistica_categorica.csv", index=False)

    datos["año"] = datos["fecha_inicio"].dt.year
    generos = separar(datos, "generos", "genero")
    estudios = separar(datos, "estudios", "estudio")

    por_formato = agrupar(datos, "formato")
    por_genero = agrupar(generos.merge(datos, left_on="anime_id", right_on="id"), "genero")
    tablas = {
        "formato": por_formato,
        "estado": agrupar(datos, "estado"),
        "año": agrupar(datos, "año"),
        "genero": por_genero,
        "estudio": agrupar(estudios.merge(datos, left_on="anime_id", right_on="id"), "estudio"),
    }
    for nombre, tabla in tablas.items():
        tabla.to_csv(resultados / f"metricas_por_{nombre}.csv", index=False)

    formatos = pd.DataFrame({"formato": sorted(datos["formato"].dropna().unique())})
    formatos.insert(0, "formato_id", range(1, len(formatos) + 1))
    estados = pd.DataFrame({"estado": sorted(datos["estado"].dropna().unique())})
    estados.insert(0, "estado_id", range(1, len(estados) + 1))
    tabla_generos = pd.DataFrame({"genero": sorted(generos["genero"].unique())})
    tabla_generos.insert(0, "genero_id", range(1, len(tabla_generos) + 1))
    tabla_estudios = pd.DataFrame({"estudio": sorted(estudios["estudio"].unique())})
    tabla_estudios.insert(0, "estudio_id", range(1, len(tabla_estudios) + 1))

    anime = datos.drop(columns=["generos", "estudios", "año"]).rename(columns={"id": "anime_id"})
    anime = anime.merge(formatos, on="formato", how="left").merge(estados, on="estado")
    anime = anime.drop(columns=["formato", "estado"])
    anime[["formato_id", "estado_id"]] = anime[["formato_id", "estado_id"]].astype(pd.Int64Dtype())

    entidades = {
        "anime": anime,
        "formato": formatos,
        "estado": estados,
        "genero": tabla_generos,
        "estudio": tabla_estudios,
        "anime_genero": generos.merge(tabla_generos, on="genero")[["anime_id", "genero_id"]],
        "anime_estudio": estudios.merge(tabla_estudios, on="estudio")[["anime_id", "estudio_id"]],
    }
    for nombre, tabla in entidades.items():
        tabla.to_csv(modelo / f"{nombre}.csv", index=False)

    calificacion = estadistica.loc["calificacion"]
    popularidad = estadistica.loc["popularidad"]
    mejor_formato = por_formato[por_formato["calificaciones_disponibles"] >= 30].nlargest(1, "calificacion_media").iloc[0]
    mejor_genero = por_genero[por_genero["calificaciones_disponibles"] >= 30].nlargest(1, "calificacion_media").iloc[0]
    mayor_nulo = calidad.nlargest(1, "porcentaje_nulos").iloc[0]
    reporte = f"""# reporte de resultados

se analizaron **{len(datos):,} anime** entre **{datos['fecha_inicio'].min().date()}** y **{datos['fecha_inicio'].max().date()}**.

- calificacion media: **{calificacion['media']:.2f}**.
- mediana de calificacion: **{calificacion['mediana']:.2f}**.
- desviacion estandar de calificacion: **{calificacion['desviacion_estandar_muestral']:.2f}**.
- asimetria de popularidad: **{popularidad['asimetria']:.2f}**.
- columna con mas nulos: **{mayor_nulo['columna']}**, con **{int(mayor_nulo['nulos'])}**.
- formato con mayor calificacion media: **{str(mejor_formato['formato']).lower()}**, con **{mejor_formato['calificacion_media']:.2f}**.
- genero con mayor calificacion media: **{str(mejor_genero['genero']).lower()}**, con **{mejor_genero['calificacion_media']:.2f}**.

las entidades son anime, formato, estado, genero y estudio. anime se relaciona con formato y estado, y tiene relaciones muchos a muchos con genero y estudio mediante anime_genero y anime_estudio. los datos faltantes se excluyeron de los calculos y no se reemplazaron con cero.
"""
    (resultados / "reporte_resultados.md").write_text(reporte, encoding="utf-8")
    print("analisis terminado")


analizar()
