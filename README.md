# Elige tu vino

⚠️ **Aviso Legal**: Este proyecto se distribuye exclusivamente con **fines educativos**.  
No está permitido su uso con **fines comerciales ni lucrativos** sin autorización expresa del autor.


## Descripción

Este proyecto se realiza en el marco del bootcamp de Machine Learning de la 4GeeksAcademy, llevado a cabo de noviembre de 2024 a marzo de 2025.

Elige tu vino es un proyecto que, mediante técnicas de análisis de datos y machine learning, tiene como objetivo ofrecer aplicaciones reales y útiles tales como: 
- Estimación de la nota de un vino en la plataforma VIVINO por medio de fotografías de sus etiquetas.
- Porpuesta del vino con mayor puntuación posible en VIVINO para un precio máximo dado en relación a uno vino dado (vinos catalogados como similiares según el algoritmo que hemos realizado)

Se basa en informaciones sobre unos 32.000 vinos, extraídas por web scraping de la página vivino.es. 
Utilizando modelos como KMean, clustering, NLP e integración de IA Gemini (LMM), hemos implementado herramientas que complementan lo que ya ofrece esa plataforma, ayudando aún más a los usuarios en su búsqueda del vino ideal.

## Web scraping ;
- **3 datasets :** por tipo de vino (tinto, blancos, espumosos). Vinos ofrecidos en mercado español.
- **Datos recolectados** : Url, ID, Nombre del vino, Año, País, Región, Bodega, Tipo de vino, Uva, Precio, Valoración, Contenido de alcohol, Maridajes, Ligero/Poderoso, Suave/Tánico, Seco/Dulce, Débil/Ácido, Notas de sabor.

## Las funcionalidades incluyen:

**Datos relevantes e infografía :** análisis enfocada al mercado español.
**Bodega perfecta y vino perfecto :** estudio de mercado, recomendaciones para inversores queriendo empezar un negocio acerca el vino, en España.
**Recomendador de vino :** Recomendación de un vino similar al elegido por el usuario, dentro de un rango de precio y con la mejor valoración.
**Valorify :** Predicción de la valoración de un vino nuevo. Reconocimiento de foto de la etiqueta por IA (Gemini) para facilitar al usuario el relleno de los campos necesarios.

## Librerías: 

**BeautifulSoup y Selenium :** Web Scraping
**Streamlit :** Framework para crear aplicaciones web interactivas.
**Pandas :** Librería para manejo y análisis de datos en estructuras tabulares.
**Plotly Express :** Librería para crear gráficos interactivos y visualizaciones.
**Altair :** Librería para crear gráficos declarativos.
**Random :**  Genera números aleatorios y realiza selecciones al azar.
**PIL :** Librería para abrir, manipular y guardar imágenes.
**Requests :**  Permite hacer peticiones HTTP y obtener datos de la web.
**BytesI0 :** Módulo para trabajar con flujos de datos binarios (como imágenes).
**Plotly Colors :** Proporciona una paleta de colores para visualizaciones en Plotly.
**Matplotlib :** Librería para la creación de gráficos estáticos.
**Seaborn :** Librería para visualización de datos estadísticos y gráficos atractivos.
**SKlearn :** Librería con funciones, modelos de ML y mértricas.
**google.generativeai :** Librería para uso de la api de Gemini (LLM).
**Re :** Expresión regular


## 📂 Estructura del Proyecto

Explicación de los archivos y su propósito.

### 📘 Documentación  
- **`README.md`** → Explicación del proyecto, su estructura y cómo trabajar con él.  

### 🗂 Datos  
- **`data/`** → Contiene:  
  - Datasets originales (incluyendo el merged final).  
  - Datasets trabajados.  
  - Imágenes necesarias para los scripts. 

### 🔄 obtencion_datos_scraping  
- **`scrap_wine_list.py`** → Obtiene URLs de todos los vinos en formato API.  
- **`Conversor2.0.py`** → Realiza una conversión de url al formato "estático". 
- **`web_scraping.ipynb`** → notebook para extraer información detallada de las páginas de vino.  
 
### 📊 analisis_y_modelado/  
- **`eda_blancos.ipynb/`** → Tratamiento del dataset inicial de vinos blancos.  
- **`eda_espumosos.ipynb/`** → Tratamiento del dataset inicial de vinos espumosos. 
- **`eda_modelos_tintos.ipynb/`** → Tratamiento del dataset inicial de vinos tintos y modelados para las aplicaciones.  

 
### 📊 notebook_scripts_aux 
- Scripts y cuadernos de desarrollo auxiliar.

 
### 🌐 Aplicación Web  
- **`src/`** → Contiene los scripts finales y los modelos usados: 
  - **`modelos/`** →  Contiene los modelos entrenados para la aplicación. 
  - **`utils.py`** →  Contiene los scripts fundamentales del proyecto. El archivo main invoca las funciones de contenidas en él.
  - **`main_stream.py`** → Desarrollo de la app en Streamlit.  
  

## Instalación

**Enlace Streamlit :** https://eligetuvino-bwssqkrbqm8gvrncys5jof.streamlit.app