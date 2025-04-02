# Elige tu vino

## Descripción

Este proyecto se realiza en el marco del bootcamp de Machine Learning de la 4GeeksAcademy, llevado a cabo de noviembre de 2024 a marzo de 2025.

Elige tu vino es un proyecto que, mediante técnicas de análisis de datos y machine learning, tiene como objetivo definir el "vino perfecto" para un usuario, tanto B2C como B2B. 
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



## Archivos y su Propósito

- **README.md :** Este archivo, donde se explica la estructura del proyecto y cómo trabajar con él.
- **scrap_wine_list.py :** Conseguir URLs de todos los vinos, en formato API.
- **Conversor2.0.py :** Scraping de la lista de URLs en formato API para obtener URLs finales, por batch de 100.
- **Corrector csv.ipynb :** Scripts para conseguir información detallada  dentro de las páginas de vino. 
- **merge.ipynb :** Codigos utiles para recopilación de la info de cientos de archivos de scrap: adaptar formato, limpiar duplicados, revisar info, y merge final.
- **archivos en data :** Datasets originales (con el merged ya hecho), datasets trabajados y fotos necesarios para los scripts
- **Archivo Notebooks_script_aux :** Script necesarios para tareas a lo largo del proceso: limpieza de datos, script para API Gemini, scrapping, EDA, KMeans
- **src :** (Script finales) = main_stream.py para el desarollo de streamlit y las funciones y modelos necesarios para que funcione. 

## Instalación

**Enlace Streamlit :**
