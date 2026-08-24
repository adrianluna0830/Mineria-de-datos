import pandas as pd


def limpiar_anime():
    datos = pd.read_csv("anilist_raw.csv")
    datos = datos.drop_duplicates(subset="id")
    datos["fecha_inicio"] = pd.to_datetime(datos["fecha_inicio"], errors="coerce")
    datos = datos.dropna(subset=["titulo", "fecha_inicio"])
    columnas = ["episodios", "duracion", "calificacion", "popularidad", "favoritos"]
    for columna in columnas:
        datos[columna] = pd.to_numeric(datos[columna], errors="coerce")
    datos.to_csv("anilist_limpio.csv", index=False)
    print("archivo anilist_limpio.csv creado con", len(datos), "filas")


limpiar_anime()
