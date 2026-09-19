import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


carpeta = Path(__file__).resolve().parent
archivo = carpeta.parent / "practica 1" / "anilist_limpio.csv"
resultados = carpeta / "resultados"


def guardar(nombre):
    plt.tight_layout()
    plt.savefig(resultados / nombre, dpi=150)
    plt.close()


def visualizar():
    datos = pd.read_csv(archivo)
    resultados.mkdir(exist_ok=True)

    formatos = datos["formato"].value_counts()
    formatos.index = formatos.index.str.lower()
    formatos.plot.pie(autopct="%1.1f%%", ylabel="")
    plt.title("porcentaje de anime por formato")
    guardar("pastel_formatos.png")

    for columna in ["calificacion", "episodios", "duracion"]:
        datos[columna].dropna().plot.hist(bins=20, edgecolor="black")
        plt.title("histograma de " + columna)
        plt.xlabel(columna)
        plt.ylabel("frecuencia")
        guardar("histograma_" + columna + ".png")

    for columna in ["calificacion", "popularidad", "favoritos"]:
        datos[columna].dropna().plot.box()
        plt.title("diagrama de caja de " + columna)
        guardar("caja_" + columna + ".png")

    datos.plot.scatter(x="calificacion", y="popularidad", alpha=0.4)
    plt.title("calificacion y popularidad")
    guardar("dispersion_calificacion_popularidad.png")

    generos = datos["generos"].dropna().str.split("|").explode().value_counts().head(10)
    generos.index = generos.index.str.lower()
    generos.plot.bar()
    plt.title("diez generos mas comunes")
    plt.xlabel("genero")
    plt.ylabel("cantidad")
    guardar("barras_generos.png")

    años = pd.to_datetime(datos["fecha_inicio"]).dt.year.value_counts().sort_index()
    años.plot.line()
    plt.title("anime por año")
    plt.xlabel("año")
    plt.ylabel("cantidad")
    guardar("linea_anime_por_año.png")

    print("graficas creadas")


visualizar()
