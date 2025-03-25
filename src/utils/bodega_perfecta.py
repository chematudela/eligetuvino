
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder



def bodega_perfecta():

    st.title("Datos para una bodega perfecta")
     # Crear el desplegable para seleccionar el tipo de vino
    vino_tipo = st.selectbox(
        "Selecciona el tipo de vino",
        ("Vino Tinto", "Vino Blanco", "Vino Espumoso")
    )

    # Definir las rutas de los archivos CSV según el tipo de vino seleccionado
    if vino_tipo == "Vino Tinto":
        archivo_csv = "data/datasets/processed/df_merged.csv"
        uva_columns = [
            'Aglianico', 'Barbera', 'Blaufränkisch', 'CabernetFranc', 'CabernetSauvignon', 'Carignan',
            'Cariñena', 'Corvina', 'Corvinone', 'Gamay', 'Garnacha', 'Graciano', 'Grenache', 'Malbec',
            'Mencia', 'Merlot', 'Monastrell', 'Montepulciano', 'Mourvedre', 'Nebbiolo', 'NerelloMascalese',
            "Nerod'Avola", 'PetitVerdot', 'PinotNero', 'PinotNoir', 'Primitivo', 'Rondinella', 'Sangiovese',
            'Shiraz/Syrah', 'Tempranillo', 'TourigaNacional', 'Zweigelt'
        ]
    elif vino_tipo == "Vino Blanco":
        archivo_csv = "data/datasets/processed/df_mergedf_blancos.csv"
        uva_columns = [
            "Albariño", "Chardonnay", "CheninBlanc", "Garganega", "GarnachaBlanca",
            "Gewürztraminer", "Godello", "GrenacheBlanc", "GrünerVeltliner", "Macabeo",
            "Malvasia", "Marsanne", "Nodisponible", "PinotBlanc", "PinotGrigio",
            "PinotGris", "PinotMeunier", "PinotNoir", "RibollaGialla", "Riesling",
            "Roussanne", "SauvignonBlanc", "Sémillon", "Verdejo", "Vermentino",
            "Viognier", "Viura", "Weissburgunder", "Xarel-lo"
        ]
    else:
        archivo_csv = "data/datasets/processed/df_mergedf_espumosos.csv"
        uva_columns = [
            "Barbera", "Chardonnay", "CheninBlanc", "Garnacha", "Glera", "Lambrusco",
            "Macabeo", "Malvasia", "Moscato", "MoscatoBianco", "Nodisponible",
            "Parellada", "PinotBlanc", "PinotMeunier", "PinotNero", "PinotNoir",
            "Riesling", "Trepat", "Xarel-lo"
        ]

# Cargar el CSV seleccionado en el DataFrame df
    df = pd.read_csv(archivo_csv)
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
   
    st.markdown("La Bodega perfecta: Mejores valores")

    # Convertir las columnas de uva a columnas dummies
    df_uvas = pd.get_dummies(df[uva_columns])

    # Añadir las columnas dummies al DataFrame original
    df = pd.concat([df, df_uvas], axis=1)

    # Crear un diccionario para almacenar las correlaciones de cada uva
    uva_price_corr = {}

    # 1. Correlación de cada uva con el precio
    for uva in uva_columns:
        # Verifica si la columna dummies para esa uva existe en el DataFrame
        dummy_column = uva
        if dummy_column in df.columns:
            # Agrupar por la columna dummy de cada uva
            uva_price_corr[uva] = df.groupby(dummy_column)[['Precio']].mean()  # Agrupar por cada uva y calcular la media del precio

    # Mostrar las correlaciones
    for uva in uva_columns:
        if uva in uva_price_corr:
            print(f"Correlación de {uva} con el precio:\n", uva_price_corr[uva])

    # 3. Correlación País vs Precio
    pais_price_corr = df.groupby('País').Precio.mean()
    st.write("Correlación País vs Precio", pais_price_corr)

    # 4. Correlación Región vs Precio
    region_price_corr = df.groupby('Región').Precio.mean()
    st.write("Correlación Región vs Precio", region_price_corr)

    # 5. Correlación Vino vs Precio
    vino_price_corr = df.groupby('Bodega').Precio.mean()
    st.write("Correlación Vino vs Precio", vino_price_corr)

    # 6. Combinación país + región + vino
    df['Combinacion'] = df['País'] + '_' + df['Región'] + '_' + df['Bodega']

    # 7. Codificar la columna Combinacion
    le = LabelEncoder()
    df['Combinacion_cod'] = le.fit_transform(df['Combinacion'])

    # 8. Entrenar un modelo para predecir la valoración a partir de las combinaciones
    X = df[['Combinacion_cod', 'Precio']]  # Usar la codificación en lugar del texto
    y = df['Valoración']

    # División del conjunto de datos para entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelo de regresión
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predicciones y evaluación del modelo
    y_pred = model.predict(X_test)
    st.write("Predicción de la valoración estimada:", y_pred)