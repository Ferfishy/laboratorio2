import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar y preparar documentos
libros = pd.read_csv("libros.csv", encoding="utf-8")
libros = libros.dropna(subset=["titulo_normalizado"]).copy()
libros["titulo_normalizado"] = libros["titulo_normalizado"].astype(str).str.strip()
libros = libros[libros["titulo_normalizado"] != ""].reset_index(drop=True)

# Construir el índice (una sola vez)
vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(libros["titulo_normalizado"])


def buscar(consulta: str, top_k: int = 5):
    consulta = consulta.strip().lower()
    if not consulta:
        print("Ingrese una consulta no vacía.")
        return []

    # Transformar la consulta usando el vocabulario aprendido
    vector_consulta = vectorizador.transform([consulta])

    puntuaciones = cosine_similarity(vector_consulta, matriz_tfidf).ravel()
    indices = puntuaciones.argsort()[::-1]

    resultados = []
    for i in indices:
        if puntuaciones[i] <= 0:
            break
        resultados.append({
            "titulo": libros.iloc[i]["titulo"],
            "precio": libros.iloc[i]["precio"],
            "similitud": float(puntuaciones[i])
        })
        if len(resultados) >= top_k:
            break

    return resultados


if __name__ == "__main__":
    consulta = input("Ingrese una palabra o título: ")
    # Desafío breve Paso 11: usar top_k=3 (puedes dejar buscar(consulta) si prefieres top_k=5 por defecto)
    resultados = buscar(consulta, top_k=3)
    if not resultados:
        print("No se encontraron coincidencias.")
    for r in resultados:
        print(f"{r['titulo']} | Precio: £{r['precio']:.2f} | "
              f"Similitud: {r['similitud']:.4f}")