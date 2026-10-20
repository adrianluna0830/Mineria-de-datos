import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


carpeta = Path(__file__).resolve().parent
datos = pd.read_csv(carpeta.parent / "practica 1" / "anilist_limpio.csv")
total = len(datos)
datos = datos.dropna(subset=["episodios", "duracion"])[["id", "episodios", "duracion"]].copy()
resultados = carpeta / "resultados"
resultados.mkdir(exist_ok=True)
escala = StandardScaler()
x = escala.fit_transform(datos[["episodios", "duracion"]])

evaluacion = []
mejor_silueta = -1
for k in range(2, 7):
    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    grupos = modelo.fit_predict(x)
    silueta = silhouette_score(x, grupos)
    evaluacion.append([k, modelo.inertia_, silueta])
    if silueta > mejor_silueta:
        mejor_modelo = modelo
        mejor_silueta = silueta

evaluacion = pd.DataFrame(evaluacion, columns=["k", "inercia", "silueta"])
evaluacion.to_csv(resultados / "evaluacion.csv", index=False)
datos["grupo"] = mejor_modelo.labels_
datos.to_csv(resultados / "grupos.csv", index=False)
resumen = datos.groupby("grupo").agg(
    cantidad=("id", "count"),
    episodios_promedio=("episodios", "mean"),
    duracion_promedio=("duracion", "mean"),
)
resumen.round(2).to_csv(resultados / "resumen_grupos.csv")

plt.figure(figsize=(8, 5))
for numero, grupo in datos.groupby("grupo"):
    plt.scatter(grupo["episodios"], grupo["duracion"], s=12, alpha=0.4, label=f"grupo {numero}")
centros = escala.inverse_transform(mejor_modelo.cluster_centers_)
plt.scatter(centros[:, 0], centros[:, 1], marker="x", s=100, color="black", label="centroides")
plt.title(f"k-means: {mejor_modelo.n_clusters} grupos")
plt.xlabel("episodios")
plt.ylabel("duracion en minutos")
plt.legend()
plt.tight_layout()
plt.savefig(resultados / "agrupamiento.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 4))
for posicion, metrica in enumerate(["inercia", "silueta"], start=1):
    plt.subplot(1, 2, posicion)
    plt.plot(evaluacion["k"], evaluacion[metrica], marker="o")
    plt.title(metrica)
    plt.xlabel("cantidad de grupos")
    plt.ylabel(metrica)
    plt.xticks(evaluacion["k"])
plt.tight_layout()
plt.savefig(resultados / "evaluacion.png", dpi=150)
plt.close()

reporte = f"""# reporte de resultados

se agruparon {len(datos)} anime usando episodios y duracion; se excluyeron {total - len(datos)} filas sin esos datos
se ajusto la escala de ambas variables y se probaron de dos a seis grupos con k-means
el modelo uso la semilla 42 y diez inicializaciones por cada valor de k

- grupos elegidos: {mejor_modelo.n_clusters}
- silueta: {mejor_silueta:.4f}
- inercia: {mejor_modelo.inertia_:.4f}

se eligio el modelo con mayor silueta entre los valores probados
la silueta va de -1 a 1; valores cercanos a 1 indican grupos compactos y separados
la inercia suma las distancias al cuadrado de los datos a sus centroides, usando la escala ajustada
la inercia suele bajar al agregar grupos, por eso se uso la silueta para elegir k

el grupo {resumen['episodios_promedio'].idxmax()} tiene mas episodios en promedio y el grupo {resumen['duracion_promedio'].idxmax()} tiene mayor duracion en promedio
los grupos tienen tamaños distintos: el mas grande contiene {resumen['cantidad'].max()} anime y el mas pequeño {resumen['cantidad'].min()}
los numeros de grupo solo los identifican; se agrupo sin usar las etiquetas de formato
`resumen_grupos.csv` contiene la cantidad y los promedios de cada grupo en sus unidades originales
`agrupamiento.png` muestra los grupos y sus centroides; `evaluacion.png` compara inercia y silueta
"""
(resultados / "reporte_resultados.md").write_text(reporte, encoding="utf-8")
print(f"agrupamiento terminado, grupos = {mejor_modelo.n_clusters}, silueta = {mejor_silueta:.4f}")
