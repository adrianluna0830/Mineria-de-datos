# practica 6 de mineria de datos

crear y evaluar un modelo de knn que clasifique el formato del anime usando episodios y duracion

en la conferencia de clasificacion, entre 20:50 y 23:17, se explica que knn usa datos etiquetados y asigna a cada dato nuevo la etiqueta mas repetida entre sus vecinos mas cercanos

se usan cinco vecinos y distancia euclidiana; los datos se separan en 80% para entrenamiento y 20% para prueba, conservando aproximadamente la proporcion de formatos; la escala se ajusta solo con el entrenamiento

para instalar las dependencias y ejecutar desde esta carpeta:

```bash
pip install pandas scikit-learn
python clasificacion_knn.py
```

los resultados se guardan en `resultados`:

- `predicciones.csv`: formato real y estimado de cada anime de prueba
- `matriz_confusion.csv`: aciertos y errores por formato
- `reporte_resultados.md`: datos usados, configuracion, porcentaje de aciertos y conclusion

se usa [knn de scikit-learn](https://scikit-learn.org/stable/modules/neighbors.html#nearest-neighbors-classification)
