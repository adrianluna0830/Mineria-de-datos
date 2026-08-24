# Práctica 1 de Minería de Datos

Nombre: Dataset de Anime de AniList API.

Fuente: https://docs.anilist.co/

Objetivo: analizar la relación entre características, popularidad y calificación de los anime.

Archivos creados:

- `obtener_anilist.py`: descarga los datos de la API.
- `limpiar_anilist.py`: limpia el dataset descargado.
- `anilist_raw.csv`: datos originales.
- `anilist_limpio.csv`: dataset final limpio.

La limpieza elimina duplicados por `id`, convierte la fecha de inicio, elimina registros sin título o fecha completa y convierte las variables numéricas sin reemplazar los valores nulos.

Para instalar las dependencias y ejecutar los scripts:

```bash
pip install requests pandas
python obtener_anilist.py
python limpiar_anilist.py
```
