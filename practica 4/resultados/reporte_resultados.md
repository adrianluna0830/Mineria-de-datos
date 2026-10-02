# reporte de resultados

se comparo la calificacion de 4337 anime en 7 formatos mediante kruskal-wallis.
se excluyeron 1431 filas sin formato o calificacion.

primero se aplico shapiro-wilk por formato, con h0 de que las calificaciones siguen una distribucion normal.
se rechazo la normalidad en 6 de 7 formatos con nivel de significancia 0.05.
por eso se uso kruskal-wallis para comprobar las diferencias entre formatos.
los resultados de normalidad estan en `normalidad_por_formato.csv`.

- h0: la distribucion de calificaciones es igual en todos los formatos.
- h1: al menos un formato tiene una distribucion diferente.
- nivel de significancia: 0.05.
- estadistico h: 630.2593.
- valor p: 6.9125e-133.

se rechaza h0, hay diferencias entre al menos dos formatos.

se consideran independientes las observaciones y cada anime pertenece a un solo formato.
la prueba no requiere suponer una distribucion normal y no identifica cuales formatos difieren.
el resumen por formato esta en `resumen_por_formato.csv`.
