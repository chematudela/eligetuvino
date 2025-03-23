
import streamlit as st
import altair as alt
import pandas as pd

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