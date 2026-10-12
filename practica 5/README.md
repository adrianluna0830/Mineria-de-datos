# practica 5 de mineria de datos

generar un modelo lineal entre popularidad y favoritos, crear las graficas y obtener r^2 y la correlacion de pearson

en la conferencia de regresion lineal se indica que basta un modelo (1:05:05) y que x puede ser numerica (58:29); se muestran los puntos, la recta y el promedio, como en el ejemplo del profesor

para instalar las dependencias y ejecutar desde esta carpeta:

```bash
pip install pandas scipy matplotlib
python modelo_lineal.py
```

los resultados se guardan en `resultados`:

- `dispersion.png`: popularidad y favoritos de cada anime
- `modelo_lineal.png`: datos, recta ajustada, promedio y r^2
- `reporte_resultados.md`: variables, ecuacion, correlacion, r^2 y conclusion

se usa [linregress de scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html) para ajustar la recta por minimos cuadrados y obtener la correlacion; en este modelo, r^2 es el cuadrado de esa correlacion
