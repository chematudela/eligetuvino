
import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO
import pandas as pd


def pagina_principal():
    def cargar_frases():
            try:
                with open("frases.txt", "r", encoding="utf-8") as file:
                    frases = file.readlines()
                return [frase.strip() for frase in frases if frase.strip()]
            except FileNotFoundError:
                return ["No se encontraron frases sobre vino."]

    frases = cargar_frases()

    if "mostrar_analisis" not in st.session_state:
            st.session_state.mostrar_analisis = False

        # Inicializar una frase aleatoria en session_state
    if "frase_actual" not in st.session_state:
            st.session_state.frase_actual = random.choice(frases)

        # Función para cambiar la frase
    def cambiar_frase():
        st.session_state.frase_actual = random.choice(frases)
    # Cargar la imagen desde la URL
    url = "https://ebootcamp.net/wp-content/uploads/2021/11/4Geeks-Academy.jpeg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

# Redimensionar la imagen
    img = img.resize((100, 100))
    header_html = f"""
    <div style="text-align: center; background-color: #800000; padding: 20px; border-radius: 15px; margin: 20px;">
        <img src="{url}" width="100" height="100" style="display: block; float: right;">
        <p style="font-family: 'Playball', cursive; font-size: 35px; color: #b1dbde;">
            Proyecto de Data Science - 4Geeks <br> Analítica sobre vino mundial
        </p>   <p class="frase">{st.session_state.frase_actual}</p>            
    </div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
 
    st.markdown(
            """
            <style>
            .styled-table {
                width: 50%;
                margin: auto;
                border-collapse: collapse;
            }
            .styled-table th {
                background-color: #800000;
                color: white;
                text-align: center;
                font-size: 20px;
                padding: 10px;
            }
            .styled-table td {
                text-align: center;
                padding: 8px;
                font-size: 18px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    integrantes = pd.DataFrame({
            "Integrantes": ["Pauline Charvin", "Jose María Tudela", "Vicente Polo"]
        })

    st.markdown("<table class='styled-table'><tr><th>Nuestro proyecto de Data Science</th></tr>" +
                    "".join(f"<tr><td>{nombre}</td></tr>" for nombre in integrantes["Integrantes"]) +
                    "</table>", unsafe_allow_html=True)

    st.write("")

        # Segunda tabla con tecnologías usadas
    tecnologias = pd.DataFrame({
            "Tecnología": ["Tamaño del Dataset", "Uso de Web Scraping", "Integridad de datos"],
            "Descripción": ["32,000 vinos (espumosos, blancos, tintos)",
                            "BeautifulSoup y Selenium",
                            "NLP y KNN"]
        })

    st.markdown("### Tecnologías utilizadas")
    st.table(tecnologias.set_index("Tecnología")) 

    librerias = pd.DataFrame({
    "Librería": [
        "Streamlit", 
        "Pandas", 
        "Plotly Express", 
        "Altair", 
        "Random", 
        "PIL (Pillow)", 
        "Requests", 
        "BytesIO", 
        "Plotly Colors", 
        "Matplotlib", 
        "Seaborn",
        "Sklearn",
        "google.generativeai"
    ],
    "Descripción": [
        "Framework para crear aplicaciones web interactivas.",
        "Librería para manejo y análisis de datos en estructuras tabulares.",
        "Librería para crear gráficos interactivos y visualizaciones.",
        "Librería para crear gráficos declarativos.",
        "Genera números aleatorios y realiza selecciones al azar.",
        "Librería para abrir, manipular y guardar imágenes.",
        "Permite hacer peticiones HTTP y obtener datos de la web.",
        "Módulo para trabajar con flujos de datos binarios (como imágenes).",
        "Proporciona una paleta de colores para visualizaciones en Plotly.",
        "Librería para la creación de gráficos estáticos.",
        "Librería para visualización de datos estadísticos y gráficos atractivos.",
        "Librería con funciones, modelos de ML y mértricas.",
        "Librería para uso de la api de Gemini (LLM)"

    ]})
    st.markdown("### Librerías utilizadas")
    st.table(librerias.set_index("Librería")) 
    
