import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress


carpeta = Path(__file__).resolve().parent
datos = pd.read_csv(carpeta.parent / "practica 1" / "anilist_limpio.csv")
total = len(datos)
datos = datos.dropna(subset=["popularidad", "favoritos"]).sort_values("popularidad")
resultados = carpeta / "resultados"
resultados.mkdir(exist_ok=True)

x = datos["popularidad"]
y = datos["favoritos"]
modelo = linregress(x, y)
ajuste = modelo.slope * x + modelo.intercept
r2 = modelo.rvalue ** 2

for nombre in ["dispersion", "modelo_lineal"]:
    plt.figure(figsize=(8, 5))
    plt.scatter(x, y, s=12, alpha=0.4, label="datos")
    if nombre == "modelo_lineal":
        plt.plot(x, ajuste, color="red", label=f"recta, r^2 = {r2:.4f}")
        plt.axhline(y.mean(), color="green", linestyle="--", label="promedio")
    plt.title("popularidad y favoritos")
    plt.xlabel("popularidad")
    plt.ylabel("favoritos")
    plt.legend()
    plt.tight_layout()
    plt.savefig(resultados / f"{nombre}.png", dpi=150)
    plt.close()

reporte = f"""# reporte de resultados

se uso el dataset limpio de anilist para estudiar la relacion entre popularidad y favoritos
se analizaron {len(datos)} anime y se excluyeron {total - len(datos)} filas sin esos datos

- x: popularidad, cantidad de usuarios que tienen el anime en su lista
- y: favoritos, cantidad de usuarios que lo marcaron como favorito
- modelo por minimos cuadrados: favoritos = {modelo.slope:.6f} * popularidad + ({modelo.intercept:.4f})
- correlacion de pearson: {modelo.rvalue:.4f}
- r^2: {r2:.4f}

la relacion es positiva: los anime con mayor popularidad tienden a tener mas favoritos
el modelo explica el {r2 * 100:.2f}% de la variacion de favoritos en los datos usados
esta relacion no demuestra que una variable cause la otra

`dispersion.png` muestra los datos; `modelo_lineal.png` agrega la recta y el promedio de favoritos
"""
(resultados / "reporte_resultados.md").write_text(reporte, encoding="utf-8")
print(f"modelo terminado, r^2 = {r2:.4f}")
