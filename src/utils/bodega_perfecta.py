
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def bodega_perfecta():

    st.title("Datos para una bodega perfecta")
       
    # Crear el desplegable para seleccionar el tipo de vino
    vino_tipo = st.selectbox(
        "Selecciona el tipo de vino",
        ("Vino Tinto", "Vino Blanco", "Vino Espumoso")
    )

# Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    if vino_tipo == "Vino Tinto":
        archivo_csv = '../data/datasets/processed/df_merged.csv'  
    elif vino_tipo == "Vino Blanco":
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\blancos.csv"  
    else:
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\espumosos.csv"  

    # Cargar el CSV seleccionado en el DataFrame df
    df = pd.read_csv(archivo_csv)

    # Lista de columnas con las uvas
    uva_columns = ['Aglianico', 'Barbera', 'Blaufränkisch', 'CabernetFranc', 'CabernetSauvignon', 'Carignan',
               'Cariñena', 'Corvina', 'Corvinone', 'Gamay', 'Garnacha', 'Graciano', 'Grenache', 'Malbec',
               'Mencia', 'Merlot', 'Monastrell', 'Montepulciano', 'Mourvedre', 'Nebbiolo', 'NerelloMascalese',
               'Nerod\'Avola', 'PetitVerdot', 'PinotNero', 'PinotNoir', 'Primitivo', 'Rondinella', 'Sangiovese',
               'Shiraz/Syrah', 'Tempranillo', 'TourigaNacional', 'Zweigelt']

    # Asegúrate de que las columnas 'Valoración' y 'Precio' sean numéricas
    df['Valoración'] = pd.to_numeric(df['Valoración'], errors='coerce')
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

    # Calcular el ratio de valoración/precio para cada vino
    df['ratio_uva_valor_precio'] = df['Valoración'] / df['Precio']

    # Crear un diccionario para almacenar el promedio del ratio para cada uva
    uva_ratios = {}

    # Calcular el ratio promedio por cada uva (columna)
    for uva in uva_columns:
        # Filtrar los vinos que contienen la uva (donde el valor de la columna es 1)
        uva_vinos = df[df[uva] == 1]
        
        # Calcular el promedio del ratio para esos vinos
        promedio_ratio = uva_vinos['ratio_uva_valor_precio'].mean()
        
        # Almacenar el resultado en el diccionario
        uva_ratios[uva] = promedio_ratio

    # Convertir el diccionario en un DataFrame
    uva_ratios_df = pd.DataFrame(list(uva_ratios.items()), columns=['Uva', 'Promedio_Ratio'])

    # Ordenar el DataFrame por el Promedio_Ratio de mayor a menor
    uva_ratios_sorted = uva_ratios_df.sort_values(by='Promedio_Ratio', ascending=False)

    # Mostrar solo los 10 primeros registros
    top_10_uva_ratios_sorted = uva_ratios_sorted.head(10)

    # Dividir la pantalla en dos columnas para mostrar la tabla y el gráfico
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    with col1:
        # Mostrar la tabla con los 10 primeros registros
        st.write(top_10_uva_ratios_sorted)

    with col2:
        # Crear el gráfico con Altair usando los 10 primeros registros
        chart = alt.Chart(top_10_uva_ratios_sorted).mark_bar().encode(
            x=alt.X('Promedio_Ratio:Q', title='Ratio Valoración/Precio'),
            y=alt.Y('Uva:N', sort='-x', title='Uva'),
            color=alt.Color('Uva:N', legend=None),  # Eliminar la leyenda de color
            tooltip=['Uva:N', 'Promedio_Ratio:Q']  # Mostrar el nombre de la uva y el ratio en el tooltip
        ).properties(
            title='Top 10 Ratio Valoración/Precio por Uva'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

    st.divider()
    
      
    df['Valoración'] = pd.to_numeric(df['Valoración'], errors='coerce')
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

    # Calcular el ratio de valoración/precio
    df['Ratio_Valor_Precio'] = df['Valoración'] / df['Precio']

    # Agrupar por País y Región, y obtener el promedio del ratio
    pais_region_ratio = df.groupby(['País', 'Región'], as_index=False)['Ratio_Valor_Precio'].mean()

    # Ordenar los resultados por el ratio de mayor a menor
    pais_region_ratio = pais_region_ratio.sort_values(by='Ratio_Valor_Precio', ascending=False)

    # Mostrar solo los 10 primeros registros
    top_10_pais_region_ratio = pais_region_ratio.head(10)

    # Crear dos columnas en Streamlit para mostrar la tabla y el gráfico
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    with col1:
        # Mostrar la tabla con los 10 primeros registros
        st.write(top_10_pais_region_ratio)

    with col2:
        # Crear el gráfico con Altair
        chart = alt.Chart(top_10_pais_region_ratio).mark_bar().encode(
            x=alt.X('Ratio_Valor_Precio:Q', title='Ratio Valoración/Precio'),
            y=alt.Y('Región:N', sort='-x', title='Región'),
            color=alt.Color('País:N', legend=None),  # Colorear por país
            tooltip=['Región:N', 'País:N', 'Ratio_Valor_Precio:Q']  # Mostrar la región, país y ratio
        ).properties(
            title='Top 10 Regiones más Valoradas por País'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

    st.divider()

    df['Valoración'] = pd.to_numeric(df['Valoración'], errors='coerce')
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')

    # Calcular el ratio de valoración/precio para cada vino
    df['Ratio_Pais_Valor_Precio'] = df['Valoración'] / df['Precio']

    # Agrupar por País y calcular el promedio del ratio para cada país
    pais_ratio = df.groupby('País', as_index=False)['Ratio_Pais_Valor_Precio'].mean()

    # Ordenar el DataFrame por el Ratio de Valoración/Precio de mayor a menor
    pais_ratio_sorted = pais_ratio.sort_values(by='Ratio_Pais_Valor_Precio', ascending=False)

    # Mostrar solo los 10 primeros países con la mejor relación
    top_10_pais_ratio_sorted = pais_ratio_sorted.head(10)

    # Dividir la pantalla en dos columnas para mostrar la tabla y el gráfico
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    with col1:
        # Mostrar la tabla con los 10 primeros registros
        st.write(top_10_pais_ratio_sorted)

    with col2:
        # Crear el gráfico con Altair usando los 10 primeros registros
        chart = alt.Chart(top_10_pais_ratio_sorted).mark_bar().encode(
            x=alt.X('Ratio_Pais_Valor_Precio:Q', title='Ratio Valoración/Precio'),
            y=alt.Y('País:N', sort='-x', title='País'),
            color=alt.Color('País:N', legend=None),  # Eliminar la leyenda de color
            tooltip=['País:N', 'Ratio_Pais_Valor_Precio:Q']  # Mostrar el nombre del país y el ratio en el tooltip
        ).properties(
            title='Top 10 Países con Mejor Ratio Valoración/Precio'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

    st.divider()

    df['Ratio_Bodega_Valor_Precio'] = df['Valoración'] / df['Precio']

# Agrupar por Bodega y calcular el promedio del ratio para cada bodega
    bodega_ratio = df.groupby('Bodega', as_index=False)['Ratio_Bodega_Valor_Precio'].mean()

    # Ordenar el DataFrame por el Ratio de Valoración/Precio de mayor a menor
    bodega_ratio_sorted = bodega_ratio.sort_values(by='Ratio_Bodega_Valor_Precio', ascending=False)

    # Mostrar solo los 10 primeros bodegas con la mejor relación
    top_10_bodega_ratio_sorted = bodega_ratio_sorted.head(10)

    # Dividir la pantalla en dos columnas para mostrar la tabla y el gráfico
    col1, col2 = st.columns([2, 2])  # Controlamos el tamaño de las columnas

    with col1:
        # Mostrar la tabla con los 10 primeros registros
        st.write(top_10_bodega_ratio_sorted)

    with col2:
        # Crear el gráfico con Altair usando los 10 primeros registros
        chart = alt.Chart(top_10_bodega_ratio_sorted).mark_bar().encode(
            x=alt.X('Ratio_Bodega_Valor_Precio:Q', title='Ratio Valoración/Precio'),
            y=alt.Y('Bodega:N', sort='-x', title='Bodega'),
            color=alt.Color('Bodega:N', legend=None),  # Eliminar la leyenda de color
            tooltip=['Bodega:N', 'Ratio_Bodega_Valor_Precio:Q']  # Mostrar el nombre de la bodega y el ratio en el tooltip
        ).properties(
            title='Top 10 Bodegas con Mejor Ratio Valoración/Precio'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

    st.divider()

    df["Uva"] = df[uva_columns].apply(lambda row: [uva for uva in uva_columns if row[uva] == 1], axis=1)

# Expandir las listas en filas separadas
    df_exploded = df.explode("Uva")

    # Calcular los ratios
    # Agrupar por "Uva" y calcular la media de "Valoración"
    uva_ratios = df_exploded.groupby("Uva")["Valoración"].mean().reset_index()
    # Agrupar por "País" y "Región" y calcular la media de "Valoración"
    pais_region_ratios = df.groupby(["País", "Región"])["Valoración"].mean().reset_index()
    # Agrupar por "País" y calcular la media de "Valoración" y "Precio"
    pais_ratios = df.groupby("País")[["Valoración", "Precio"]].mean().reset_index()
    # Agrupar por "Bodega" y calcular la media de "Valoración" y "Precio"
    bodega_ratios = df.groupby("Bodega")[["Valoración", "Precio"]].mean().reset_index()

    # Filtrar el Top 10 de cada categoría
    top_uvas = uva_ratios.nlargest(10, "Valoración")
    top_paises = pais_ratios.nlargest(10, "Valoración")
    top_bodegas = bodega_ratios.nlargest(10, "Valoración")
    top_regiones = pais_region_ratios.nlargest(10, "Valoración")

    df["País"] = df["País"].str.strip()
    df["Región"] = df["Región"].str.strip()

    top_paises["País"] = top_paises["País"].str.strip()
    top_regiones["País"] = top_regiones["País"].str.strip()
    top_regiones["Región"] = top_regiones["Región"].str.strip()
# Limpiar las columnas clave antes del merge
    df_exploded['Uva'] = df_exploded['Uva'].str.strip().str.lower()
    top_uvas['Uva'] = top_uvas['Uva'].str.strip().str.lower()

    df_exploded['País'] = df_exploded['País'].str.strip().str.lower()
    top_paises['País'] = top_paises['País'].str.strip().str.lower()

    df_exploded['Región'] = df_exploded['Región'].str.strip().str.lower()
    top_regiones['Región'] = top_regiones['Región'].str.strip().str.lower()

    df_exploded['Bodega'] = df_exploded['Bodega'].str.strip().str.lower()
    top_bodegas['Bodega'] = top_bodegas['Bodega'].str.strip().str.lower()

    top_combined = df_exploded.merge(top_uvas, on="Uva")
    top_combined = top_combined.merge(top_paises, on="País")
    top_combined = top_combined.merge(top_regiones, on=["País", "Región"], suffixes=('_left', '_right'))
    top_combined = top_combined.merge(top_bodegas, on="Bodega")


    top_combined["Puntuacion_Combinada"] = top_combined[
        ["Valoración_x", "Valoración_y", "Valoración_left", "Valoración_right"]
        ].mean(axis=1)

        # Seleccionar la mejor combinación
    mejor_combinacion = top_combined.sort_values(by="Puntuacion_Combinada", ascending=False).iloc[0]

        # Mostrar en Streamlit
    st.title("Mejor combinación de vino")

    st.markdown(
            f"""
            ### Mejor combinación encontrada:
            - **Bodega:** {mejor_combinacion['Bodega']}
            - **Uva:** {mejor_combinacion['Uva']}
            - **Región:** {mejor_combinacion['Region']}
            - **País:** {mejor_combinacion['Pais']}
            - **Puntuación combinada:** {mejor_combinacion['Puntuacion_Combinada']:.2f}
            """
        )

        # Mostrar tabla con colores en Streamlit
    st.dataframe(top_combined.sort_values(by="Puntuacion_Combinada", ascending=False).head(10)
            .style.background_gradient(cmap="coolwarm", subset=["Puntuacion_Combinada"]))




"""
    # Crear columnas    tab1, tab2 = st.columns(2)

    with tab1:
        uva_columns = ['Aglianico', 'Barbera', 'Blaufränkisch', 'CabernetFranc', 'CabernetSauvignon', 'Carignan',
               'Cariñena', 'Corvina', 'Corvinone', 'Gamay', 'Garnacha', 'Graciano', 'Grenache', 'Malbec',
               'Mencia', 'Merlot', 'Monastrell', 'Montepulciano', 'Mourvedre', 'Nebbiolo', 'NerelloMascalese',
               'Nerod\'Avola', 'PetitVerdot', 'PinotNero', 'PinotNoir', 'Primitivo', 'Rondinella', 'Sangiovese',
               'Shiraz/Syrah', 'Tempranillo', 'TourigaNacional', 'Zweigelt']

        # Dictionary to store average ratings by grape type
        valoraciones_por_uva = {}

        for uva in uva_columns:
            # Ensure 'Valoración' is numeric and filter for rows where the grape is present (value 1)
            valoracion_media = df[df[uva] == 1]['Valoración'].mean()
            valoraciones_por_uva[uva] = valoracion_media

            # Convert the dictionary to a DataFrame
        tipo_uva_valorada = pd.DataFrame(list(valoraciones_por_uva.items()), columns=['Tipo de uva', 'Valoración'])

            # Sort the DataFrame by 'Valoración'
        tipo_uva_valorada = tipo_uva_valorada.sort_values(by='Valoración', ascending=False)

            # Display the most valued grape types
        st.subheader("Tipos de Uva Más Valorados")
        st.write(tipo_uva_valorada[['Tipo de uva', 'Valoración']])
    
    with tab2:
            # Create a heatmap of ratings by country and grape type
            st.subheader("Heatmap de Valoraciones por País y Tipo de Uva")
            heatmap = alt.Chart(df.melt(id_vars=['País', 'Valoración'], value_vars=uva_columns, var_name='Tipo de uva', value_name='Presencia')).mark_rect().encode(
                x=alt.X('País:O', title="País"),
                y=alt.Y('Tipo de uva:O', title="Tipo de Uva"),
                color=alt.Color('Valoración:Q', scale=alt.Scale(scheme='reds')),
                tooltip=['País', 'Tipo de uva', 'Valoración']
            ).properties(width=400, height=300)

            st.altair_chart(heatmap, use_container_width=True)
    
    st.divider
    
    tab1, tab2 = st.columns(2)
    with tab1: 
        st.write("")
    # Gráfico 2: Precio medio por tipo de uva
    with tab2:
        st.subheader("Precio medio por tipo de uva")
        bar_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('mean(Precio):Q', title="Precio Medio"),
            y=alt.Y('Uva:N', title="Tipo de Uva", sort='-x'),
            color=alt.Color('Uva:N', legend=None)
        ).properties(width=400, height=300)
        st.altair_chart(bar_chart, use_container_width=True)

    st.divider()


    # Gráfico 3: Proporción de vinos por país
    with tab1:
        st.subheader("Distribución de vinos por país")
        country_count = df['País'].value_counts().reset_index()
        country_count.columns = ['País', 'Cantidad']
        pie_chart = alt.Chart(country_count).mark_arc().encode(
            theta='Cantidad:Q',
            color=alt.Color('País:N', legend=None)
        ).properties(width=400, height=300)
        st.altair_chart(pie_chart, use_container_width=True)"
"""
