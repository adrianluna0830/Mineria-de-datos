# reporte de resultados

se uso el dataset limpio de anilist para estudiar la relacion entre popularidad y favoritos
se analizaron 5768 anime y se excluyeron 0 filas sin esos datos

- x: popularidad, cantidad de usuarios que tienen el anime en su lista
- y: favoritos, cantidad de usuarios que lo marcaron como favorito
- modelo por minimos cuadrados: favoritos = 0.038769 * popularidad + (-205.5286)
- correlacion de pearson: 0.8805
- r^2: 0.7753

la relacion es positiva: los anime con mayor popularidad tienden a tener mas favoritos
el modelo explica el 77.53% de la variacion de favoritos en los datos usados
esta relacion no demuestra que una variable cause la otra

`dispersion.png` muestra los datos; `modelo_lineal.png` agrega la recta y el promedio de favoritos
