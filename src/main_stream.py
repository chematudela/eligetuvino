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
<<<<<<< Updated upstream
=======
import json
from utils import pagina_principal,eda_1,bodega_perfecta,vino_perfecto,recomendador_vinos,estimacion_valoracion
from country_mapping import country_mapping

#with open('../data/datasets/processed/country_mapping.json', 'r', encoding="utf-8") as f:
    #country_mapping = json.load(f)
>>>>>>> Stashed changes

country_mapping = {
        "Italia": "Italy",
        "Austria": "Austria",
        "España": "Spain",
        "Francia": "France",
        "Alemania": "Germany",
        "Sudáfrica": "South Africa",
        "Eslovenia": "Slovenia",
        "Australia": "Australia",
        "Portugal": "Portugal",
        "Argentina": "Argentina",
        "Hungría": "Hungary",
        "Grecia": "Greece",
        "New Zealand": "New Zealand",
        "Estados Unidos": "United States",
        "Chile": "Chile",
        "Croacia": "Croatia",
        "Rumanía": "Romania",
        "Bulgaria": "Bulgaria",
        "Marruecos": "Morocco",
        "Perú": "Peru",
        "Brasil": "Brazil",
        "Líbano": "Lebanon",
        "Luxembourg": "Luxembourg",
        "Suiza": "Switzerland",
        "Japón": "Japan",
        "Georgia": "Georgia",
        "Armenia": "Armenia",
        "Ucrania": "Ukraine",
        "México": "Mexico",
        "Reino Unido": "United Kingdom",
        "Israel": "Israel",
        "República Checa": "Czech Republic",
        "Países Bajos": "Netherlands",
        "Bélgica": "Belgium",
        "Canadá": "Canada",
        "Chipre": "Cyprus",
        "Norte de Macedonia": "North Macedonia",
        "Polonia": "Poland",
        "Serbia": "Serbia",
        "Eslovaquia": "Slovakia",
        "Uruguay": "Uruguay",
        "China": "China",
        "Moldavia": "Moldova",
        "Dinamarca": "Denmark",
        "Albania": "Albania",
        "Afganistán": "Afghanistan",
        "Albania": "Albania",
        "Algeria": "Algeria",
        "Andorra": "Andorra",
        "Angola": "Angola",
        "Antigua y Barbuda": "Antigua and Barbuda",
        "Arabia Saudita": "Saudi Arabia",
        "Argentina": "Argentina",
        "Armenia": "Armenia",
        "Australia": "Australia",
        "Austria": "Austria",
        "Azerbaiyán": "Azerbaijan",
        "Bahamas": "Bahamas",
        "Baréin": "Bahrain",
        "Bangladés": "Bangladesh",
        "Barbados": "Barbados",
        "Bélgica": "Belgium",
        "Belice": "Belize",
        "Benín": "Benin",
        "Bhután": "Bhutan",
        "Bielorrusia": "Belarus",
        "Birmania": "Myanmar",
        "Botsuana": "Botswana",
        "Brasil": "Brazil",
        "Brunéi": "Brunei",
        "Bulgaria": "Bulgaria",
        "Burkina Faso": "Burkina Faso",
        "Burundi": "Burundi",
        "Bután": "Bhutan",
        "Cabo Verde": "Cape Verde",
        "Camboya": "Cambodia",
        "Camerún": "Cameroon",
        "Canadá": "Canada",
        "Catar": "Qatar",
        "Chad": "Chad",
        "Chile": "Chile",
        "China": "China",
        "Chipre": "Cyprus",
        "Colombia": "Colombia",
        "Comoras": "Comoros",
        "Congo": "Congo",
        "Corea del Norte": "North Korea",
        "Corea del Sur": "South Korea",
        "Costa Rica": "Costa Rica",
        "Croacia": "Croatia",
        "Cuba": "Cuba",
        "Curazao": "Curaçao",
        "Chipre": "Cyprus",
        "República Checa": "Czech Republic",
        "Côte d'Ivoire": "Ivory Coast",
        "Dinamarca": "Denmark",
        "Djibouti": "Djibouti",
        "Dominica": "Dominica",
        "República Dominicana": "Dominican Republic",
        "Ecuador": "Ecuador",
        "Egipto": "Egypt",
        "El Salvador": "El Salvador",
        "Emiratos Árabes Unidos": "United Arab Emirates",
        "Ecuador": "Ecuador",
        "Eslovaquia": "Slovakia",
        "Eslovenia": "Slovenia",
        "España": "Spain",
        "Estados Unidos": "United States",
        "Etiopía": "Ethiopia",
        "Fiyi": "Fiji",
        "Filipinas": "Philippines",
        "Finlandia": "Finland",
        "Francia": "France",
        "Gabon": "Gabon",
        "Gambia": "Gambia",
        "Georgia": "Georgia",
        "Ghana": "Ghana",
        "Granada": "Grenada",
        "Grecia": "Greece",
        "Guatemala": "Guatemala",
        "Guinea": "Guinea",
        "Guinea-Bisáu": "Guinea-Bissau",
        "Guyana": "Guyana",
        "Haití": "Haiti",
        "Honduras": "Honduras",
        "Hungría": "Hungary",
        "India": "India",
        "Indonesia": "Indonesia",
        "Irak": "Iraq",
        "Irlanda": "Ireland",
        "Isla de Man": "Isle of Man",
        "Islas Cook": "Cook Islands",
        "Islas Feroe": "Faroe Islands",
        "Islas Malvinas": "Falkland Islands",
        "Islandia": "Iceland",
        "Israel": "Israel",
        "Italia": "Italy",
        "Jamaica": "Jamaica",
        "Japón": "Japan",
        "Jordania": "Jordan",
        "Kazajistán": "Kazakhstan",
        "Kenia": "Kenya",
        "Kirguistán": "Kyrgyzstan",
        "Kiribati": "Kiribati",
        "Kuwait": "Kuwait",
        "Laos": "Laos",
        "Lesoto": "Lesotho",
        "Letonia": "Latvia",
        "Líbano": "Lebanon",
        "Liberia": "Liberia",
        "Libia": "Libya",
        "Liechtenstein": "Liechtenstein",
        "Lituania": "Lithuania",
        "Luxemburgo": "Luxembourg",
        "Madagascar": "Madagascar",
        "Malasia": "Malaysia",
        "Malaui": "Malawi",
        "Maldivas": "Maldives",
        "Malta": "Malta",
        "Marruecos": "Morocco",
        "Mauricio": "Mauritius",
        "Mauritania": "Mauritania",
        "México": "Mexico",
        "Micronesia": "Micronesia",
        "Mónaco": "Monaco",
        "Mongolia": "Mongolia",
        "Mozambique": "Mozambique",
        "Namibia": "Namibia",
        "Nauru": "Nauru",
        "Nepal": "Nepal",
        "Nicaragua": "Nicaragua",
        "Níger": "Niger",
        "Nigeria": "Nigeria",
        "Noruega": "Norway",
        "Nueva Zelanda": "New Zealand",
        "Omán": "Oman",
        "Países Bajos": "Netherlands",
        "Pakistán": "Pakistan",
        "Palau": "Palau",
        "Panamá": "Panama",
        "Papúa Nueva Guinea": "Papua New Guinea",
        "Paraguay": "Paraguay",
        "Perú": "Peru",
        "Polonia": "Poland",
        "Portugal": "Portugal",
        "Reino Unido": "United Kingdom",
        "República Checa": "Czech Republic",
        "Rumanía": "Romania",
        "Rusia": "Russia",
        "Ruanda": "Rwanda",
        "Sahara Occidental": "Western Sahara",
        "Samoa": "Samoa",
        "San Cristóbal y Nieves": "Saint Kitts and Nevis",
        "San Marino": "San Marino",
        "Santa Lucía": "Saint Lucia",
        "Senegal": "Senegal",
        "Serbia": "Serbia",
        "Seychelles": "Seychelles",
        "Sierra Leona": "Sierra Leone",
        "Singapur": "Singapore",
        "Siria": "Syria",
        "Somalia": "Somalia",
        "Sri Lanka": "Sri Lanka",
        "Suazilandia": "Eswatini",
        "Sudán": "Sudan",
        "Sudáfrica": "South Africa",
        "Suecia": "Sweden",
        "Suiza": "Switzerland",
        "Surinam": "Suriname",
        "Siria": "Syria",
        "Somalia": "Somalia",
        "Sri Lanka": "Sri Lanka",
        "Tailandia": "Thailand",
        "Tanzania": "Tanzania",
        "Togo": "Togo",
        "Trinidad y Tobago": "Trinidad and Tobago",
        "Túnez": "Tunisia",
        "Turkmenistán": "Turkmenistan",
        "Turquía": "Turkey",
        "Tuvalu": "Tuvalu",
        "Uganda": "Uganda",
        "Ucrania": "Ukraine",
        "Uruguay": "Uruguay",
        "Uzbekistán": "Uzbekistan",
        "Vanuatu": "Vanuatu",
        "Vaticano": "Vatican",
        "Venezuela": "Venezuela",
        "Vietnam": "Vietnam",
        "Yemen": "Yemen",
        "Zambia": "Zambia",
        "Zimbabue": "Zimbabwe"
    }

st.set_page_config(
    page_title="Dashboard sobre vino mundial",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

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
        "Seaborn"
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
        "Librería para visualización de datos estadísticos y gráficos atractivos."
    ]
})

# Mostrar el título
    st.markdown("### Librerías utilizadas")
    st.table(librerias.set_index("Librería"))

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
        archivo_csv = r'C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\tintos.csv'  
    elif vino_tipo == "Vino Blanco":
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\blancos.csv"  
    else:
        archivo_csv = r"C:\Users\yiyip\OneDrive\Documents\GitHub\Proyecto_grupo2_vinos\csv\espumosos.csv"  
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
        st.subheader("🏢 Top 10 países con más bodegas registradas")
        st.table(df_top_10.set_index("País"))


    # Average wine rating per country
    df['Valoración'] = pd.to_numeric(df['Valoración'], errors='coerce')
    df_grouped_2 = df.groupby("País").agg(
    num_bodegas=('Bodega', 'nunique'),  # Contamos el número único de bodegas
    avg_valoracion=('Valoración', 'mean')  # Calculamos la valoración promedio
).reset_index()

    with col1: 
        fig4 = px.scatter(df_grouped_2, 
                        x="num_bodegas",  # Número de bodegas
                        y="avg_valoracion",  # Valoración promedio
                        color="avg_valoracion",  # Colorear según la valoración
                        hover_name="País",  # Muestra el país al pasar el ratón
                        title=f"Relación entre el Número de Bodegas y la Valoración Promedio de {vino_tipo}",
                        labels={'avg_valoracion': 'Valoración Promedio', 'num_bodegas': 'Número de Bodegas'},
                        color_continuous_scale="RdYlGn")  # Color según la valoración

        st.plotly_chart(fig4, use_container_width=True)

    # Top 10 países con mejor valoración promedio
    with col2:
        df_top_10_valoracion = df_grouped_2.sort_values(by="avg_valoracion", ascending=False).head(10)
        st.subheader("⭐ Top 10 países con la mejor valoración promedio de vinos")
        st.table(df_top_10_valoracion.set_index("País"))

    # Wine price by country
    df['Precio'] = pd.to_numeric(df['Precio'], errors='coerce')
    df_grouped_3 = df.groupby("País")["Precio"].mean().reset_index(name="avg_precio")

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