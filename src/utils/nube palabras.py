import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from collections import Counter
from wordcloud import WordCloud
from PIL import Image

def nube_palabras():
    st.title("🌐 Nube de palabras")

    # Crear el desplegable para seleccionar el tipo de vino
    vino_tipo = st.selectbox(
        "Selecciona el tipo de vino",
        ("Vino Tinto", "Vino Blanco", "Vino Espumoso")
    )

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
    wine_mask = np.array(Image.open('vaso_botella.png'))  # Cambia el nombre de la imagen y el path si es necesario

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
        st.table(df_word_freq[['Palabra', 'Num_Veces', 'Porcentaje']])

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