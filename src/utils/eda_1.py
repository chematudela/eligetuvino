import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import json
import plotly.express as px
import plotly.colors as pc
from utils.country_mapping import country_mapping
from PIL import Image
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#with open('data/datasets/processed/country_mapping.json', 'r', encoding="utf-8") as f:
    #country_mapping = json.load(f)

def eda_1():
    st.title("📊 Primera parte del EDA")

    # Crear el desplegable para seleccionar el tipo de vino
    vino_tipo = st.selectbox(
        "Selecciona el tipo de vino",
        ("Vino Tinto", "Vino Blanco", "Vino Espumoso")
    )

# Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    # Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    if vino_tipo == "Vino Tinto":
        archivo_csv = 'data/datasets/processed/df_merged.csv'
    elif vino_tipo == "Vino Blanco":
        archivo_csv = 'data/datasets/processed/df_mergedf_blancos.csv'
    else:
        archivo_csv = 'data/datasets/processed/df_mergedf_espumosos.csv'  
# Cargar el CSV seleccionado en el DataFrame df
    df = pd.read_csv(archivo_csv)    
    df["País"] = df["País"].replace(country_mapping)

    # Grouping data by number of wines
    df_grouped_1 = df.groupby("País")["ID"].nunique().reset_index(name="num_vinos")
    
    # Columna para el gráfico
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas
    
    with col1:
        st.subheader("Distribución de vinos por país")
        country_count = df['País'].value_counts().reset_index()
        country_count.columns = ['País', 'Cantidad']
        total_vinos = country_count['Cantidad'].sum()
        country_count['Porcentaje'] = (country_count['Cantidad'] / total_vinos) * 100
        
        pie_chart = alt.Chart(country_count).mark_arc().encode(
            theta='Cantidad:Q',  # El tamaño de cada sección
            color=alt.Color('País:N', legend=None),  # Color por país
            tooltip=['País:N', 'Cantidad:Q', 'Porcentaje:Q'],  # Mostrar el país, la cantidad y el porcentaje en el tooltip
            text=alt.Text('Porcentaje:Q', format='.1f')  # Mostrar el porcentaje en cada sección
        ).properties(width=350, height=300)  # Ajusta el tamaño del gráfico

        pie_chart = pie_chart.configure_mark(
            fontSize=14,  # Tamaño de la fuente
            fontWeight='bold'
        )
        st.altair_chart(pie_chart, use_container_width=True)

    with col2:
        # Columna para la tabla
        st.subheader("🔝 Top 10 países con más vinos registrados")
        # Top 10 países con más vinos
        df_top_10 = df_grouped_1.sort_values(by="num_vinos", ascending=False).head(10)
        st.table(df_top_10.set_index("País"))
        pass

    st.divider()

    # Agrupar los datos por país y bodega, contando el número de vinos por combinación
    df_grouped_1 = df.groupby(["País", "Bodega"])["ID"].nunique().reset_index(name="num_vinos")

    # Crear las columnas para el layout
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    country_bodega_count = df.groupby(["País", "Bodega"])["ID"].nunique().reset_index(name="Cantidad")
    total_vinos = country_bodega_count['Cantidad'].sum()
    country_bodega_count['Porcentaje'] = (country_bodega_count['Cantidad'] / total_vinos) * 100

    with col1:
        country_bodega_count_grouped = country_bodega_count.groupby("País")["Cantidad"].count().reset_index(name="num_bodegas")
        countries_with_more_than_20_bodegas = country_bodega_count_grouped[country_bodega_count_grouped['num_bodegas'] > 20]['País']
        filtered_data = country_bodega_count[country_bodega_count['País'].isin(countries_with_more_than_20_bodegas)]

        # Gráfico de barras apiladas
        bar_chart = alt.Chart(filtered_data).mark_bar().encode(
            x='Cantidad:Q',  # Longitud de las barras
            y=alt.Y('País:N', sort='-x'),  # Países, ordenados por la cantidad
            color=alt.Color('Bodega:N', legend=None),  # Colores por bodega sin leyenda
            tooltip=['País:N', 'Bodega:N', 'Cantidad:Q', 'Porcentaje:Q']  # Información mostrada al pasar el ratón
        ).properties(width=600, height=400)

        # Ajusta el diseño de la gráfica (opcional)
        bar_chart = bar_chart.configure_mark(
            fontSize=14,  # Tamaño de la fuente
            fontWeight='bold'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(bar_chart, use_container_width=True)

        
    with col2:
        # Columna para la tabla
        st.subheader("🔝 Top 10 combinaciones de país y bodega con más vinos registrados")
        
        # Top 10 combinaciones de país y bodega con más vinos
        df_top_10 = df_grouped_1.sort_values(by="num_vinos", ascending=False).head(10)
        st.table(df_top_10.set_index(["País", "Bodega"]))

    st.divider()
    

    # Primero, agrupar los datos y calcular el número de bodegas por país
    df_grouped_1 = df.groupby("País")["Bodega"].nunique().reset_index(name="num_bodegas")

    # Obtener los 10 países con más bodegas
    df_top_10 = df_grouped_1.sort_values(by="num_bodegas", ascending=False).head(10)

    # Crear las columnas para los gráficos
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas
    
    # Graficar el Top 10 países con más bodegas registradas
    with col1: 
        fig = px.bar(df_top_10, 
                    x='País', 
                    y='num_bodegas', 
                    color='num_bodegas', 
                    title="🏢 Top 10 países con más bodegas registradas",
                    labels={'num_bodegas': 'Número de Bodegas', 'País': 'País'},
                    color_continuous_scale='Viridis')  # Puedes cambiar el color_continuous_scale a tu preferencia

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Mostrar la tabla con los 10 países con más bodegas
    with col2: 
        st.write("🏢 Top 10 países con más bodegas registradas")
        st.table(df_top_10.set_index("País"))
    
    
    st.divider()


    # Average wine rating per country
    df['Valoración'] = pd.to_numeric(df['Valoración'], errors='coerce')
    df_grouped_2 = df.groupby("País").agg(
    num_bodegas=('Bodega', 'nunique'),  # Contamos el número único de bodegas
    avg_valoracion=('Valoración', 'mean')  # Calculamos la valoración promedio
    ).reset_index()

    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas
    with col1: 
        # Crear el gráfico de dispersión
        fig4 = px.scatter(
            df_grouped_2, 
            x="num_bodegas",  # Número de bodegas
            y="avg_valoracion",  # Valoración promedio
            color="avg_valoracion",  # Colorear según la valoración
            hover_name="País",  # Muestra el país al pasar el ratón
            labels={'avg_valoracion': 'Valoración Promedio', 'num_bodegas': 'Número de Bodegas'},
            color_continuous_scale="RdYlGn"  # Color según la valoración
            )

            # Actualizar el diseño del gráfico
        fig4.update_layout(
            title=dict(
                text=f"Número de Bodegas <br> y la Valoración Promedio de {vino_tipo}",
                font=dict(size=16),  # Ajusta el tamaño de la fuente
                x=0.5,  # Centra el título
                xanchor='center'
            )
        )

    # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig4, use_container_width=True)

    # Top 10 países con mejor valoración promedio
    with col2:
        df_min20bodega = df_grouped_2[df_grouped_2['num_bodegas'] > 20]
        df_top_10_valoracion = df_min20bodega.sort_values(by="avg_valoracion", ascending=False).head(10)
        st.write("⭐ Top 10 países con la mejor valoración promedio de vinos")
        st.table(df_top_10_valoracion.set_index("País"))
    
    st.divider()


    # Wine price by country
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
    df_grouped_3 = df.groupby("País")["Precio"].mean().reset_index(name="avg_precio")

    # Contar el número de vinos por país
    df_vino_count = df.groupby("País")["ID"].count().reset_index(name="vino_count")
    
    # Filtrar los países con más de un vino
    df_vino_count_filtered = df_vino_count[df_vino_count["vino_count"] > 1]
    
    # Filtrar df_grouped_3 para incluir solo los países que tienen más de un vino 
    df_grouped_3 = df_grouped_3[df_grouped_3["País"].isin(df_vino_count_filtered["País"])]


    # Create the choropleth map for average price
    fig3 = px.choropleth(df_grouped_3, 
                        locations="País",  
                        locationmode="country names",  
                        color="avg_precio",  
                        hover_name="País",  
                        color_continuous_scale="Viridis",  
                        labels={"avg_precio": "Precio Promedio"})  

    # Adjust map layout
    fig3.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")
    fig3.update_layout(title=f"Precio Promedio de {vino_tipo} por País", geo=dict(showframe=False, projection_type="natural earth"))

    # Display the map in Streamlit
    st.plotly_chart(fig3, use_container_width=True)

    # Top 10 countries with the highest average price
    df_top_10_precio = df_grouped_3.sort_values(by="avg_precio", ascending=False).head(10)
    st.subheader(f"💰 Top 10 países con mayor precio promedio de {vino_tipo}")
    st.table(df_top_10_precio.set_index("País"))

    st.divider()

    st.subheader("Nube de palabras de notas de sabor")

    # Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    if vino_tipo == "Vino Tinto":
        archivo_csv = 'data/datasets/raw/0_VERSION_FINAL_TINTOS.csv'
    elif vino_tipo == "Vino Blanco":
        archivo_csv = "data/datasets/raw/0_VERSION_FINAL_BLANCOS.csv"
    else:
        archivo_csv = "data/datasets/raw/0_VERSION_FINAL_ESPU.csv"

    # Cargar el CSV seleccionado en el DataFrame df
    df = pd.read_csv(archivo_csv)

    # Cargar la imagen de la botella (coloca la imagen en el mismo directorio)
    wine_mask = np.array(Image.open('data/fotos/vaso_botella.png'))  # Cambia el nombre de la imagen y el path si es necesario

    # Ajustar la máscara para el WordCloud
    wine_mask[wine_mask == 0] = 255

    # Seleccionar solo las notas de sabor de todas las columnas especificadas
    columns_of_interest = [
        'Taste_Notes_1_1', 'Taste_Notes_1_2', 'Taste_Notes_1_3',
        'Taste_Notes_2_1', 'Taste_Notes_2_2', 'Taste_Notes_2_3',
        'Taste_Notes_3_1', 'Taste_Notes_3_2', 'Taste_Notes_3_3'
    ]

    # Concatenar todas las notas de sabor en un solo texto, eliminando "No disponible"
    text = ' '.join(df[columns_of_interest].fillna('').replace('No disponible', '').values.flatten())

    # Definir una lista de palabras que quieres excluir
    stopwords = set([
        "de", "la", "del", "y", "a", "en", "el", "es", "los", "las", "un", "una", "con", "por", "para", "sobre", "o", "se", "rojo", "rojos", "bosque"
    ])

    # Limpiar el texto: pasar todo a minúsculas y eliminar caracteres no deseados
    text_cleaned = re.sub(r'\b(?:' + '|'.join(stopwords) + r')\b', '', text)  # Eliminar stopwords
    text_cleaned = re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]', '', text_cleaned)  # Eliminar caracteres no alfabéticos
    text_cleaned = text_cleaned.lower()  # Convertir a minúsculas

    # Contar las palabras utilizando Counter
    word_counts = Counter(text_cleaned.split())

    # Convertir a DataFrame para mejor visualización
    df_word_freq = pd.DataFrame(word_counts.items(), columns=['Palabra', 'Num_Veces'])

    # Calcular el total de palabras
    total_words = sum(df_word_freq['Num_Veces'])

    # Calcular el porcentaje de cada palabra
    df_word_freq['Porcentaje'] = (df_word_freq['Num_Veces'] / total_words) * 100
    df_word_freq['Porcentaje'] = df_word_freq['Porcentaje'].round(2)

    # Ordenar por frecuencia y mostrar las 10 más frecuentes
    df_word_freq = df_word_freq.sort_values(by="Num_Veces", ascending=False).head(10)

    # Crear las columnas para el layout de Streamlit
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    with col1:
        st.subheader("🔝 Top 10 palabras más frecuentes en las notas de sabor:")
        st.table(df_word_freq[['Palabra', 'Num_Veces', 'Porcentaje']].reset_index(drop=True))






    with col2:
        # Crear la nube de palabras con la máscara de botella
        wordcloud = WordCloud(width=2000, height=2000, 
                            background_color='black', 
                            mask=wine_mask,
                            max_words=300,
                            min_font_size=5,
                            colormap='RdYlGn', 
                            contour_width=0.4, 
                            contour_color='black',
                            relative_scaling=0, 
                            random_state=42).generate_from_frequencies(word_counts)

        # Mostrar la visualización de la nube de palabras
        st.subheader("🌟 Nube de palabras:")
        plt.figure(figsize=(10, 10), dpi=100)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        # Mostrar la nube de palabras en Streamlit
        st.pyplot(plt)