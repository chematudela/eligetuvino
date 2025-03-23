import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px
import altair as alt
import random
from PIL import Image
import requests
from io import BytesIO
import plotly.colors as pc
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import json
from utils import pagina_principal

with open('data/datasets/processed/country_mapping.json', 'r', encoding="utf-8") as f:
    country_mapping = json.load(f)



st.set_page_config(
    page_title="Dashboard sobre vino mundial",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")





def bodega_perfecta():

    st.title("Datos para una bodega perfecta")
       
    # Crear el desplegable para seleccionar el tipo de vino
    vino_tipo = st.selectbox(
        "Selecciona el tipo de vino",
        ("Vino Tinto", "Vino Blanco", "Vino Espumoso")
    )

# Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    if vino_tipo == "Vino Tinto":
        archivo_csv = r'C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\tintos.csv'  
    elif vino_tipo == "Vino Blanco":
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\blancos.csv"  
    else:
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\espumosos.csv"  

    # Cargar el CSV seleccionado en el DataFrame df
    df = pd.read_csv(archivo_csv)

    # Crear columnas
    tab1, tab2 = st.columns(2)

    # Gráfico 1: Heatmap
    with tab1:
        st.subheader("Heatmap de Valoraciones")
        heatmap = alt.Chart(df).mark_rect().encode(
            x=alt.X('Año:O', title="Año"),
            y=alt.Y('País:O', title="País"),
            color=alt.Color('Valoración:Q', scale=alt.Scale(scheme='reds'))
        ).properties(width=400, height=300)
        st.altair_chart(heatmap, use_container_width=True)

    # Gráfico 2: Precio medio por tipo de uva
    with tab2:
        st.subheader("Precio medio por tipo de uva")
        bar_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('mean(Precio):Q', title="Precio Medio"),
            y=alt.Y('Uva:N', title="Tipo de Uva", sort='-x'),
            color=alt.Color('Uva:N', legend=None)
        ).properties(width=400, height=300)
        st.altair_chart(bar_chart, use_container_width=True)

    # Gráfico 3: Proporción de vinos por país
    with tab1:
        st.subheader("Distribución de vinos por país")
        country_count = df['País'].value_counts().reset_index()
        country_count.columns = ['País', 'Cantidad']
        pie_chart = alt.Chart(country_count).mark_arc().encode(
            theta='Cantidad:Q',
            color=alt.Color('País:N', legend=None)
        ).properties(width=400, height=300)
        st.altair_chart(pie_chart, use_container_width=True)

def img_process():
    st.title("Subir y mostrar imagen")

    # Widget para subir la imagen
    uploaded_file = st.file_uploader("Sube una etiqueta de vino DE FRENTE", type=["png", "jpg", "jpeg"])

    # Si se sube una imagen, se muestra en pantalla
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        delantera = image.resize((200, 200))

        # Mostrar la imagen redimensionada y centrada
        st.image(delantera, caption="Etiqueta delantera de vino subida", use_container_width=False)
    
    uploaded_file = st.file_uploader("Sube una etiqueta de vino TRASERA", type=["png", "jpg", "jpeg"])

    # Si se sube una imagen, se muestra en pantalla
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        trasera = image.resize((200, 200))

        # Mostrar la imagen redimensionada y centrada
        st.image(trasera, caption="Etiqueta trasera de vino subida", use_container_width=False)

    precio = st.text_input("¿Cuál es el precio del vino?")

    # Mostrar el precio ingresado
    if precio:
        try:
            precio_float = float(precio)  # Convertir el precio a float
            st.write(f"El precio ingresado es: ${precio_float:.2f}")
        except ValueError:
            st.error("Por favor, ingresa un valor numérico válido para el precio.")
    

def vino_perfecto():
    st.title("Características del vino perfecto")
    
    # Botón para subir el archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type="csv")

    # Verificar si se ha subido un archivo
    if uploaded_file is not None:
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(uploaded_file)
        
        st.write("Gráficos de dispersión sobre características de sabor")

        # Definir características sensoriales
        features = ['Ligero/Poderoso', 'Suave/Tánico', 'Seco/Dulce', 'Débil/Ácido']

        # Ordenar el DataFrame por valoración y tomar los 50 mejores vinos
        top_50_vinos = df.sort_values(by='Valoración', ascending=False).head(50)

        # Calcular los valores promedio de las características en los 50 mejores vinos
        mean_values = top_50_vinos[features].mean()

        # Graficar la relación entre cada característica y la valoración
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()

        for i, feature in enumerate(features):
            sns.scatterplot(data=df, x=feature, y='Valoración', alpha=0.5, ax=axes[i], label="Todos los vinos")
            sns.scatterplot(data=top_50_vinos, x=feature, y='Valoración', color='red', ax=axes[i], label="Top 50 vinos")
            axes[i].set_title(f'Valoración vs {feature}')
            axes[i].set_xlabel(feature)
            axes[i].set_ylabel('Valoración')

        plt.tight_layout()
        st.pyplot(fig)

        # Mostrar los valores en la aplicación
        st.write("**Valores promedio en los 50 vinos mejor valorados:**")
        for feature, value in mean_values.items():
            st.write(f"- {feature}: {value:.2f}")
        
    
    st.title("🍷 Características promedio de los 100 vinos mejor valorados")

    # Tomar los 100 mejores vinos según la valoración
    top_100_vinos = df.sort_values(by='Valoración', ascending=False).head(100)
    # Características a analizar
    features = ['Ligero/Poderoso', 'Suave/Tánico', 'Seco/Dulce', 'Débil/Ácido']

    # Calcular la media de cada característica
    media_caracteristicas = top_100_vinos[features].mean()

    # Convertir valores en lista
    values = media_caracteristicas.tolist()

    # Nombres de las características
    labels = features

        # Número de variables (lados del gráfico)
    num_vars = len(labels)

        # Ángulos para el gráfico de araña
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Cerrar el gráfico de araña
    values += values[:1]
    angles += angles[:1]

        # Crear la figura y los ejes en modo polar
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Dibujar el gráfico con colores de vino
    ax.fill(angles, values, color='#8B0000', alpha=0.4)  # Relleno color vino tinto (granate)
    ax.plot(angles, values, color='#4B0000', linewidth=2)  # Bordes más oscuros (burdeos)

        # Agregar etiquetas con los valores
    for i, value in enumerate(values[:-1]):
        ax.text(angles[i], value + 0.2, f"{value:.2f}", ha='center', fontsize=10, fontweight='bold', color='#4B0000')

        # Ajustar los labels y los ticks
    ax.set_yticklabels([])  # No mostrar etiquetas en el eje radial
    ax.set_xticks(angles[:-1])  # No incluir el último ángulo porque lo hemos duplicado
    ax.set_xticklabels(labels, fontsize=12, fontweight='bold', color='#8B0000')

        # Título del gráfico
    ax.set_title('🍷 Características promedio de los 100 vinos mejor valorados', size=15, color='#4B0000', y=1.1)

        # Mostrar en Streamlit
    st.pyplot(fig)

    st.title("🍇 Correlación entre Tipos de Uva y Valoración")

    # Lista de columnas de tipos de uva
    uva_columns = ['Aglianico', 'Barbera', 'Blaufränkisch', 'CabernetFranc', 'CabernetSauvignon', 'Carignan',
                       'Cariñena', 'Corvina', 'Corvinone', 'Gamay', 'Garnacha', 'Graciano', 'Grenache', 'Malbec',
                       'Mencia', 'Merlot', 'Monastrell', 'Montepulciano', 'Mourvedre', 'Nebbiolo', 'NerelloMascalese',
                       "Nerod'Avola", 'PetitVerdot', 'PinotNero', 'PinotNoir', 'Primitivo', 'Rondinella', 'Sangiovese',
                       'Shiraz/Syrah', 'Tempranillo', 'TourigaNacional', 'Zweigelt']

        # Asegurar que las columnas son numéricas
    df[uva_columns] = df[uva_columns].apply(pd.to_numeric, errors='coerce', downcast='integer')

        # Calcular la correlación con la valoración
    correlaciones = df[uva_columns].corrwith(df['Valoración']).sort_values(ascending=False)

    tab1, tab2 = st.columns(2)

    with tab1:    # Obtener las 10 mejores correlaciones
        top_10_correlaciones = correlaciones.head(10)
    # Mostrar las 10 mejores correlaciones en la app
        st.write(top_10_correlaciones)
    with tab2:
    # Crear el gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=top_10_correlaciones.index, y=top_10_correlaciones.values, palette='magma', ax=ax)

        # Personalización del gráfico
        ax.set_title('🍷 Correlación entre Tipos de Uva y Valoración', fontsize=16)
        ax.set_xlabel('Tipo de Uva', fontsize=14)
        ax.set_ylabel('Correlación con Valoración', fontsize=14)
        ax.set_xticklabels(top_10_correlaciones.index, rotation=45, ha='right')

        # Mostrar gráfico en Streamlit
        st.pyplot(fig)





def recomendador_de_vinos():
    st.title("Recomendador de vinos")
    

st.sidebar.title("Navegación")
pagina= st.sidebar.selectbox("Selecciona una página", ["Página principal", "EDA 1", "Bodega Perfecta","Vino perfecto","Procesado de imagen", "Recomendador de vinos"])

if pagina == "Página principal":
    pagina_principal()
elif pagina == "EDA 1":
    eda_1()
elif pagina == "Bodega Perfecta":
    bodega_perfecta()
elif pagina == "Vino perfecto":
    vino_perfecto()
elif pagina == "Procesado de imagen":
    img_process()
elif pagina == "Recomendador de vinos":
    recomendador_de_vinos()