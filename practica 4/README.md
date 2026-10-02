# practica 4 de mineria de datos

comprobar diferencias en la calificacion del dataset limpio de anilist usando el formato como etiqueta.

primero se revisa la normalidad con shapiro-wilk por formato. se rechaza la normalidad en seis de los siete formatos, por lo que se aplica kruskal-wallis. se usa un nivel de significancia de 0.05 y se excluyen las filas sin formato o calificacion.

para instalar las dependencias y ejecutar desde esta carpeta:

```bash
pip install pandas scipy
python pruebas_estadisticas.py
```

los resultados se guardan en `resultados`:

- `resumen_por_formato.csv`: cantidad, media y mediana de calificacion por formato.
- `normalidad_por_formato.csv`: estadistico, valor p y resultado de shapiro-wilk por formato.
- `reporte_resultados.md`: hipotesis, estadistico, valor p y conclusion.
