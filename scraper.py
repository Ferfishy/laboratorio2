import re
import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"

MAPA_CALIFICACION = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def obtener_libros() -> list[dict]:
    """
    Extrae los libros de la primera página de books.toscrape.com.
    Gestiona elementos faltantes o malformados mediante bloques try/except
    y valores por defecto, evitando que la ejecución se detenga.
    """
    respuesta = requests.get(URL, timeout=10)
    respuesta.raise_for_status()
    respuesta.encoding = "utf-8"

    soup = BeautifulSoup(respuesta.text, "html.parser")
    articulos = soup.select("article.product_pod")

    libros = []

    for idx, item in enumerate(articulos, start=1):
        try:
            # 1. Título (desde el atributo 'title' del enlace para no truncarlo)
            tag_a = item.select_one("h3 a")
            if not tag_a:
                print(f"[Advertencia] Libro #{idx} sin título. Se omite.")
                continue
            titulo = tag_a.get("title") or tag_a.get_text(strip=True)

            # 2. Precio (limpiando el símbolo £ o caracteres extraños y convirtiendo a float)
            tag_precio = item.select_one("p.price_color")
            texto_precio = tag_precio.get_text(strip=True) if tag_precio else "0.0"
            precio_limpio = re.sub(r"[^\d.]", "", texto_precio)
            precio = float(precio_limpio) if precio_limpio else 0.0

            # 3. Disponibilidad
            tag_disp = item.select_one("p.instock.availability")
            disponibilidad = tag_disp.get_text(strip=True) if tag_disp else "Desconocido"

            # 4. Calificación en estrellas (convertida a entero de 1 a 5)
            tag_rating = item.select_one("p.star-rating")
            clases_rating = tag_rating.get("class", []) if tag_rating else []
            calificacion = 0
            for clase in clases_rating:
                if clase in MAPA_CALIFICACION:
                    calificacion = MAPA_CALIFICACION[clase]
                    break

            libros.append({
                "titulo": titulo.strip(),
                "precio": precio,
                "disponibilidad": disponibilidad,
                "calificacion": int(calificacion)
            })

        except Exception as e:
            # Gestión de errores: se registra el incidente y el bucle continúa
            print(f"[Error] No se pudo procesar el elemento #{idx}: {e}")
            continue

    return libros


if __name__ == "__main__":
    lista_libros = obtener_libros()
    print(f"Total de libros extraídos: {len(lista_libros)}\n")
    print("Primeros 5 registros extraídos:")
    for libro in lista_libros[:5]:
        print(libro)