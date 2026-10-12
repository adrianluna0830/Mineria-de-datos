# reporte de resultados

se uso knn para clasificar el formato del anime a partir de episodios y duracion
se analizaron 5361 anime y se excluyeron 407 filas sin esos datos

- vecinos: 5
- distancia: euclidiana
- entrenamiento: 4288 anime, aproximadamente el 80%
- prueba: 1073 anime, aproximadamente el 20%
- aciertos: 821 de 1073
- exactitud: 0.7651, equivalente al 76.51%
- aciertos al elegir siempre el formato mas comun del entrenamiento: 31.97%

se mantuvo aproximadamente la proporcion de formatos al separar los datos, usando la semilla 42
se ajusto la escala de episodios y duracion con los datos de entrenamiento para que sus unidades no dominen las distancias
cada anime de prueba recibe el formato mas repetido entre sus cinco vecinos mas cercanos del entrenamiento

el modelo supera la referencia de elegir siempre el formato mas comun, aunque todavia comete errores
la exactitud corresponde a datos de prueba que no se usaron para entrenar

`predicciones.csv` contiene el formato real y el estimado
en `matriz_confusion.csv`, las filas son los formatos reales y las columnas los estimados
la diagonal muestra los aciertos y las otras celdas muestran los errores
