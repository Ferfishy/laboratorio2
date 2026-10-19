import pandas as pd
from scraper import obtener_libros

def procesar_datos():
    # 5.2 Obtener los datos extraídos
    libros = obtener_libros()

    # 5.3 Construir el DataFrame
    df = pd.DataFrame(libros)

    # 5.4 Verificar la información inicial
    print("=== Inspección inicial del DataFrame ===")
    print(df.head())
    print("\n=== Información del esquema ===")
    print(df.info())
    print(f"\nDimensiones iniciales (filas, columnas): {df.shape}")
    print(f"Columnas: {list(df.columns)}\n")

    # Paso 6: Limpieza, normalización y verificación de tipos
    # Retirar espacios sobrantes en cadenas
    df["titulo"] = df["titulo"].astype(str).str.strip()
    df["disponibilidad"] = df["disponibilidad"].astype(str).str.strip()

    # Eliminar duplicados por título
    df = df.drop_duplicates(subset=["titulo"]).reset_index(drop=True)

    # Crear columna titulo_normalizado en minúsculas y sin espacios extremos
    df["titulo_normalizado"] = df["titulo"].str.lower().str.strip()

    # Asegurar tipos numéricos en precio (float) y calificacion (int)
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce").astype(float)
    df["calificacion"] = pd.to_numeric(df["calificacion"], errors="coerce").fillna(0).astype(int)

    # Paso 7: Calcular indicadores y exportar a CSV
    cantidad_libros = len(df)
    precio_promedio = df["precio"].mean()

    print("=== Indicadores tras el procesamiento ===")
    print(f"Cantidad de libros válidos: {cantidad_libros}")
    print(f"Precio promedio: £{precio_promedio:.2f}")

    # Exportar a libros.csv sin índice y con codificación UTF-8
    df.to_csv("libros.csv", index=False, encoding="utf-8")
    print("\nArchivo 'libros.csv' exportado correctamente.")


if __name__ == "__main__":
    procesar_datos()