# Laboratorio Evaluado 2: Web Scraping, Procesamiento y Recuperación de Información

**Asignatura:** Ingeniería Web Avanzada (OII436-1)  
**Integrante:** Fernando Ariel Figueroa Olivares  
**URL del Repositorio:** https://github.com/Ferfishy/laboratorio2.git

---

## 1. Instrucciones para reproducir la ejecución

Siga estos pasos desde una terminal para crear y activar el entorno virtual, instalar las dependencias y ejecutar el proyecto de principio a fin:

### 1.1. Crear carpeta de trabajo y entorno virtual
```bash
mkdir laboratorio2
cd laboratorio2

# En Linux / macOS:
python3 -m venv .venv

# En Windows:
py -m venv .venv
```

### 1.2. Activar el entorno virtual
```bash
# En Linux / Git Bash:
source .venv/bin/activate

# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# En Windows (CMD):
.venv\Scripts\activate.bat
```

### 1.3. Instalar dependencias desde `requirements.txt`
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 1.4. Orden de ejecución de los programas
1. **Extracción de datos (Web Scraping):**
   ```bash
   python scraper.py
   ```
2. **Procesamiento, limpieza y exportación a CSV:**
   ```bash
   python procesamiento.py
   ```
3. **Ejecución del buscador de títulos (TF-IDF y similitud del coseno):**
   ```bash
   python buscador.py
   ```

---

## 2. Documentación del manejo de elementos sin datos (Paso 4)

En `scraper.py`, la extracción de cada libro (`article.product_pod`) está encapsulada dentro de un bloque `try...except` para garantizar que el programa nunca termine abruptamente ante un elemento incompleto o malformado:
* Si un libro no posee la etiqueta del título (`h3 a`), se registra una advertencia en consola y se omite ese registro mediante `continue`.
* Si el precio, la disponibilidad o la calificación en estrellas no están presentes, se asignan valores seguros por defecto (`0.0`, `"Desconocido"` y `0`, respectivamente) antes de realizar la conversión de tipos.

---

## 3. Evidencias de Procesamiento y Ejemplos de Búsqueda (Pasos 11 y 13)

### Indicadores obtenidos en `procesamiento.py`
* **Cantidad de libros extraídos y válidos:** `20`
* **Precio promedio:** `£38.05` (`38.0485`)

### Ejemplos de búsqueda ejecutados en `buscador.py`

**Ejemplo 1 — Consulta:** `the` (evaluado con `top_k=3`)
```text
Ingrese una palabra o título: the
The Coming Woman: A Novel Based on the Life of the Infamous Feminist, Victoria Woodhull | Precio: £17.93 | Similitud: 0.3407
The Boys in the Boat: Nine Americans and Their Epic Quest for Gold at the 1936 Berlin Olympics | Precio: £22.60 | Similitud: 0.3056
The Black Maria | Precio: £52.15 | Similitud: 0.2584
```
*Comparación del orden:* Los primeros dos libros repiten la palabra `"the"` varias veces en su título, lo que incrementa su frecuencia de término (TF) y les otorga mayor similitud en comparación con `"The Black Maria"`, donde el término aparece una sola vez.

**Ejemplo 2 — Consulta:** `light`
```text
Ingrese una palabra o título: light
A Light in the Attic | Precio: £51.77 | Similitud: 0.5646
```
*Comparación del orden:* Al ser `"light"` un término único dentro de los 20 títulos de la primera página, tiene un alto peso IDF y recupera exclusivamente el libro coincidente con una puntuación de `0.5646`.

---

## 4. Registro de Pruebas Funcionales (Paso 12)

| Caso | Consulta utilizada | Resultado observado | Estado |
| :--- | :--- | :--- | :--- |
| **T1** | `light` | Se recuperó el libro `"A Light in the Attic"` (Precio: £51.77) con similitud positiva `0.5646`, ordenado de mayor a menor relevancia. | **Cumple** |
| **T2** | `zzxyz123` | Ningún documento obtuvo similitud mayor que cero. Se mostró por pantalla: `No se encontraron coincidencias.` | **Cumple** |
| **T3** | `LIGHT` | Se obtuvo exactamente el mismo ranking y similitud (`0.5646`) que en el caso T1 para `"A Light in the Attic"`. | **Cumple** |
| **T4** | `[vacía]` *(Enter)* | Se mostró el mensaje informativo `Ingrese una consulta no vacía.` seguido de `No se encontraron coincidencias.`, sin lanzar excepciones. | **Cumple** |

**Explicación del comportamiento observado:**  
Todas las pruebas cumplieron con el resultado esperado. El preprocesamiento de la consulta con `consulta.strip().lower()` asegura que las búsquedas en mayúsculas (T3) produzcan vectores idénticos a las búsquedas en minúsculas (T1), y la validación condicional `if not consulta:` gestiona las entradas vacías o compuestas solo por espacios (T4) sin errores en tiempo de ejecución.

---

## 5. Respuestas a las Preguntas del Laboratorio

### Pregunta 1 (2 pts): ¿Para qué sirve BeautifulSoup y cómo se diferencia de requests?
* **`requests`** es una librería de cliente HTTP encargada de la comunicación de red: envía la petición al servidor web (como `requests.get()`) y descarga la respuesta del servidor, entregando el código HTML como una cadena de texto plano sin procesar.
* **`BeautifulSoup`** es una librería de análisis sintáctico (*parsing*) de documentos HTML y XML. Su función es tomar el texto plano obtenido con `requests` y construir un árbol de objetos en memoria (DOM) que permite buscar, recorrer y filtrar etiquetas, clases CSS y atributos de manera estructurada.

### Pregunta 2 (2 pts): ¿Qué riesgo existe al depender de selectores HTML específicos si el sitio cambia?
Existe el riesgo de que **el scraper deje de funcionar o extraiga datos incorrectos (alta fragilidad ante cambios en la interfaz)**. Si el sitio web actualiza su diseño, modifica la jerarquía de etiquetas HTML o cambia el nombre de las clases CSS (por ejemplo, si `article.product_pod` o `p.price_color` pasan a llamarse distinto), los selectores definidos en el código ya no encontrarán los elementos esperados, retornando `None`, listas vacías o provocando excepciones si no se manejan adecuadamente.

### Pregunta 3 (2 pts): ¿Por qué normalizar los títulos antes de implementar la búsqueda?
La normalización (convertir a minúsculas y eliminar espacios sobrantes en los extremos) es necesaria para garantizar la **consistencia léxica del vocabulario** entre el índice y las consultas. Sin normalización, variaciones de una misma palabra como `"Light"`, `"LIGHT"` o `"light "` serían tratadas como tokens diferentes, fragmentando las frecuencias en la matriz TF-IDF e impidiendo encontrar coincidencias cuando el usuario escribe con distinta capitalización.

### Pregunta 4 (2 pts): En el código entregado, ¿qué función cumple `fit_transform()` sobre los títulos y por qué se usa `transform()` para la consulta?
* **`fit_transform()`** sobre los títulos realiza dos pasos: primero **aprende (`fit`)** el vocabulario de toda la colección de libros y calcula los pesos IDF de cada término; segundo, **transforma (`transform`)** cada título en su vector numérico TF-IDF dentro de ese espacio vectorial.
* **`transform()`** se utiliza para la consulta porque esta debe representarse utilizando **exactamente el mismo vocabulario y las mismas dimensiones** aprendidas a partir de los títulos. Si se usara `fit_transform()` en la consulta, el vectorizador redefiniría el vocabulario únicamente con las palabras ingresadas por el usuario, generando un vector de distinta dimensión incompatible para calcular la similitud del coseno contra `matriz_tfidf`.

### Pregunta 5 (2 pts): Si dos libros obtienen similitudes de 0.75 y 0.20 para la misma consulta, ¿cuál se muestra primero? Explique qué indica una puntuación cercana a cero.
* **¿Cuál se muestra primero?** Se muestra primero el libro con similitud **0.75**, ya que los resultados se ordenan de mayor a menor relevancia (`argsort()[::-1]`), priorizando el título cuya representación vectorial es más cercana a la consulta.
* **¿Qué indica una puntuación cercana a cero?** Indica que el ángulo entre el vector de la consulta y el vector del título es cercano a 90° (vectores casi ortogonales); en términos prácticos, significa que el título del libro no comparte términos (o comparte términos de peso insignificante) con las palabras buscadas por el usuario.

### Pregunta 6 (2 pts): ¿Qué limitación tiene buscar solo por palabras presentes en títulos mediante TF-IDF? Proponga una mejora concreta.
* **Limitación:** TF-IDF se basa en coincidencias léxicas exactas (*bag-of-words*) y no comprende el significado ni el contexto semántico; además, los títulos suelen ser muy breves y poco descriptivos. Si el usuario busca mediante sinónimos, conceptos relacionados, palabras con errores ortográficos o términos que describen la trama pero no figuran literalmente en el título, el buscador obtendrá una similitud de `0` y no recuperará el libro.
* **Mejora concreta:** Extraer también la **descripción completa y la categoría** de cada libro entrando a su URL de detalle para indexar un texto más rico junto al título, y combinar o reemplazar TF-IDF por **embeddings semánticos preentrenados** (como `Sentence-Transformers`) o aplicar **lematización y n-gramas de caracteres** (`ngram_range=(3, 5)`) en el vectorizador para capturar raíces de palabras, sinónimos y tolerar errores de tipeo.