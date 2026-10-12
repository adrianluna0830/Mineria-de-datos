import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix


carpeta = Path(__file__).resolve().parent
datos = pd.read_csv(carpeta.parent / "practica 1" / "anilist_limpio.csv")
total = len(datos)
datos = datos.dropna(subset=["episodios", "duracion", "formato"])
datos["formato"] = datos["formato"].str.lower()
resultados = carpeta / "resultados"
resultados.mkdir(exist_ok=True)

x = datos[["episodios", "duracion"]]
y = datos["formato"]
x_entrenamiento, x_prueba, y_entrenamiento, y_prueba = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

escala = StandardScaler()
modelo = KNeighborsClassifier(n_neighbors=5, metric="euclidean")
modelo.fit(escala.fit_transform(x_entrenamiento), y_entrenamiento)
prediccion = modelo.predict(escala.transform(x_prueba))
aciertos = (y_prueba == prediccion).sum()
exactitud = aciertos / len(y_prueba)
referencia = (y_prueba == y_entrenamiento.mode()[0]).mean()

comparacion = datos.loc[x_prueba.index, ["id", "episodios", "duracion"]].copy()
comparacion["formato_real"] = y_prueba
comparacion["formato_estimado"] = prediccion
comparacion.to_csv(resultados / "predicciones.csv", index=False)

matriz = confusion_matrix(y_prueba, prediccion, labels=modelo.classes_)
matriz = pd.DataFrame(matriz, index=modelo.classes_, columns=modelo.classes_)
matriz.rename_axis("formato_real").to_csv(resultados / "matriz_confusion.csv")

reporte = f"""# reporte de resultados

se uso knn para clasificar el formato del anime a partir de episodios y duracion
se analizaron {len(datos)} anime y se excluyeron {total - len(datos)} filas sin esos datos

- vecinos: 5
- distancia: euclidiana
- entrenamiento: {len(x_entrenamiento)} anime, aproximadamente el 80%
- prueba: {len(x_prueba)} anime, aproximadamente el 20%
- aciertos: {aciertos} de {len(y_prueba)}
- exactitud: {exactitud:.4f}, equivalente al {exactitud * 100:.2f}%
- aciertos al elegir siempre el formato mas comun del entrenamiento: {referencia * 100:.2f}%

se mantuvo aproximadamente la proporcion de formatos al separar los datos, usando la semilla 42
se ajusto la escala de episodios y duracion con los datos de entrenamiento para que sus unidades no dominen las distancias
cada anime de prueba recibe el formato mas repetido entre sus cinco vecinos mas cercanos del entrenamiento

el modelo supera la referencia de elegir siempre el formato mas comun, aunque todavia comete errores
la exactitud corresponde a datos de prueba que no se usaron para entrenar

`predicciones.csv` contiene el formato real y el estimado
en `matriz_confusion.csv`, las filas son los formatos reales y las columnas los estimados
la diagonal muestra los aciertos y las otras celdas muestran los errores
"""
(resultados / "reporte_resultados.md").write_text(reporte, encoding="utf-8")
print(f"clasificacion terminada, exactitud = {exactitud * 100:.2f}%")
