# reporte de resultados

se agruparon 5361 anime usando episodios y duracion; se excluyeron 407 filas sin esos datos
se ajusto la escala de ambas variables y se probaron de dos a seis grupos con k-means
el modelo uso la semilla 42 y diez inicializaciones por cada valor de k

- grupos elegidos: 3
- silueta: 0.7605
- inercia: 3491.6896

se eligio el modelo con mayor silueta entre los valores probados
la silueta va de -1 a 1; valores cercanos a 1 indican grupos compactos y separados
la inercia suma las distancias al cuadrado de los datos a sus centroides, usando la escala ajustada
la inercia suele bajar al agregar grupos, por eso se uso la silueta para elegir k

el grupo 1 tiene mas episodios en promedio y el grupo 2 tiene mayor duracion en promedio
los grupos tienen tamaños distintos: el mas grande contiene 4887 anime y el mas pequeño 27
los numeros de grupo solo los identifican; se agrupo sin usar las etiquetas de formato
`resumen_grupos.csv` contiene la cantidad y los promedios de cada grupo en sus unidades originales
`agrupamiento.png` muestra los grupos y sus centroides; `evaluacion.png` compara inercia y silueta
