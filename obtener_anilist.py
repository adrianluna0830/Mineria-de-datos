import requests
import pandas as pd
import time


def obtener_anime():
    url = "https://graphql.anilist.co"
    consulta = """
    query ($pagina: Int, $maximo: FuzzyDateInt) {
      Page(page: $pagina, perPage: 50) {
        media(type: ANIME, sort: START_DATE_DESC, startDate_greater: 10000000, startDate_lesser: $maximo) {
          id
          title { romaji }
          startDate { year month day }
          format
          status
          episodes
          duration
          genres
          studios(isMain: true) { nodes { name } }
          averageScore
          popularity
          favourites
        }
      }
    }
    """
    datos = []
    pagina = 1
    total_paginas = 1
    maximo = 20270000
    while total_paginas <= 120:
        variables = {"pagina": pagina, "maximo": maximo}
        respuesta = requests.post(url, json={"query": consulta, "variables": variables})
        if respuesta.status_code == 429:
            time.sleep(60)
            continue
        animes = respuesta.json()["data"]["Page"]["media"]
        for anime in animes:
            fecha = anime["startDate"]
            fecha_inicio = None
            if fecha["year"] and fecha["month"] and fecha["day"]:
                fecha_inicio = f'{fecha["year"]}-{fecha["month"]:02d}-{fecha["day"]:02d}'
            datos.append({
                "id": anime["id"],
                "titulo": anime["title"]["romaji"],
                "fecha_inicio": fecha_inicio,
                "formato": anime["format"],
                "estado": anime["status"],
                "episodios": anime["episodes"],
                "duracion": anime["duration"],
                "generos": "|".join(anime["genres"]),
                "estudios": "|".join(estudio["name"] for estudio in anime["studios"]["nodes"]),
                "calificacion": anime["averageScore"],
                "popularidad": anime["popularity"],
                "favoritos": anime["favourites"]
            })
        print("pagina", total_paginas, "elementos", len(datos))
        if pagina == 60:
            fecha = anime["startDate"]
            maximo = fecha["year"] * 10000 + fecha["month"] * 100 + fecha["day"]
            pagina = 1
        else:
            pagina += 1
        total_paginas += 1
        if total_paginas <= 120:
            time.sleep(3)
    pd.DataFrame(datos).to_csv("anilist_raw.csv", index=False)
    print("archivo anilist_raw.csv creado")


obtener_anime()
