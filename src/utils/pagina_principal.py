import streamlit as st
import random
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import os


def pagina_principal():
        
    # Cargar imagen desde URL
    url = "https://ebootcamp.net/wp-content/uploads/2021/11/4Geeks-Academy.jpeg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).resize((100, 100))
    
    # Encabezado
    st.markdown(f"""
    <div style="text-align: center; background-color: #800000; padding: 20px; border-radius: 15px; margin: 20px;">
        <img src="{url}" width="100" height="100" style="display: block; float: right;">
        <p style="font-family: 'Playball', cursive; font-size: 35px; color: #b1dbde;">
            Proyecto de Data Science - 4Geeks <br> Analítica sobre vino mundial
        </p>
      
    </div>
    """, unsafe_allow_html=True)

   
    
    # Tabla de integrantes
    integrantes = pd.DataFrame({"Integrantes": ["Pauline Charvin", "Jose María Tudela", "Vicente Polo"]})
    st.markdown("### Nuestro proyecto de Data Science")
    integrantes = integrantes.reset_index(drop=True)
    st.dataframe(integrantes, hide_index=True)
    
    # Tecnologías utilizadas
    tecnologias = pd.DataFrame({
        "Función": ["Tamaño del Dataset", "Uso de Web Scraping", "Integridad de datos","Nubes de palabras", "Gráficos para análisis",
                     "Uso de la IA", "Soporte web", "One Hot Encoder", "Normalización de valores","Selección características importantes", 
                     "Modelo de Machine Learning Supervisado", "Optimización de hiperparámetros del modelo"],
        "Tecnología utilizada": ["32,000 vinos (espumosos, blancos, tintos)",
                        "BeautifulSoup y Selenium",
                        "NLP y KNN","WordCloud","Seaborn, Altair, Matplotlib", "Google Gemini", 
                        "Streamlit", "Sklearn","MinMaxScaler", "XgBoost", "LinearRegression de Sklearn, Decision Tree regressor, Random Forest Regressor", "Randomized Search CV"]
    })
    st.markdown("### Tecnologías utilizadas")
    st.table(tecnologias.set_index("Función")) 
    
    # Métricas del modelo
    metricas = pd.DataFrame({
        "Métrica": ["R²", "MAPE"],
        "Train": [0.73, 2.90],
        "Test": [0.61, 3.51],
    })
    st.markdown("### Métricas finales del modelo")
    st.table(metricas.set_index("Métrica"))
