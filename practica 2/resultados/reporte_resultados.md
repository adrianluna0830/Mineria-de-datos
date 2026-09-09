# reporte de resultados

se analizaron **5,768 anime** entre **2019-10-03** y **2026-12-11**.

- calificacion media: **64.25**.
- mediana de calificacion: **64.00**.
- desviacion estandar de calificacion: **9.97**.
- asimetria de popularidad: **5.91**.
- columna con mas nulos: **calificacion**, con **1431**.
- formato con mayor calificacion media: **movie**, con **69.04**.
- genero con mayor calificacion media: **drama**, con **70.62**.

las entidades son anime, formato, estado, genero y estudio. anime se relaciona con formato y estado, y tiene relaciones muchos a muchos con genero y estudio mediante anime_genero y anime_estudio. los datos faltantes se excluyeron de los calculos y no se reemplazaron con cero.
