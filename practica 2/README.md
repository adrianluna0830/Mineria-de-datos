# Practica 2 de Mineria de Datos

## Objetivo

Aplicar estadistica descriptiva al dataset limpio de AniList de la practica 1,
identificar sus entidades y relaciones, trazar un diagrama entidad-relacion y
obtener metricas de datos agrupados.

## Estadistica aplicada

Para `episodios`, `duracion`, `calificacion`, `popularidad` y `favoritos` se
calculan conteo, nulos, media, mediana, moda, minimo, maximo, sumatoria,
varianza y desviacion estandar muestrales, asimetria y exceso de curtosis.

Las metricas agrupadas se calculan por:

- formato;
- estado;
- año de inicio;
- genero;
- estudio.

Cada tabla agrupada contiene cantidad de anime, disponibilidad y distribucion
de calificaciones, promedios de episodios y duracion, y promedios y sumas de
popularidad y favoritos. Al hacer los calculos, los datos vacios simplemente no se toman en cuenta.

## Entidades y relaciones

Se identificaron las siguientes entidades:

- `Anime`: entidad central identificada por `anime_id`.
- `Formato`: catalogo de formatos como TV, pelicula u ONA.
- `Estado`: catalogo del estado de publicacion.
- `Genero`: catalogo de generos.
- `Estudio`: catalogo de estudios participantes.
- `AnimeGenero`: entidad asociativa entre anime y genero.
- `AnimeEstudio`: entidad asociativa entre anime y estudio.
